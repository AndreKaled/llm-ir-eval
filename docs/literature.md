# MATRIZ COMPARATIVA DE MÉTODOS DE AVALIAÇÃO AUTOMÁTICA DE RI COM LLMs

## Metodologia da Matriz

Esta matriz consolida os métodos identificados nos artigos originais, organizando-os por **variante metodológica** e não por artigo. Cada linha representa uma unidade experimentalmente distinta. A classificação segue a auditoria científica realizada, que corrigiu atribuições imprecisas de métricas, latências e escopo.

---

## MATRIZ COMPLETA

### 1. Identificação e Classificação

| Método | Variante | Artigo | Ano | Classificação | Família/Abordagem |
|--------|----------|--------|-----|---------------|-------------------|
| UMBRELA | DNA Prompting | Upadhyay et al. [927] | 2024 | **Núcleo** | Pointwise Direto |
| UMBRELA | Basic Prompt | Farzi & Dietz [221] | 2025 | **Núcleo** | Pointwise Direto (simplificado) |
| Criteria-Based | 4prompts | Farzi & Dietz [188] | 2024 | **Núcleo** | Pointwise com Decomposição |
| Criteria-Based | sumdecompose | Farzi & Dietz [188] | 2024 | **Núcleo** | Pointwise com Decomposição |
| Criteria-Based | naiveBdecompose | Farzi & Dietz [188] | 2024 | **Núcleo** | Pointwise com Decomposição |
| Criteria-Based | COT (Bifurcação) | Farzi & Dietz [188] | 2024 | **Núcleo** | Pointwise com Decomposição + Árvore |
| Pointwise Legal | simple | Fernandes et al. [599] | 2026 | **Núcleo** | Pointwise Direto (Português) |
| Pointwise Legal | rationale | Fernandes et al. [599] | 2026 | **Núcleo** | Pointwise com Rationale |
| JudgeBlender | PromptBlender | Rahmani et al. [338] | 2025 | **Ensemble/Wrapper** | Ensemble de prompts |
| JudgeBlender | LLMBlender + MV(Avg.) | Rahmani et al. [338] | 2025 | **Ensemble/Wrapper** | Ensemble de modelos |
| RUBRIC | Question RUBRIC | Farzi & Dietz [741] | 2024 | **RAG/Conteúdo** | Decomposição em Perguntas |
| RUBRIC | Nugget RUBRIC | Farzi & Dietz [741] | 2024 | **RAG/Conteúdo** | Decomposição em Nuggets |
| AutoNuggetizer | Fully Automatic | Pradeep et al. [884] | 2025 | **RAG/Conteúdo** | Extração de Fatos (Nuggets) |
| One-Shot Labeling | DuoPrompt | MacAvaney & Soldaini [697] | 2023 | **Relacionado** | Pairwise + k-NN |
| One-Shot Labeling | DuoT5 | MacAvaney & Soldaini [697] | 2023 | **Relacionado** | Pairwise supervisionado |
| RankGPT | Permutation Generation | Sun et al. [266] | 2023 | **Re-ranking** | Listwise (Sliding Window) |

---

### 2. Tarefa e Unidade de Avaliação

