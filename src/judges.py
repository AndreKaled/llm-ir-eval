"""Cliente LLM (API compatível com OpenAI, com cache) + métodos de julgamento.

Para adicionar um método novo: escreva uma função `(llm, query, doc) -> dict` e registre em METHODS.
O dict devolvido tem: score, raw, calls, in_tok, out_tok, latency, cached.
"""
import hashlib, json, os, re, sqlite3, time
from pathlib import Path

from openai import OpenAI

# Prompt oficial do UMBRELA: castorini/umbrela @986aae4e (Apache-2.0, ver prompts/LICENSE-umbrela.txt)
UMBRELA = (Path(__file__).parent / "prompts" / "umbrela_qrel_zeroshot_bing.txt").read_text()

# Prompt simples próprio, usado só como controle (não é um método publicado)
SIMPLE = """Judge the relevance of the passage to the query on an integer scale from 0 to 3
(0 = not relevant, 1 = related but does not answer, 2 = partially answers, 3 = perfectly answers).

Query: {query}

Passage: {passage}

Answer only in the format: ##final score: <0-3>"""

FINAL = re.compile(r"##\s*final\s*score\s*:\s*(\d)", re.I)


class LLM:
    """Chama o modelo e guarda tudo em SQLite. No cache devolvemos tokens/latência da chamada original."""

    def __init__(self, model, base_url=None, cache="cache/llm.sqlite", max_tokens=512):
        self.model, self.max_tokens = model, max_tokens
        self.client = OpenAI(base_url=base_url, api_key=os.getenv("OPENAI_API_KEY", "none"))
        Path(cache).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(cache)
        self.db.execute("CREATE TABLE IF NOT EXISTS c (k TEXT PRIMARY KEY, v TEXT)")

    def __call__(self, prompt):
        key = hashlib.sha256(json.dumps([self.model, self.max_tokens, prompt]).encode()).hexdigest()
        row = self.db.execute("SELECT v FROM c WHERE k=?", (key,)).fetchone()
        if row:
            return {**json.loads(row[0]), "cached": True}
        t0 = time.perf_counter()
        r = self.client.chat.completions.create(
            model=self.model, temperature=0, max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}])
        u = r.usage
        out = {"text": r.choices[0].message.content or "",
               "in_tok": u.prompt_tokens if u else 0, "out_tok": u.completion_tokens if u else 0,
               "latency": time.perf_counter() - t0}
        self.db.execute("INSERT OR REPLACE INTO c VALUES (?,?)", (key, json.dumps(out)))
        self.db.commit()
        return {**out, "cached": False}


def pointwise(template):
    """Método pointwise: um prompt -> uma nota 0-3. Tenta de novo 1x se a resposta for inválida."""
    def judge(llm, query, doc, retries=1):
        prompt = template.replace("{query}", query).replace("{passage}", doc[:4000])
        res = {"score": None, "raw": "", "calls": 0, "in_tok": 0, "out_tok": 0, "latency": 0.0, "cached": True}
        for _ in range(retries + 1):
            o = llm(prompt)
            res["calls"] += 1
            res["in_tok"] += o["in_tok"]; res["out_tok"] += o["out_tok"]; res["latency"] += o["latency"]
            res["cached"] = res["cached"] and o["cached"]
            res["raw"] = o["text"]
            m = FINAL.findall(o["text"])  # última ocorrência: o modelo raciocina antes da nota
            if m and int(m[-1]) <= 3:
                res["score"] = int(m[-1])
                break
        return res
    return judge


METHODS = {"umbrela": pointwise(UMBRELA), "simple": pointwise(SIMPLE)}
# Próximo: "criteria": função com 4 chamadas (ver docs/methods.md), mesmo formato de retorno.