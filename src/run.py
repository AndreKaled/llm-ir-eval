"""Uso (dentro do Docker, ver README):
  python src/run.py prepare dl19                       # baixa e prepara os dados
  python src/run.py run dl19 umbrela --limit 20        # julga e grava JSONL
  python src/run.py analyze experiments/dl19_umbrela.jsonl
"""
import argparse, json, os, random
from pathlib import Path
from statistics import mean, median

from judges import LLM, METHODS

DATASETS = {"dl19": "msmarco-passage/trec-dl-2019/judged", "dl20": "msmarco-passage/trec-dl-2020/judged"}


def clean(s):
    return " ".join(s.split())  # TSV de uma linha por registro


#def prepare(name):
#    """Baixa via ir_datasets e guarda só consultas, qrels e as passagens julgadas (não o corpus todo)."""
#    import ir_datasets
#    from tqdm import tqdm
#    ds, out = ir_datasets.load(DATASETS[name]), Path("data") / name
#    out.mkdir(parents=True, exist_ok=True)
#    qrels = [(q.query_id, q.doc_id, q.relevance) for q in ds.qrels_iter()]
#    need = {d for _, d, _ in qrels}
#    (out / "qrels.txt").write_text("".join(f"{q} 0 {d} {r}\n" for q, d, r in qrels))
#    (out / "queries.tsv").write_text("".join(f"{q.query_id}\t{clean(q.text)}\n" for q in ds.queries_iter()))
#    with open(out / "docs.tsv", "w") as f:  # percorre o corpus uma vez (alguns minutos)
#        for d in tqdm(ds.docs_iter(), desc="passagens", total=ds.docs_count()):
#            if d.doc_id in need:
#                f.write(f"{d.doc_id}\t{clean(d.text)}\n")
#    print(f"{len(qrels)} julgamentos em {out}/")

def prepare(name, src_dir=None):
    """Converte queries.jsonl + corpus.jsonl + qrels.tsv para o formato interno.

    src_dir padrão: data/<name>_raw/
    Espera os três arquivos do HuggingFace nesse diretório.
    """
    src_dir = Path(src_dir) if src_dir else Path("data") / f"{name}_raw"
    out = Path("data") / name
    out.mkdir(parents=True, exist_ok=True)

    # queries.jsonl -> queries.tsv  (qid \t texto)
    with open(src_dir / "queries.jsonl") as f, open(out / "queries.tsv", "w") as g:
        for line in f:
            if not line.strip():
                continue
            o = json.loads(line)
            g.write(f"{o['_id']}\t{clean(o['text'])}\n")

    # corpus.jsonl -> docs.tsv  (docid \t texto)
    with open(src_dir / "corpus.jsonl") as f, open(out / "docs.tsv", "w") as g:
        for line in f:
            if not line.strip():
                continue
            o = json.loads(line)
            g.write(f"{o['_id']}\t{clean(o['text'])}\n")

    # qrels.tsv -> qrels.txt  (TREC: qid 0 docid rel)
    with open(src_dir / "qrels.tsv") as f, open(out / "qrels.txt", "w") as g:
        for line in f:
            if not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            qid, docid, rel = parts[0], parts[1], parts[-1]
            g.write(f"{qid} 0 {docid} {rel}\n")

    n_q = sum(1 for _ in open(out / "queries.tsv"))
    n_d = sum(1 for _ in open(out / "docs.tsv"))
    n_r = sum(1 for _ in open(out / "qrels.txt"))
    print(f"pronto: {out}/ ({n_q} queries, {n_d} docs, {n_r} qrels)")


def load(name):
    d = Path("data") / name
    kv = lambda p: dict(l.rstrip("\n").split("\t", 1) for l in open(p) if "\t" in l)
    queries, docs = kv(d / "queries.tsv"), kv(d / "docs.tsv")
    pairs = []
    for line in open(d / "qrels.txt"):
        q, _, doc, rel = line.split()
        if q in queries and doc in docs:
            pairs.append((q, doc, queries[q], docs[doc], int(rel)))
    return pairs


def run_pairs(pairs, llm, method, out, dataset=""):
    """Julga cada par e grava um JSONL. Retomável: pares já presentes no arquivo são pulados."""
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if os.path.exists(out):
        done = {(r["method"], r["model"], r["qid"], r["docid"]) for r in map(json.loads, open(out))}
    new = 0
    with open(out, "a") as f:
        for qid, docid, query, text, label in pairs:
            if (method, llm.model, qid, docid) in done:
                continue
            r = METHODS[method](llm, query, text)
            f.write(json.dumps({"dataset": dataset, "method": method, "model": llm.model, "qid": qid,
                                "docid": docid, "human": label, **r}, ensure_ascii=False) + "\n")
            f.flush()
            new += 1
    return new


def analyze(path, price_in=0.0, price_out=0.0):
    """Concordância com o humano + custo e latência. price_* = USD por 1M de tokens."""
    from sklearn.metrics import cohen_kappa_score as kappa
    rs = [json.loads(l) for l in open(path)]
    ok = [r for r in rs if r["score"] is not None]
    h, m = [r["human"] for r in ok], [r["score"] for r in ok]
    return {
        "n": len(rs), "invalid_rate": 1 - len(ok) / len(rs),
        "kappa": kappa(h, m), "kappa_quadratic": kappa(h, m, weights="quadratic"),
        "kappa_binary(>=2)": kappa([x >= 2 for x in h], [x >= 2 for x in m]),
        "mae": mean(abs(a - b) for a, b in zip(h, m)),
        "bias(+ = LLM superestima)": mean(b - a for a, b in zip(h, m)),
        "calls_per_judgment": mean(r["calls"] for r in rs),
        "latency_mean_s": mean(r["latency"] for r in rs), "latency_median_s": median(r["latency"] for r in rs),
        "in_tokens": sum(r["in_tok"] for r in rs), "out_tokens": sum(r["out_tok"] for r in rs),
        "est_cost_usd": sum(r["in_tok"] for r in rs) / 1e6 * price_in + sum(r["out_tok"] for r in rs) / 1e6 * price_out,
    }
    # TODO quando houver runs de sistemas: nDCG@10 por sistema e Kendall tau (humano vs LLM).


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("prepare")
    p.add_argument("name", choices=DATASETS)
    p.add_argument("--src", default=None,
                    help="diretório com queries.jsonl, corpus.jsonl, qrels.tsv "
                            "(default: data/<name>_raw/)")

    r = sub.add_parser("run")
    r.add_argument("name", choices=DATASETS)
    r.add_argument("method", choices=METHODS)
    r.add_argument("--limit", type=int)
    r.add_argument("--model", default=os.getenv("MODEL", "llama3.1:8b"))
    r.add_argument("--base-url", default=os.getenv("BASE_URL"))
    a = sub.add_parser("analyze")
    a.add_argument("path")
    a.add_argument("--price-in", type=float, default=0.0)
    a.add_argument("--price-out", type=float, default=0.0)
    args = ap.parse_args()

    if args.cmd == "prepare":
        prepare(args.name, args.src)
    elif args.cmd == "run":
        pairs = load(args.name)
        if args.limit:
            pairs = random.Random(0).sample(pairs, min(args.limit, len(pairs)))  # amostra fixa (seed 0)
        out = f"experiments/{args.name}_{args.method}.jsonl"
        n = run_pairs(pairs, LLM(args.model, args.base_url), args.method, out, args.name)
        print(f"{n} novos julgamentos em {out}")
    else:
        print(json.dumps(analyze(args.path, args.price_in, args.price_out), indent=2))