| Método/Variante | Objetivo | Tarefa Avaliada | Unidade | Entrada | Saída | Escala | Gera Qrels? | Qrel Absoluto/Relativo |
|-----------------|----------|-----------------|---------|---------|-------|--------|-------------|-------------------------|
| UMBRELA DNA | Julgar relevância de passagens | RI ad-hoc | Pointwise | Query + Passage | Score (0-3) | Graduada (0-3) | Sim | Absoluto |
| UMBRELA Basic | Julgar relevância de passagens | RI ad-hoc | Pointwise | Query + Passage | Score (0-3) | Graduada (0-3) | Sim | Absoluto |
| Criteria-Based 4prompts | Julgar relevância por critérios | RI ad-hoc | Pointwise | Query + Passage | Notas dos critérios + Score final | Graduada (0-3) | Sim | Absoluto |
| Criteria-Based sumdecompose | Julgar relevância por critérios | RI ad-hoc | Pointwise | Query + Passage | Notas dos critérios + Score final (soma) | Graduada (0-3) | Sim | Absoluto |
| Criteria-Based naiveBdecompose | Julgar relevância por critérios | RI ad-hoc | Pointwise | Query + Passage | Notas dos critérios + Score final (NB) | Graduada (0-3) | Sim | Absoluto |
| Criteria-Based COT | Julgar relevância com filtro binário | RI ad-hoc | Pointwise | Query + Passage | Score final (0-3) via árvore | Graduada (0-3) | Sim | Absoluto |
| Pointwise Legal simple | Julgar relevância jurídica (PT-BR) | RI ad-hoc (domínio legal) | Pointwise | Query + Documento legal | Score (0-2) em JSON | Graduada (0-2) | Sim | Absoluto |
| Pointwise Legal rationale | Julgar relevância jurídica com justificativa | RI ad-hoc (domínio legal) | Pointwise | Query + Documento legal | Rationale + Score (0-2) | Graduada (0-2) | Sim | Absoluto |
| JudgeBlender PromptBlender | Combinar múltiplos prompts | RI ad-hoc | Ensemble (Pointwise) | Query + Passage | Score consolidado (0-3) | Graduada (0-3) | Sim | Absoluto (agregado) |
| JudgeBlender LLMBlender | Combinar múltiplos modelos | RI ad-hoc | Ensemble (Pointwise) | Query + Passage | Score consolidado (0-3) | Graduada (0-3) | Sim | Absoluto (agregado) |
| RUBRIC Question | Avaliar answerability de respostas | RAG / Conteúdo | Pointwise (por pergunta) | Pergunta de teste + Passage | Answerability (0-5) | Graduada (0-5) → binária | Sim (via max grade) | Absoluto (derivado) |
| RUBRIC Nugget | Avaliar cobertura de fatos | RAG / Conteúdo | Nugget-based | Nugget + Passage | Answerability (0-5) | Graduada (0-5) → binária | Sim (via max grade) | Absoluto (derivado) |
| AutoNuggetizer | Avaliar recall de fatos em RAG | RAG / Conteúdo | Nugget-based (iterativo) | Resposta RAG + Nuggets | Suporte (support/partial/not_support) | Suporte ternário | Não | Relativo (recall) |
| One-Shot Labeling DuoPrompt | Preencher "holes" sob escassez | RI ad-hoc (estimativa) | Pairwise | Query + d⁺ + d? | Relevância relativa a d⁺ | Binária/relativa | Sim (estimado) | Relativo |
| One-Shot Labeling DuoT5 | Preencher "holes" sob escassez | RI ad-hoc (estimativa) | Pairwise | Query + d⁺ + d? | Relevância relativa a d⁺ | Binária/relativa | Sim (estimado) | Relativo |
| RankGPT PG | Re-ranquear passagens | Busca / Re-ranking | Listwise (Sliding Window) | Query + lote de passagens | Permutação ordenada | Ordinal relativa | Não | Relativo (ordem) |

---

### 3. Estratégia de Julgamento

