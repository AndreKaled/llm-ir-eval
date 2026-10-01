# Matriz Consolidada de Métodos — Avaliação Automática de RI com LLMs

Inventário consolidado e filtrado pelo escopo do PIBIT (com auxílio do Kimi K3 e Claude Sonnet 4.6 baixo): avaliação automática de relevância ad-hoc (documento-consulta) com LLMs. Métodos exclusivos de RAG e de re-ranking foram excluídos (ver tabela de ignorados ao final).
Revisão nº 2: 2026-09-08. Todos os campos conferidos contra os PDFs dos artigos (quando o artigo estava disponível); nada foi inferido além do texto.

Será revisado manualmente by me, andré kaled :D
as observaçoes foram feitas pelo Kimi, então talvez estejam falando de algo do artigo em si puramente pra preencher o campo ou delirando lalalala e nao concordo sem ter visto o artigo ao todo, portanto se veres antes de eu apagar essa linha, discorde de tudo até leitura do artigo como eu. Considere os artigos com o Título linkado ao invés de apenas o link como vistos parcialmente por mim e com as observações de autoria própria.lalalalalala

## Métodos no escopo

| Método | Ano | Abordagem | Paper | Código | Benchmark | Observações |
|--------|-----|-----------|-------|--------|-----------|-------------|
| UMBRELA | 2024 | Pointwise | [UMBRELA: UMbrela is the (Open-Source Reproduction of the) Bing RELevance Assessor](https://arxiv.org/abs/2406.06519) | [Sim](https://github.com/castorini/umbrela) | TREC DL 2019–2023 | Código aparentemente inclui modelos da OpenAI, GeminiJudge, Hugging Face transformer e aparentemente tem relação com EnsembleJudge |
| UMBRELA em outros LLMs (Farzi & Dietz) | 2025 | Pointwise (reprodução/validação do UMBRELA) | [Does UMBRELA Work on Other LLMs?](https://arxiv.org/abs/2507.09483) | [Sim](https://github.com/TREMA-UNH/appendix-umbrella-other-llm) | TREC DL 2019, DL 2020, DL 2023 | código do github conta com reimplementação própria dos autores; prompts do repositório UMBRELA |faz
| Thomas et al. | 2024 | Pointwise | [Large language models can accurately predict searcher preferences](https://arxiv.org/abs/2309.10621) | Não | TREC Robust 2004 | Xeretei rapidamente e não vi github, porém há outros links que olharei depois, pode estar hospedado em outros lugares, AVISO: tem prompt no artigo :D |
| Faggioli et al. | 2023 | Pointwise | [Perspectives on Large Language Models for Relevance Judgment](https://arxiv.org/abs/2304.09161) | Não | TREC-8, TREC DL 2021 | Piloto com prompts simples, define espectro de colaboração humano-máquina, re-julgamento de TREC DL 2021 com few-shot|
| Criteria-Based (Four Prompts) | 2024 | Pointwise + decomposição | [Best in Tau@LLMJudge: Criteria-Based Relevance Evaluation with Llama3](https://arxiv.org/abs/2410.14044) | Não | LLMJudge (TREC DL 2023) | Decompõe relevância em 4 critérios (exactness, coverage, topicality, contextual fit); melhor Kendall's τ do desafio (0,9483); LLaMA-3-8B-Instruct, o github só contém o dataset, mas tem prompts no artigo |
| Criteria-Based (sumdecompose) | 2024 | Pointwise + decomposição | [Best in Tau@LLMJudge: Criteria-Based Relevance Evaluation with Llama3](https://arxiv.org/abs/2410.14044) | Não | LLMJudge (TREC DL 2023) | Agregação por soma com mapeamento de faixas (10–12->3; 7–9->2; 5–6->1; 0–4->0); Kendall's τ 0,9300 |
| Criteria-Based (naiveBdecompose) | 2024 | Pointwise + decomposição | [Best in Tau@LLMJudge: Criteria-Based Relevance Evaluation with Llama3](https://arxiv.org/abs/2410.14044) | Não | LLMJudge (TREC DL 2023) | Agregação por Gaussian Naive Bayes (scikit-learn) treinado nas notas dos critérios; Kendall's τ 0,9128 |
| Criteria-Based (COT) | 2024 | Pointwise + decomposição + gate binário | [Best in Tau@LLMJudge: Criteria-Based Relevance Evaluation with Llama3](https://arxiv.org/abs/2410.14044) | Não | LLMJudge (TREC DL 2023) | Pré-check binário (prompt de Sun et al.); se relevante, avalia Exactness+Coverage e rotula 2–3; se não, avalia Topicality+Contextual Fit e rotula 0–1; Kendall's τ 0,8956 |
| Criteria-Based (query-style synthesis) | 2024 | Outra (síntese estilo-query + similaridade) | [Best in Tau@LLMJudge: Criteria-Based Relevance Evaluation with Llama3](https://arxiv.org/abs/2410.14044) | Não | LLMJudge (TREC DL 2023) | Gera uma pseudo-query para a passagem e pontua similaridade com a consulta original (0–3); não é julgamento pointwise; τ 0,8200 (????? vou ler isso melhor) |
| Pointwise Legal (simple) | 2026 | Pointwise | [NormasTCU --- A Brazilian Portuguese IR Dataset and an Evaluation of LLM-as-a-Judge for Relevance Assessment](https://arxiv.org/abs/2608.27746) | Não (dataset público no [HF](https://huggingface.co/datasets/LeandroRibeiro/NormasTCU)) | NormasTCU | Score direto em PT-BR, domínio jurídico; escala 0–2; 3 LLMs (deepseek-3.2, gpt-5-mini, sabiazinho-4); temperature 0. Dataset disponível no HF |
| Pointwise Legal (rationale) | 2026 | Pointwise + rationale | [NormasTCU --- A Brazilian Portuguese IR Dataset and an Evaluation of LLM-as-a-Judge for Relevance Assessment](https://arxiv.org/abs/2608.27746) | Não (dataset público no [HF](https://huggingface.co/datasets/LeandroRibeiro/NormasTCU)) | NormasTCU | Justificativa antes da nota; LLMs com viés positivo (MAE 0,46–0,66; κ 0,32–0,53); rationale melhora ranking de sistemas (nDCG@10/MRR) sem reduzir viés por par; P@10/R@10 instáveis.  Dataset disponível no HF|
| JudgeBlender (PromptBlender) | 2024 | Ensemble (sobre julgamentos pointwise) | [JudgeBlender: Ensembling Judgments for Automatic Relevance Assessment](https://arxiv.org/abs/2412.13268) | [Sim](https://github.com/rahmanidashti/JudgeBlender) | LLMJudge (TREC DL 2023) | 1 LLM (Llama-3-8B) × 3 prompts (Thomas; decomposição em critérios tipo MultiCriteria; two-step binário→nota de Sun); agregação AV ou MV com desempate (MV(Avg.), MV(Max.), MV(Min.)). O código-fonte só tem analise para geração dos gráficos, sem código para garantir reprodutibilidade (inclusive tentei [engenharia reversa aqui](https://github.com/AndreKaled/JudgeBlender-Implementation)) |
| JudgeBlender (LLMBlender) | 2024 | Ensemble (sobre julgamentos pointwise) | [JudgeBlender: Ensembling Judgments for Automatic Relevance Assessment](https://arxiv.org/abs/2412.13268) | [Sim](https://github.com/rahmanidashti/JudgeBlender) (prompts) | LLMJudge (TREC DL 2023) | 3 LLMs com prompts distintos: Mistral-7B (critérios), Gemma-7B (Thomas), Llama-3-8B (two-step); melhor variante geral: LLMBlender-MV(Avg.). O código-fonte só tem analise para geração dos gráficos, sem código para garantir reprodutibilidade (inclusive tentei [engenharia reversa aqui](https://github.com/AndreKaled/JudgeBlender-Implementation)) |
| One-Shot Labeling (DuoPrompt) | 2023 | Pairwise | [One-Shot Labeling for Automatic Relevance Estimation](https://arxiv.org/abs/2302.11266) | [Sim](https://github.com/seanmacavaney/autoqrels) | TREC DL 2019–2021 | Não entendi nada, vou olhar dps mas nao parece ser codigo fonte pra reproduzir experimento pelo menos, deve ser outra coisa (hipotese minha estou com sono) |
| One-Shot Labeling (DuoT5) — baseline | 2023 | Pairwise (supervisionado) | [One-Shot Labeling for Automatic Relevance Estimation](https://arxiv.org/abs/2302.11266) | [Sim](https://github.com/seanmacavaney/autoqrels) | TREC DL 2019–2021 | T5-3B fine-tunado de relevância relativa (DuoT5 de Pradeep et al. 2021) — não é zero-shot; usar como baseline supervisionado (a ler) |


## Datasets para experimentar
| Artigo/Link | Detalhe |
|---|---|
| [TREC Deep Learning](https://microsoft.github.io/msmarco/TREC-Deep-Learning) | "benchmark âncora" para avaliação automática por LLM, investigar |
| [BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663) | Framework com diversos datasets, melhor para verificar se o método funciona além de um único corpus, investigar|
| [MS MARCO](https://huggingface.co/datasets/microsoft/ms_marco) | Dataset da Microsoft para o navegador Bing, investigar dps |
| [NormasTCU --- A Brazilian Portuguese IR Dataset and an Evaluation of LLM-as-a-Judge for Relevance Assessment](https://arxiv.org/abs/2608.27746)|Brasileiro, talvez seja bom para medir se a avaliação automática generaliza para normas e pareceres de domínio específico (juridico), investigar dps|
| [JurisTCU: A Brazilian Portuguese Information Rtrieval Dataset with Query Relevance Judgments](https://arxiv.org/abs/2503.08379)| Brasileiro, útil para separar "normativo" de "jurisprudencial", dominio específico (juridico), investigar dps |
---

a partir de baixo, não garanto nada tbm irei ver mais tarde


## Baselines (não são métodos LLM candidatos)

| Método | Ano | Abordagem | Paper | Papel no estudo |
|--------|-----|-----------|-------|-----------------|
| One-Shot Labeling (MaxRep) | 2023 | k-NN (BM25/TCT) | [arXiv:2302.11266](https://arxiv.org/abs/2302.11266) | Baseline não-LLM por similaridade com d+ (k=128, ganho linear decrescente); sem uso da consulta; correlação de sistemas < 0,87 |

## Métodos ignorados (fora do escopo do PIBIC)

| Método | Paper | Motivo da exclusão |
|--------|-------|--------------------|
| RUBRIC (Question e Nugget) | [Pencils Down! (ICTIR 2024)](https://dl.acm.org/doi/10.1145/3664190.3672511) | Avalia answerability de perguntas de teste/nuggets sobre respostas de sistemas retrieve/generate — paradigma de RAG/geração, não relevância ad-hoc documento-consulta (tem código: Question-RUBRIC no Autograding Workbench) |
| AutoNuggetizer | [The Great Nugget Recall (SIGIR 2025)](https://arxiv.org/abs/2504.15068) | Mede recall de nuggets em respostas geradas por sistemas RAG — fora do escopo |
| SA Judge / Auto-Judge | [Auto-Judge (SIGIR 2026)](https://doi.org/10.1145/3805712.3808601) | Benchmark de meta-avaliação de juízes LLM para RAG com citações (DRAGUN, RAG, RAGTIME 2025); o SA Judge é um baseline interno (prompt de entailment 8-shot do Auto-ARGUE) que verifica suporte de citações — fora do escopo |
| RankGPT (Permutation Generation) | [Is ChatGPT Good at Search? (EMNLP 2023)](https://arxiv.org/abs/2304.09542) | Método de re-ranking listwise (permutation generation + janela deslizante); não gera qrels/julgamentos — foge do objetivo de avaliação automática |
| LRL (Listwise Reranker) | [Zero-Shot Listwise Document Reranking (arXiv:2305.02156)](https://arxiv.org/abs/2305.02156) | Idem: re-ranking zero-shot, não avaliador; sem código disponível |
| Framework de Merlo et al. (Confidence-/Budget-Based) | [A Cost-Effective Framework (CIKM 2025)](https://dl.acm.org/doi/10.1145/3746252.3761200) | Framework estatístico de meta-avaliação (amostragem SRS + intervalo de Wald) para estimar MAE e κ de julgamentos já gerados — não realiza julgamentos; candidato a apoio metodológico na etapa de meta-avaliação do PIBIC |
| LLM-BLENDER (Jiang et al.) | [arXiv:2306.02561](https://arxiv.org/abs/2306.02561) | Ensembling de GERAÇÕES de LLMs (PairRanker + GenFuser), benchmark MixInstruct — não é avaliação de RI nem o JudgeBlender (baixado por engano em vez do artigo de Rahmani et al.) |

## Literatura de apoio (não são métodos candidatos)

| Artigo | Papel para o PIBIC |
|--------|--------------------|
| LLMJudge: LLMs for Relevance Judgments ([arXiv:2408.08896](https://arxiv.org/abs/2408.08896)) | Descrição do desafio/benchmark LLMJudge (25 queries dev + 25 teste, TREC DL 2023) usado por TREMA e JudgeBlender |
| Judging the Judges ([arXiv:2502.13908](https://arxiv.org/abs/2502.13908)) | Recurso com 42 conjuntos de julgamentos do LLMJudge; análise de viés de escores entre métodos |
| A Large-Scale Study of Relevance Assessments Using UMBRELA ([ICTIR 2025](https://doi.org/10.1145/3731120.3744605)) | Validação in situ do UMBRELA (TREC 2024 RAG, tarefa de recuperação ad hoc): julgamentos automáticos replicam rankings em nível de run, mas com resolução limitada (nDCG@20) e viés positivo vs. NIST |
| From Generation to Judgment (EMNLP 2025) | Survey geral de LLM-as-a-judge (taxonomia: atributos, metodologias, benchmarks) |
| LLM4Eval @SIGIR 2024 / @WSDM 2025 | Páginas dos workshops (contexto da comunidade) |

## Relatório de correções (revisão nº 1 -> nº 2, com os PDFs em mãos)

1. **PDF errado identificado:** o arquivo "LLM-BL E N D E R" enviado é Jiang et al. 2023
   (ensembling de gerações, ACL 2023) — NÃO é o JudgeBlender (Rahmani et al.,
   arXiv:2412.13268). Os campos do JudgeBlender foram re-verificados diretamente no
   arXiv nesta revisão: PromptBlender = Llama-3-8B × 3 prompts (Thomas / critérios /
   two-step de Sun); LLMBlender = Mistral-7B (critérios), Gemma-7B (Thomas),
   Llama-3-8B (two-step); agregações AV e MV(Avg./Max./Min.); melhor variante
   LLMBlender-MV(Avg.); prompts no GitHub (link adicionado à coluna Código).
2. **SA Judge — URL localizada:** o artigo não enviado era "Auto-Judge: A Cross-Task
   Benchmark..." (Farzi et al., SIGIR 2026, DOI 10.1145/3805712.3808601). O SA Judge é
   um baseline interno desse benchmark (prompt 8-shot de entailment do Auto-ARGUE,
   RAGTIME 2025). Mantido como ignorado (RAG), agora com link correto.
3. **Nova linha no escopo:** "UMBRELA em outros LLMs" (Farzi & Dietz, 2025,
   arXiv:2507.09483) — reprodução do UMBRELA com GPT-4o, DeepSeek V3, LLaMA-3.3-70B,
   LLaMA-3-8B e FLAN-T5-large em TREC DL 2019/2020/2023. Diretamente relevante para o
   eixo custo/qualidade do PIBIC. Código: o paper não indica repositório público
   (os autores reimplementaram; prompts do repo UMBRELA) — marcado "Não".
4. **Nova linha ignorada:** Merlo et al. (CIKM 2025) — confirmado pelos PDF que é um
   framework estatístico de meta-avaliação (procedimentos Confidence-Based e
   Budget-Based com SRS + Wald), não um julgador. Sugerido como apoio metodológico
   para a meta-avaliação do PIBIC. Link ACM adicionado (DOI 10.1145/3746252.3761200).
5. **Campos conferidos e confirmados contra os PDFs (sem alteração):**
   - NormasTCU: sem código no paper (só dataset no HF); números (14.469 docs, 46
     queries, 812 pares, MAE 0,46–0,66, κ 0,32–0,53) batem com a matriz.
   - Thomas et al.: TREC Robust 2004, 250 tópicos, GPT-4 in-house, sem código.
   - Faggioli et al.: TREC-8 e TREC DL 2021; GPT-3.5 = text-davinci-003; sem código.
   - Criteria-Based/TREMA: LLaMA-3-8B-Instruct; código não mencionado no paper
     ("Não" mantido); variantes e nomes dos 4 critérios confirmados.
   - UMBRELA: TREC DL 2019–2023, GPT-4o, código castorini/umbrela confirmado.
   - One-Shot Labeling: DuoPrompt usa Flan-T5 com teacher-forcing (probabilidade
     yes/no) — confirma "Pairwise"; pacote de código publicado; TREC DL 2019–2021.
   - MaxRep: k=128, BM25/TCT, não usa a consulta — confirma baseline não-LLM.
   - RankGPT: re-ranking com janela deslizante — confirma exclusão.
6. **Detalhes adicionados (estavam nos PDFs, enriqueceram as Observações):** τ/κ do
   UMBRELA por track; mapeamento de faixas do sumdecompose; nomes dos LLMs do
   NormasTCU; correlações de sistemas do One-Shot; melhor variante do JudgeBlender.
7. **Seção "Literatura de apoio" criada** para os PDFs que não são métodos nem
   entram na comparação (workshops LLM4Eval, survey, LLMJudge, Judging the Judges,
   Large-Scale Study UMBRELA) — nada descartado, apenas classificado.

## Relatório de correções (versão original -> revisão nº 1, mantido para histórico)

1. **Duplicata removida:** "Thomas et al." e "Thomas et al. (Direct Prompting)" eram o
   mesmo paper (arXiv:2309.10621) — consolidado em uma linha.
2. **NormasTCU — código:** tabela original marcava "Código: Sim". O artigo não
   disponibiliza código de avaliação; o que é público é o dataset (14.469 documentos,
   46 consultas, 812 pares julgados, escala 0–2) no HuggingFace. Corrigido para "Não",
   com link do dataset.
3. **UMBRELA — benchmark:** saída do NotebookLM listava "TREC Robust 2004, TREC RAG
   2024". O paper reporta experimentos apenas em TREC DL 2019–2023; o uso no TREC 2024
   RAG Track é aplicação posterior, não benchmark do estudo.
4. **UMBRELA — sigla DNA:** é Descriptive, Narrative, Aspects (técnica de prompting
   zero-shot), não "intenção provável e confiabilidade".
5. **JudgeBlender — detalhes:** PromptBlender usa 1 LLM (Llama-3-8B) com 3 prompts;
   LLMBlender usa 3 LLMs (Mistral-7B, Gemma-7B, Llama-3-8B) com prompts distintos;
   agregação inclui AV, MV(Avg.), MV(Max.), MV(Min.).
6. **JudgeBlender — ano:** arXiv dez/2024, The Web Conf 2025 — "2024/2025".
7. **Criteria-Based (COT):** renomeado de "árvore" para "gate binário" (pré-check
   binário com desvio condicional; sem árvore de decisão explícita).
8. **DuoT5:** reclassificado como "Pairwise (supervisionado)" — T5-3B fine-tunado,
   diferente dos métodos zero-shot; movido para baseline.