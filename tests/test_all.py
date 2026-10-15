from llm_ir_eval.datasets import TrecFilesDataset
from llm_ir_eval.eval import (agreement_metrics, efficiency_summary, load_records,
                              ndcg_at_k, system_ranking_tau)
from llm_ir_eval.judges import SimplePointwiseJudge, parse_score
from llm_ir_eval.llm.cache import CachedClient
from llm_ir_eval.runner import run_judge
from llm_ir_eval.types import LLMResponse


class FakeClient:
    model = "fake"
    temperature = 0.0
    max_tokens = 10

    def __init__(self, replies):
        self.replies, self.calls = list(replies), 0

    def complete(self, messages, **params):
        self.calls += 1
        txt = self.replies[(self.calls - 1) % len(self.replies)]
        return LLMResponse(text=txt, model="fake", input_tokens=10, output_tokens=3, latency_s=0.1)


def test_parse_score():
    assert parse_score('{"score": 2}') == 2
    assert parse_score('Sure! {"score": 3}') == 3
    assert parse_score("score: 1") == 1
    assert parse_score("2") == 2
    assert parse_score('{"score": 7}') is None
    assert parse_score("não sei") is None


def _make_files(tmp_path):
    (tmp_path / "q.tsv").write_text("1\tquery one\n2\tquery two\n")
    (tmp_path / "d.tsv").write_text("a\tdoc a\nb\tdoc b\nc\tdoc c\n")
    (tmp_path / "qrels.txt").write_text("1 0 a 3\n1 0 b 0\n2 0 c 2\n")
    return TrecFilesDataset("t", tmp_path / "q.tsv", tmp_path / "d.tsv", tmp_path / "qrels.txt")


def test_runner_resume_and_metrics(tmp_path):
    ds = _make_files(tmp_path)
    assert len(list(ds.pairs())) == 3
    client = FakeClient(['{"score": 3}', '{"score": 1}', "lixo", '{"score": 2}'])
    judge = SimplePointwiseJudge(client, retries=1)
    out = tmp_path / "out.jsonl"
    assert run_judge(ds, judge, "fake", out) == 3
    assert run_judge(ds, judge, "fake", out) == 0  # retomável: nada refeito
    recs = load_records(str(out))
    assert len(recs) == 3 and recs[2]["n_calls"] == 2  # retry no 3º par
    ag = agreement_metrics(recs)
    assert ag["n_valid"] == 3 and ag["invalid_rate"] == 0
    assert efficiency_summary(recs)["input_tokens"] > 0


def test_cache(tmp_path):
    inner = FakeClient(['{"score": 1}'])
    c = CachedClient(inner, tmp_path / "c.sqlite")
    r1 = c.complete([{"role": "user", "content": "x"}])
    r2 = c.complete([{"role": "user", "content": "x"}])
    assert inner.calls == 1 and not r1.cached and r2.cached and r2.latency_s == r1.latency_s


def test_system_ranking():
    human = {"q": {"a": 3, "b": 0}}
    runs = {"good": {"q": ["a", "b"]}, "bad": {"q": ["b", "a"]}, "mid": {"q": ["b", "x", "a"]}}
    assert abs(ndcg_at_k(["a", "b"], human["q"]) - 1.0) < 1e-9
    assert system_ranking_tau(runs, human, {"q": {"a": 2, "b": 1}}) == 1.0


def test_umbrela_parse_and_prompt():
    from llm_ir_eval.judges import UmbrelaJudge, parse_umbrela_score
    assert parse_umbrela_score("reasoning...\n##final score: 2") == 2
    assert parse_umbrela_score("##final score: 1 ... depois ##Final Score: 3") == 3
    assert parse_umbrela_score("##final score: 9") is None
    assert parse_umbrela_score("sem nota") is None

    seen = {}

    class Spy(FakeClient):
        def complete(self, messages, **params):
            seen["prompt"] = messages[0]["content"]
            return super().complete(messages, **params)

    j = UmbrelaJudge(Spy(["analysis\n##final score: 3"]))
    res = j.judge("my query", "my passage")
    assert res.score == 3 and res.n_calls == 1
    assert "my query" in seen["prompt"] and "my passage" in seen["prompt"]
    assert "{query}" not in seen["prompt"] and "{passage}" not in seen["prompt"]