| Método/Variante | Prompting | Rubrica/Critérios | Decomposition | Rationale | CoT/Reasoning | Nº Chamadas/Jul. | Agregação | Múltiplos Modelos? |
|-----------------|-----------|-------------------|---------------|-----------|---------------|------------------|-----------|---------------------|
| UMBRELA DNA | Zero-shot | Escala 0-3 | Não (instruções internas) | Não (saída sem justificativa) | Instrução interna (dividir em passos) | 1 | N/A | Não |
| UMBRELA Basic | Zero-shot | Escala 0-3 | Não | Não | Não | 1 | N/A | Não |
| Criteria-Based 4prompts | Zero-shot | 4 critérios (Exactness, Coverage, Topicality, Contextual Fit) | **Sim** (critérios independentes) | Não | Não | 4 (critérios) + 1 (agregação) | Prompt agregador | Não |
| Criteria-Based sumdecompose | Zero-shot | 4 critérios | **Sim** | Não | Não | 4 (critérios) | Soma simples | Não |
| Criteria-Based naiveBdecompose | Zero-shot | 4 critérios | **Sim** | Não | Não | 4 (critérios) | Naive Bayes | Não |
| Criteria-Based COT | Zero-shot | Subconjunto de critérios (depende da bifurcação) | **Sim** (bifurcação) | Não | Árvore de decisão (check binário) | 1 (check) + 2 (critérios) | Árvore | Não |
| Pointwise Legal simple | Zero-shot | Escala 0-2 | Não | Não | Não | 1 | N/A | Não |
| Pointwise Legal rationale | Zero-shot | Escala 0-2 | Não | **Sim** (justificativa prévia) | Não (rationale é verbal, não CoT) | 1 | N/A | Não |
| JudgeBlender PromptBlender | Multi-prompts (3) | Herdado dos prompts | Herdado | Herdado | Herdado | 3 | MV ou AV | Não (1 modelo, 3 prompts) |
| JudgeBlender LLMBlender | Multi-prompts (3) | Herdado dos prompts | Herdado | Herdado | Herdado | 3 | MV ou AV | **Sim** (3 modelos) |
| RUBRIC Question | Zero-shot | 10 perguntas geradas | **Sim** (consulta → perguntas) | Não | Não | 1 por pergunta | `max grade(r,p)` | Não |
| RUBRIC Nugget | Zero-shot | Nuggets extraídos | **Sim** (consulta → nuggets) | Não | Não | 1 por nugget | `max grade(r,p)` | Não |
| AutoNuggetizer | Zero-shot (iterativo) | Nuggets (vital/okay) | **Sim** (fatos atômicos) | Não | Não | Iterativo (lotes de 10) | Recall de fatos | Não |
| One-Shot Labeling DuoPrompt | Zero-shot | Comparação com d⁺ | Não | Não | Não | 1 por par | N/A | Não |
| One-Shot Labeling DuoT5 | Supervisionado | Comparação com d⁺ | Não | Não | Não | 1 por par | N/A | Não |
| RankGPT PG | Zero-shot | Ordinal | Não | Não | Não | 10 por query (sliding window) | Ordenação direta | Não |

---

### 4. Modelo e Execução

| Método/Variante | Modelo(s) Original | Tamanho | Aberto/Prop. | Execução | Temp/Params | Código | Prompt | Reprodutibilidade | Dependências |
|-----------------|--------------------|---------|--------------|----------|-------------|--------|--------|-------------------|--------------|
| UMBRELA DNA | GPT-4o [927]; DeepSeek V3, Llama 3.3 70B, Llama 3 8B, Flan-T5-large [221] | MoE ~1.8T (GPT-4o); 145B (DeepSeek); 70B; 8B; 783M | Prop. (GPT-4o); Aberto (demais) | API (GPT-4o/DeepSeek); Local (Llama/Flan) | Temp=0, Top_p=1, Freq_pen=0.5, Pres_pen=0 [927] | ✅ GitHub | ✅ Figura 1 | **Alta** (código, prompts, parâmetros) | OpenAI, Together AI, HF |
| UMBRELA Basic | Llama 3 8B [221] | 8B | Aberto | Local | Não informado | ✅ GitHub | ✅ Repositório | **Alta** | HF local |
| Criteria-Based 4prompts | Llama-3-8B-Instruct [188] | 8B | Aberto | Local | Não informado | ❌ | ✅ Tabelas 2,3,5 | **Média** (prompts doc, sem repositório) | HF local, scikit-learn |
| Criteria-Based sumdecompose | Llama-3-8B-Instruct [188] | 8B | Aberto | Local | Não informado | ❌ | ✅ Tabelas 2,3,5 | **Média** | HF local |
| Criteria-Based naiveBdecompose | Llama-3-8B-Instruct [188] | 8B | Aberto | Local | Não informado | ❌ | ✅ Tabelas 2,3,5 | **Média** | HF local, scikit-learn |
| Criteria-Based COT | Llama-3-8B-Instruct [188] | 8B | Aberto | Local | Não informado | ❌ | ✅ Tabelas 2,3,5 | **Média** | HF local |
| Pointwise Legal simple | DeepSeek-V3.2, gpt-5-mini, sabiazinho-4 [599] | 145B; NI; NI | Prop. (gpt-5-mini); Aberto (DeepSeek, sabiazinho) | API (DeepSeek, gpt); Together (sabiazinho) | Temp=0 (DeepSeek/sabiazinho); gpt-5-mini fixo [599] | ✅ HuggingFace | ✅ Figuras 8-11 | **Alta** | DeepSeek API, OpenAI API, Together AI |
| Pointwise Legal rationale | DeepSeek-V3.2, gpt-5-mini, sabiazinho-4 [599] | mesmo | mesmo | API | mesmo | ✅ HuggingFace | ✅ Figuras 8-11 | **Alta** | mesmo |
| JudgeBlender PromptBlender | Llama-3-8B-Instruct [338] | 8B | Aberto | Local | Temp=0 [338] | ✅ GitHub | ✅ Repositório | **Alta** | HF local |
| JudgeBlender LLMBlender | Mistral-7B, Gemma-7B, Llama-3-8B-Instruct [338] | 7B, 7B, 8B | Aberto | Local | Temp=0 | ✅ GitHub | ✅ Repositório | **Alta** | HF local |
| RUBRIC Question | GPT-3.5 (perguntas); Flan-T5-large (graduação) [741] | 175B (GPT-3.5); 783M (Flan) | Prop. (GPT-3.5); Aberto (Flan) | API (GPT-3.5); Local (Flan) | Padrão HF [741] | ✅ GitHub | ✅ Tabelas 1,2 | **Alta** | OpenAI API, HF local |
| RUBRIC Nugget | GPT-3.5 (nuggets); Flan-T5-large (graduação) [741] | mesmo | mesmo | mesmo | mesmo | ✅ GitHub | ✅ Tabelas 1,2 | **Alta** | OpenAI API, HF local |
| AutoNuggetizer | GPT-4o (Azure) [884] | MoE ~1.8T | Proprietário | API | Temp=0 [884] | ⚠️ Parcial | ✅ Figuras 1,2,3 | **Média** (orquestração complexa) | Azure OpenAI API |
| One-Shot Labeling DuoPrompt | Flan-T5-3B [697] | 3B | Aberto | Local | Não informado | ✅ PyPI (`autoqrels`) | ✅ Repositório | **Alta** | PyTorch, HF |
| One-Shot Labeling DuoT5 | DuoT5 (3B) [697] | 3B | Aberto | Local | Não informado | ✅ PyPI | ✅ Repositório | **Alta** | PyTorch, HF |
| RankGPT PG | GPT-4, gpt-3.5-turbo [266] | NI | Proprietário | API | Temp=0 [266] | ✅ GitHub | ✅ Apêndice A | **Alta** | OpenAI API |

