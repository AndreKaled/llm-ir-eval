Execução com o modelo openai/gpt-oss-120b (via Groq, temperature 0), prompt oficial do UMBRELA, sobre 385 pares (query, passagem) julgados do TREC DL 2019:

[dataset](https://huggingface.co/datasets/orionweller/llm-based-expansions-eval-datasets)

| Métrica | Valor |
|---|---|
| Julgamentos válidos |	385 / 385 (invalid_rate = 0) | 
| Cohen κ (4 escalas) |	0.128 |
| Cohen κ quadrático |	0.281 |
|Cohen κ binário (≥2 = relevante) |	0.341 |
|MAE |	0.77 |
|Viés (LLM − humano) |	−0.005 |
|Chamadas por julgamento |	1.00 |
|Latência média |	3.76 s |
|Latência mediana |	3.93 s |
|Tokens de entrada (total) | 165.872 |
|Tokens de saída (total) |	51.842 |

Comparação com o paper original (Upadhyay et al., 2024, GPT-4o, DL 2019 completo):

| Métrica |	Este experimento (gpt-oss-120b) | UMBRELA (GPT-4o) |
|---|---|---|
| κ 4-escalas |	0.128 | 0.3613 |
| κ binário (≥2) | 0.341 | 0.4989 |

O κ menor é esperado e motivou a escolha do modelo: o gpt-oss-120b, embora tenha 120B parâmetros totais, ativa ~5B por token (arquitetura MoE) e não é um modelo frontier como o GPT-4o. Esse resultado dialoga diretamente com o eixo custo/qualidade investigado por Farzi & Dietz (2025, Does UMBRELA Work on Other LLMs?), que reporta degradação do UMBRELA com modelos menores que GPT-4o/DeepSeek V3.

O viés ≈ 0 com n=385 contrasta com o viés negativo observado em n=100, ilustrando que amostras pequenas não são conclusivas para esse tipo de métrica.

Limitações conhecidas
Amostra parcial: 385 julgamentos de 4.102 disponíveis no DL 2019 (subconjunto julgado). Não cobre todos os tracks do paper (DL 2019–2023).

Modelo diferente do paper original: os números não são diretamente comparáveis aos de GPT-4o.

Sem avaliação em nível de sistema: falta a etapa de correlação (Kendall τ / Spearman ρ) entre rankings de sistemas pontuados com julgamentos humanos vs. julgamentos LLM — o analyze ainda não implementa isso (ver # TODO em src/run.py).

Rate limit do Groq (free tier): 200.000 tokens/dia para gpt-oss-120b, equivalente a ~350–400 julgamentos diários. A execução completa dos 4.102 pares do DL 2019 exigiria ~11 dias no free tier, ou upgrade para Dev Tier.