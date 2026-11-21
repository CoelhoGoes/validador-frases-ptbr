# Validador de frases com "respectivamente" — AP + ALL

Trabalho prático de Linguagens Formais e Autômatos: reconhecimento de linguagens com pilha e fita limitada.

**Equipe:** _(nomes completos)_ — turma _(CC6MA / CC6NA)_

## O problema

Em frases como

> *O João, a Maria, os meninos, as meninas e o Pedro são, respectivamente, médico, advogada, engenheiros, professoras e músico.*

o i-ésimo predicativo concorda em gênero e número com o i-ésimo sujeito. O validador verifica essas frases em duas etapas:

1. **Autômato de pilha (AP):** verifica a estrutura (pontuação das listas e tantos predicativos quanto sujeitos). A linguagem é livre de contexto e não é regular.
2. **Autômato linearmente limitado (ALL):** verifica a concordância **cruzada** (1º com 1º, 2º com 2º…). A linguagem é sensível ao contexto e não é livre de contexto. O ALL só executa se o AP aceitar.

### Codificação (um símbolo por palavra)

| Classe | Sujeito | Predicativo |
|---|---|---|
| masculino singular | `o` | `O` |
| feminino singular | `a` | `A` |
| masculino plural | `x` | `X` |
| feminino plural | `y` | `Y` |

`,` = vírgula · `&` = "e" antes do último item · `s` = "são" · `r` = "respectivamente" · `.` = fim

A frase acima vira `o,a,x,y&osrO,A,X,Y&O.`

## Instalação

Requer **Python 3.8 ou mais recente** (testado com 3.12). Não há dependências externas: o `requirements.txt` está vazio de propósito.

```bash
git clone <url-do-repositório>
cd <pasta-do-repositório>
python3 --version
```

## Execução

Fluxo completo (AP e depois ALL):

```bash
python3 validador.py "o,a,x,y&osrO,A,X,Y&O."
```

Com o rastreamento passo a passo (AP: estado, posição e pilha; ALL: estado, fita e cabeçote):

```bash
python3 validador.py --rastro "o,a,x,y&osrO,A,O,Y&O."
```

Só um dos módulos:

```bash
python3 validador.py --modulo ap "o&asrO&A."
```

```bash
python3 validador.py --modulo all "oaxyoOAXYO"
```

Use sempre aspas em volta da cadeia, porque o `&` tem significado especial no shell.

**Códigos de saída:** 0 = aceita, 1 = rejeita, 2 = símbolo fora do alfabeto.

### Os três cenários de integração

```bash
python3 validador.py "o,a,x,y&osrO,A,X,Y&O."
```
→ AP aceita, ALL aceita.

```bash
python3 validador.py "o,a,x,y&osrO,A,X&Y."
```
→ AP rejeita (5 sujeitos e 4 predicativos); o ALL não executa.

```bash
python3 validador.py "o,a,x,y&osrO,A,O,Y&O."
```
→ AP aceita, ALL rejeita (*os meninos … médico*: erro de número).

## Testes

```bash
python3 testes/rodar_testes.py
```

O script roda os 41 casos de [`testes/casos.csv`](testes/casos.csv): 9 aceitas e 9 rejeitadas para cada módulo, incluindo os casos-limite; os 3 cenários de integração; e 2 entradas com símbolo fora do alfabeto. Ele também:
- confere as exigências da lauda (quantidade de casos, cadeias distintas, alfabeto do módulo, 18 símbolos ou mais fora dos casos-limite);
- compara os dois autômatos com as definições formais de L1 e L2 em todas as cadeias curtas (cerca de 1,26 milhão);
- gera as tabelas com entrada, decisão esperada, decisão obtida e regra verificada em [`testes/resultados.md`](testes/resultados.md) e `testes/resultados.tex` (para o relatório).

Termina com código 0 se tudo passar.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `automato_pilha.py` | AP: tabela de transições e simulador com rastreamento |
| `automato_linear.py` | ALL: tabela de transições e simulador com rastreamento |
| `validador.py` | linha de comando, verificação do alfabeto e integração AP → ALL |
| `testes/` | casos de teste (dados de exemplo), script de testes e resultados gerados |
| `docs/etapa-1-problema.md` | problema, linguagens e fundamentação |
| `docs/etapa-2-glc.md` | GLC, derivação e prova de que L1 não é regular |
| `docs/etapa-3-ap.md` | especificação formal do AP |
| `docs/etapa-4-all.md` | especificação formal do ALL e prova de que L2 não é livre de contexto |
| `docs/rastreamentos/` | rastreamentos completos do ALL |
| `ETAPAS.md` | plano de desenvolvimento |

## Origem do material

- **Código, autômatos, gramática e casos de teste:** elaborados para este trabalho; não foram adaptados de exercícios de sala nem de código de terceiros.
- **Ideia do problema:** adaptada do argumento de dependências cruzadas de Shieber (1985) e do argumento com "respectivamente" de Bar-Hillel e Shamir (1960), discutido por Pullum e Gazdar (1982). As referências completas estão em [`docs/etapa-1-problema.md`](docs/etapa-1-problema.md).
- **Teoria (lemas do bombeamento, AP, ALL):** Sipser, *Introdução à Teoria da Computação*; Hopcroft, Motwani e Ullman, *Introduction to Automata Theory, Languages, and Computation*; Kuroda (1964).

## Uso de inteligência artificial

**Ferramenta:** Claude Code (Anthropic), modelo Claude Opus 5.5.

**Tarefas apoiadas:**
- divisão do trabalho em etapas;
- proposta do problema e das duas linguagens;
- rascunho da GLC, das especificações do AP e do ALL e das provas;
- implementação dos simuladores e da linha de comando;
- elaboração dos casos de teste e do script de testes;
- redação deste README.

**O que a equipe verificou:** _(preencher: por exemplo, quem simulou à mão quais rastreamentos, quem conferiu as provas, quais referências foram conferidas na fonte, o que foi alterado)_