---

### 5. Evidência Experimental (Benchmarks e Resultados)

| Método/Variante | Benchmark | Idioma | Domínio | Julgamentos Humanos? | Métricas Concordância | Resultado Concordância | Métricas Ranking | Resultado Ranking |
|-----------------|-----------|--------|---------|-----------------------|----------------------|------------------------|------------------|-------------------|
| UMBRELA DNA (GPT-4o) | TREC DL 2019-2023 [927] | Inglês | Web/Passagens | Sim (NIST) | Cohen's κ (4-pt), κ (binarizado) | κ 0,31-0,37; κ_bin 0,42-0,50 [927] | Kendall's τ; Spearman's ρ | τ 0,87-0,94; ρ 0,97-0,99 [927] |
| UMBRELA DNA (DeepSeek V3) | TREC DL 2023 [221] | Inglês | Web/Passagens | Sim (NIST) | Cohen's κ (4-pt), κ (binarizado) | κ 0,262; κ_bin 0,371 [221] | Kendall's τ; Spearman's ρ | τ 0,929; ρ 0,989 [221] |
| UMBRELA DNA (Llama-3-8B) | TREC DL 2023 [221] | Inglês | Web/Passagens | Sim (NIST) | Cohen's κ (4-pt), κ (binarizado) | κ 0,187; κ_bin 0,315 [221] | Kendall's τ; Spearman's ρ | τ 0,931; ρ 0,989 [221] |
| Criteria-Based 4prompts | LLMJudge / TREC DL 2023 [188] | Inglês | Web/Passagens | Sim | Cohen's κ; Krippendorff's α | κ 0,1829; α 0,2888 [188] | Kendall's τ | τ 0,9483 [188] |
| Criteria-Based sumdecompose | LLMJudge / TREC DL 2023 [188] | Inglês | Web/Passagens | Sim | Cohen's κ; Krippendorff's α | κ 0,2088; α 0,3926 [188] | Kendall's τ | τ 0,9300 [188] |
| Criteria-Based naiveBdecompose | LLMJudge / TREC DL 2023 [188] | Inglês | Web/Passagens | Sim | Cohen's κ; Krippendorff's α | κ 0,1741; α 0,3579 [188] | Kendall's τ | τ 0,9128 [188] |
| Criteria-Based COT | LLMJudge / TREC DL 2023 [188] | Inglês | Web/Passagens | Sim | Cohen's κ; Krippendorff's α | κ 0,1961; α 0,3852 [188] | Kendall's τ | τ 0,8956 [188] |
| Pointwise Legal simple | NormasTCU [599] | Português-BR | Jurídico (normas TCU) | Sim (4 especialistas) | MAE | MAE 0,46 (DeepSeek V3) [599] | Kendall's τ (nDCG@10, MRR) | τ ≥ 0,90 [599] |
| Pointwise Legal rationale | NormasTCU [599] | Português-BR | Jurídico (normas TCU) | Sim (4 especialistas) | MAE; Cohen's κ | MAE 0,46-0,66; κ 0,32-0,53 [599] | Kendall's τ (nDCG@10, MRR) | τ ≥ 0,90; P@10/R@10 τ ≤ 0,85 [599] |
| JudgeBlender LLMBlender + MV(Avg.) | LLMJudge / TREC DL 2023 [338] | Inglês | Web/Passagens | Sim | Cohen's κ; Krippendorff's α | κ 0,2553; α 0,4832 [338] | Kendall's τ; Spearman's ρ | τ 0,9612; ρ 0,9940 [338] |
| JudgeBlender PromptBlender + MV(Avg.) | LLMJudge / TREC DL 2023 [338] | Inglês | Web/Passagens | Sim | Cohen's κ; Krippendorff's α | κ 0,2398; α 0,4769 [338] | Kendall's τ; Spearman's ρ | τ 0,9526; ρ 0,9919 [338] |
| RUBRIC Question | TREC DL 2019, 2020, TREC CAR Y3 [741] | Inglês | Web/Passagens, Conhecimento | Sim | Spearman's ρ; Cohen's κ (bin.) | ρ 0,974 (DL20); 0,961 (DL19); 0,931 (CAR); κ_bin 0,25 [741] | — | — |
| One-Shot Labeling DuoPrompt | TREC DL 2019, 2020, 2021 [697] | Inglês | Web/Passagens | Sim | F1 (binário) | F1 ≤ 0,55 [697] | Kendall's τ | τ 0,87-0,92 [697] |
| One-Shot Labeling DuoT5 | TREC DL 2019, 2020, 2021 [697] | Inglês | Web/Passagens | Sim | F1 (binário) | F1 ≤ 0,59 [697] | Kendall's τ | τ 0,87-0,92 [697] |
| RankGPT PG (GPT-4) | TREC DL 2019, BEIR, Mr.TyDi, NovelEval [266] | Inglês (e multilíngue) | Diversos | Sim | nDCG@10 | 75,59 (DL19); +2,3 sobre SOTA (BEIR) [266] | — | — |

