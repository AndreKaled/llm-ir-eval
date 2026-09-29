# LLM-IR-Evaluation

Estudo comparativo de métodos baseados em Grandes Modelos de Linguagem (LLMs) para avaliação automática de resultados de sistemas de Recuperação de Informação (RI).

## Sobre

Este projeto investiga e compara métodos de avaliação automática baseados em Grandes Modelos de Linguagem para avaliar resultados de sistemas de Recuperação de Informação.

O estudo concentra-se nos *trade-offs* práticos entre qualidade da avaliação, correlação com julgamentos humanos, custo, latência e robustez, buscando identificar as vantagens, limitações e características relevantes de cada método.

## Docs
[Matriz comparativa de métodos](docs/methods.md)

## Objetivos

* Levantar sistematicamente métodos de avaliação automática baseados em LLMs publicados a partir de 2020;
* Catalogar métricas e características relevantes para a comparação dos métodos, incluindo correlação com julgamentos humanos, custo e latência;
* Selecionar métodos representativos das principais abordagens, como pontuação direta, comparação pareada, critérios gerados e raciocínio em cadeia;
* Implementar os métodos selecionados em Python, utilizando uma interface unificada;
* Avaliar os métodos sobre *benchmarks* de Recuperação de Informação, como TREC, BEIR e MS MARCO;
* Conduzir um estudo experimental analisando a qualidade, o custo, a latência e a robustez dos métodos;
* Publicar o código e os dados experimentais no GitHub sob licença aberta;
* Elaborar considerações práticas sobre as vantagens, limitações e adequação de cada método a diferentes cenários.

## Abordagens de avaliação

O estudo considera abordagens como:

* Pontuação direta;
* Comparação pareada (*pairwise*);
* Critérios gerados;
* Raciocínio em cadeia (*chain-of-thought*).

## Status

Pesquisa em andamento.

Atualmente, o projeto encontra-se na etapa de revisão da literatura e identificação de métodos de avaliação candidatos para estudo e implementação.

## Estrutura do repositório

```text
src/          # Implementação dos métodos e componentes do projeto
experiments/  # Configurações, scripts e resultados dos experimentos
data/         # Documentação dos conjuntos de dados e instruções de aquisição
docs/         # Documentação e materiais relacionados à pesquisa
```