---

### 6. Eficiência

| Método/Variante | Custo Informado | Unidade | Latência Informada | Unidade | Nº Inferências | Execução Local? |
|-----------------|-----------------|---------|---------------------|---------|----------------|-----------------|
| UMBRELA DNA (GPT-3.5) | ~$0.01 [806] | por julgamento | **Não informado para UMBRELA** | — | 1 por par | Não (API) |
| UMBRELA DNA (GPT-4o) | Não informado | — | **Não informado** | — | 1 por par | Não (API) |
| UMBRELA DNA (DeepSeek V3) | Não informado | — | **Não informado** | — | 1 por par | Não (API) |
| UMBRELA DNA (Llama-3-8B) | Não informado (computacional) | — | **Não informado** | — | 1 por par | Sim (HF local) |
| Criteria-Based (todas) | Não informado | — | **Não informado** | — | 4 por par (critérios) + 1 (agregação) | Sim (HF local) |
| Pointwise Legal | Não informado (API) | — | **Não informado** | — | 1 por par | Não (API) |
| JudgeBlender LLMBlender | Não informado (computacional) | — | **Não informado** | — | 3 por par | Sim (HF local) |
| JudgeBlender PromptBlender | Não informado (computacional) | — | **Não informado** | — | 3 por par | Sim (HF local) |
| RUBRIC | Não informado | — | ~1h para coleção inteira [741] | hora | 1 por pergunta (10 perguntas) + agregação | Sim (Flan local) |
| AutoNuggetizer | Não informado | — | **Não informado** | — | Iterativo (lotes) | Não (API) |
| One-Shot Labeling | Não informado (computacional) | — | **Não informado** | — | 1 por par | Sim (HF local) |
| RankGPT PG (GPT-4) | $0,596 [266] | por 10 requisições | ~3,2s por chamada [266] | segundos | 10 por query | Não (API) |
| RankGPT PG (gpt-3.5-turbo) | $0,040 [266] | por 10 requisições | ~1,1s por chamada [266] | segundos | 10 por query | Não (API) |

> **Observação crítica sobre latência:** Os valores de 1,1s e 3,2s reportados na tabela acima são **específicos do RankGPT** [266] e foram medidos no contexto da API OpenAI para aquela tarefa. **Não há latência reportada para UMBRELA** em nenhum dos artigos analisados. Atribuir esses valores ao UMBRELA seria uma extrapolação incorreta.

---

### 7. Análise para o PIBIT

| Método/Variante | Principais Vantagens | Principais Limitações | Trade-off Principal | Adequação ao Experimento Principal | Comparável com | Adaptações Necessárias | Prioridade | Observações |
|-----------------|----------------------|------------------------|---------------------|-----------------------------------|----------------|------------------------|------------|-------------|
| UMBRELA DNA (Llama-3-8B) | Baseline consolidada, código aberto, formato de saída estrito, amplamente validado | Viés de superestimação, baixa concordância per-label, sensível a paráfrases | Qualidade de ranking vs. concordância per-label | **Sim** — baseline pointwise | Criteria-Based (mesmo LLM) | Reimplementar com Llama-3-8B (originalmente GPT-4o) | **A** | Resultados com GPT-4o não se aplicam diretamente à reimplementação |
| Criteria-Based sumdecompose | Melhor equilíbrio per-label/ranking, explicabilidade, auditável | 4 chamadas por par, sem repositório público | Custo vs. qualidade | **Sim** — testa hipótese da decomposição | UMBRELA (mesmo LLM) | Nenhuma (já usa Llama-3-8B) | **A** | κ=0,21 e α=0,39 são os melhores per-label entre os métodos núcleo |
| JudgeBlender LLMBlender | Melhor κ per-label, mitiga vieses, modelos locais | 3 chamadas por par, complexidade de engenharia | Robustez vs. complexidade | **Não como concorrente — como condição adicional** | Ensemble sobre UMBRELA + Criteria | Aplicar sobre saídas de métodos base (pós-processamento) | **B** | Não deve ser tratado como método independente no mesmo nível |
| Pointwise Legal rationale | Único validado em Português, domínio jurídico, rationale aumenta estabilidade | Domínio específico, dependência de API | Generalização vs. especificidade | **Sim — experimento complementar** | UMBRELA (mesmo benchmark NormasTCU) | Nenhuma | **B** | MAE 0,46-0,66; κ 0,32-0,53 |
| RUBRIC Question | Reutilizável, não requer qrels manuais, excelente para RAG, human-in-the-loop | Não é avaliação de relevância clássica; extração de texto menos confiável | Conteúdo vs. relevância | **Não no principal** (constructo diferente) | Não comparável diretamente com métodos núcleo | N/A | **C** | Deve ser usado em experimento secundário sobre RAG |
| One-Shot Labeling DuoPrompt | Funciona com extrema escassez, reduz falsos positivos | F1 ≤ 0,55-0,59 — inadequado para recall | Escassez vs. completude | **Não no principal** (caso de uso específico) | Não aplicável | N/A | **C** | Útil para cold start, não para qrels completos |
| RankGPT PG | Alta correlação de ranking, listwise direto | Não gera qrels, sensível à ordem inicial | Ranking vs. qrels | **Não** (fora do escopo) | Não aplicável | N/A | **C** | Método de re-ranking, não de avaliação |

---

## COMPARAÇÕES EXPERIMENTALMENTE VÁLIDAS

| Comparação | Pergunta Científica | Variável Independente | Variáveis Controladas | Variável Dependente | Benchmark | Modelo | Escala | Condição de Controle | Hipótese | Principal Ameaça |
|------------|---------------------|-----------------------|----------------------|---------------------|-----------|--------|--------|----------------------|----------|------------------|
| **UMBRELA DNA vs. Criteria-Based sumdecompose** | A decomposição em critérios melhora a correlação de ranking (τ) em comparação com o julgamento pointwise direto? | Estrutura do prompt (direto vs. multicritério) | Mesmo LLM (Llama-3-8B), mesmo benchmark (LLMJudge/TREC DL 2023), mesma escala (0-3), mesmas consultas/documentos | Kendall's τ, Cohen's κ, Krippendorff's α | LLMJudge / TREC DL 2023 | Llama-3-8B | 0-3 | Ambos os métodos devem ser executados com o mesmo modelo e no mesmo conjunto de pares | A decomposição produz τ ≥ 0,93 (conforme reportado) e κ/α superiores ao UMBRELA com o mesmo LLM | A reimplementação do UMBRELA com Llama-3-8B pode não reproduzir os resultados originais com GPT-4o |
| **UMBRELA com diferentes LLMs** | O DeepSeek V3 é equivalente ao GPT-4o para avaliação de relevância com o prompt UMBRELA? | LLM utilizado (GPT-4o vs. DeepSeek V3 vs. Llama-3-8B) | Mesmo prompt (UMBRELA DNA), mesmo benchmark (TREC DL 2023), mesma escala (0-3) | τ, κ | TREC DL 2023 | GPT-4o, DeepSeek V3, Llama-3-8B | 0-3 | Mesmo prompt, mesmos parâmetros de inferência (Temp=0) | DeepSeek V3 apresenta τ e κ equivalentes ao GPT-4o (conforme reportado em [221]) | APIs proprietárias podem mudar; custos variam |
| **Método Base vs. Ensemble (Wrapper)** | O ensemble das saídas de múltiplos métodos/prompts reduz o viés de superestimação e melhora a concordância per-label? | Número de componentes no ensemble (1 vs. 3) | Mesmos modelos base (Llama-3-8B), mesmo benchmark, mesma escala | κ, distribuição de labels | LLMJudge | Llama-3-8B (base), Mistral-7B, Gemma-7B (para LLMBlender) | 0-3 | Executar os métodos base individualmente e depois aplicar agregação sobre suas saídas | O ensemble produz κ ≥ 0,255 (conforme reportado para LLMBlender) e reduz o número de superestimativas | O ensemble não deve ser confundido com método independente; é uma condição aplicada sobre saídas já geradas |

---

## COMPARAÇÕES QUE DEVEM SER EVITADAS

| Comparação | Motivo da Invalidade | Reformulação para Tornar Válida |
|------------|----------------------|---------------------------------|
| **UMBRELA vs. RUBRIC** | RUBRIC avalia *answerability* (conteúdo/RAG), não relevância ad-hoc. Constructos diferentes. | Utilizar RUBRIC em experimento separado sobre avaliação de RAG, não como concorrente de métodos de relevância. |
| **UMBRELA vs. RankGPT** | UMBRELA gera qrels absolutos; RankGPT gera rankings relativos (re-ranking). Tarefas diferentes. | Se quiser comparar, usar RankGPT para gerar rankings e comparar a correlação dos rankings com humanos, não a qualidade dos qrels. |
| **κ de um método vs. τ de outro** | κ mede concordância per-label; τ mede correlação de rankings de sistemas. São métricas de constructos diferentes. | Comparar κ com κ, τ com τ, sempre no mesmo benchmark e com os mesmos modelos. |
| **Métodos avaliados em benchmarks diferentes** | Ex: UMBRELA no TREC DL vs. Pointwise Legal no NormasTCU. Consultas, documentos, idioma e domínio diferem. | Somente comparar métodos no mesmo benchmark (ex: todos no LLMJudge/TREC DL 2023). |
| **Métodos executados com modelos diferentes** | Ex: UMBRELA (GPT-4o) vs. Criteria-Based (Llama-3-8B). A diferença pode ser devida ao modelo, não ao método. | Reimplementar ambos com o mesmo LLM (Llama-3-8B) para isolar a estrutura do método. |
| **JudgeBlender vs. métodos base** | JudgeBlender é um *wrapper* que combina os próprios métodos base. Comparar como concorrente é circular. | Tratar JudgeBlender como **condição experimental adicional** (ensemble) aplicada sobre os métodos base. |

---

## SHORTLIST PARA O PIBIT

### Prioridade A — Experimento Principal (Implementação Obrigatória)

| Método | Justificativa |
|--------|---------------|
| **1. UMBRELA — DNA (com Llama-3-8B)** | Baseline pointwise mais consolidada da literatura. Código aberto, reprodutível. Permite comparar a estrutura pointwise direta com a abordagem multicritério. *Adaptação necessária*: reimplementar com Llama-3-8B para isolar o efeito do método. |
| **2. Criteria-Based — sumdecompose (com Llama-3-8B)** | Melhor equilíbrio entre concordância per-label (α=0,39) e correlação de ranking (τ=0,93). Testa a hipótese central da decomposição em critérios. *Adaptação necessária*: nenhuma (já usa Llama-3-8B). |

**Por que esses dois?** Ambos geram qrels absolutos, usam escala 0-3, podem ser executados no mesmo benchmark (LLMJudge/TREC DL 2023) e, com o mesmo LLM, permitem isolar a *estrutura do prompt* como variável independente.

---

### Prioridade B — Experimento Complementar (Implementação Desejável)

| Método | Justificativa |
|--------|---------------|
| **3. Ensemble (LLMBlender + MV(Avg.)) sobre os dois anteriores** | Testa se a combinação das saídas reduz viés e melhora concordância per-label. Não é um método concorrente, mas uma condição experimental adicional. *Adaptação necessária*: pós-processamento sobre os qrels gerados. |
| **4. Pointwise Legal — rationale (com DeepSeek V3)** | Único método validado em Português e domínio jurídico. Permite avaliar generalização para o contexto do TCU/NormasTCU. *Adaptação necessária*: API, não local. |

---

### Prioridade C — Fundamentação / Trabalho Relacionado (Não Implementar no Experimento Principal)

| Método | Justificativa |
|--------|---------------|
| **RUBRIC (Question)** | Avalia *answerability* (RAG/conteúdo), não relevância ad-hoc. Constructo diferente. Pode ser usado em experimento secundário sobre RAG, mas não no núcleo do PIBIT. |
| **RankGPT (Permutation Generation)** | Método de re-ranking, não gera qrels. Fora do escopo direto do PIBIT (avaliação de relevância). |
| **One-Shot Labeling (DuoPrompt/DuoT5)** | Método para cenários de extrema escassez, não para geração de qrels completos. Caso de uso específico. |
| **AutoNuggetizer** | Avaliação de RAG por fatos. Fora do escopo de relevância ad-hoc. |

---

## MATRIZ FINAL DE DECISÃO — CANDIDATOS DO EXPERIMENTO PRINCIPAL

| Método | Estratégia | Modelo Controlado | Gera Qrels | Chamadas/Jul. | Concordância Humana (κ/α) | Ranking de Sistemas (τ/ρ) | Custo | Latência | Robustez | Reprodutibilidade | Complexidade | Papel no Experimento |
|--------|------------|-------------------|------------|---------------|---------------------------|---------------------------|-------|----------|----------|------------------|--------------|----------------------|
| **UMBRELA DNA** (adaptado) | Pointwise direto | Llama-3-8B | Sim | 1 | κ 0,19 (com Llama-8B); α NI | τ 0,93 (com Llama-8B); ρ 0,99 | Não informado (computacional) | Não informado | Moderada (varia com prompt) | Alta | Baixa | **Baseline** — referência pointwise direta |
| **Criteria-Based sumdecompose** | Pointwise multicritério | Llama-3-8B | Sim | 4 | κ 0,21; α 0,39 | τ 0,93 | Não informado (computacional) | Não informado | Moderada | Média | Média | **Hipótese** — testa se decomposição melhora qualidade |

---

## Observações Finais

- Todos os valores de concordância e ranking reportados são **específicos das variantes e modelos indicados**, conforme os artigos originais.
- A comparação entre UMBRELA (adaptado para Llama-3-8B) e Criteria-Based (já com Llama-3-8B) é **metodologicamente válida** porque isola a estrutura do método como variável independente.
- Os valores de κ, α, τ e ρ não devem ser comparados entre si — são métricas de constructos diferentes.
- A ausência de dados de custo e latência para a maioria dos métodos (especialmente os locais) é uma **lacuna que o PIBIT pode ajudar a preencher** com medições experimentais.