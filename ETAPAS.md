# Plano de etapas — Trabalho prático de LFA (AP + ALL)

> **Prazo apertado:** hoje é 20/11/2026. Entrega e apresentação em **25/11 (CC6NA)** ou **27/11 (CC6MA)**.
> O cronograma abaixo considera 25/11. Se a turma for a CC6MA, os dois dias a mais servem de folga para o ensaio.

---

## Etapa 0 — Organização (20/11)
- [ ] Fechar a equipe (1 a 4 pessoas, mesma turma) e confirmar a turma/data.
- [ ] Criar o repositório no GitHub e dar acesso ao professor.
- [ ] Dividir as partes técnicas: **cada integrante vai apresentar e defender uma parte** (ex.: GLC+derivação / AP / ALL / implementação+testes).

## Etapa 1 — Escolha do problema e das linguagens (20–21/11)
O problema precisa ser **diferente do exemplo da lauda** (parênteses + `#` + R/V/E) e dos exercícios de sala.

- [ ] Escolher um problema com contexto real (validador de algum tipo de registro/mensagem).
- [ ] **L1 (AP):** linguagem livre de contexto **não regular** (ex.: aninhamento/balanceamento, `aⁿbⁿ`, palíndromos com marcador).
- [ ] **L2 (ALL):** linguagem sensível ao contexto **não livre de contexto** (ex.: `aⁿbⁿcⁿ`, `w#w` — cópia, `aⁿbᵐcⁿdᵐ`).
- [ ] Definir como a entrada é dividida entre os módulos (o ALL recebe que parte?).
- [ ] Verificar que os dois autômatos vão ter **no mínimo 8 estados cada** — a linguagem precisa ter fases suficientes para isso de forma natural, sem estados artificiais.
- [ ] Verificar que dá para montar cadeias com **18+ caracteres**.

Ideias de problema (só ponto de partida):
- *Pacote com checksum de cópia*: o AP valida um cabeçalho com dois tipos de delimitadores aninhados (`{[()]}`) seguido de `#`; o ALL verifica que o corpo tem a forma `w$w` (o dado repetido de forma idêntica).
- *Ordem de produção*: o AP valida blocos aninhados de etapas; o ALL verifica `aⁿbᵐcⁿdᵐ` (pedidos casam com entregas e insumos casam com consumos, em pares cruzados).

## Etapa 2 — Modelagem formal da GLC (21/11)
- [ ] Alfabeto, regra de formação, GLC completa: terminais, não terminais, símbolo inicial, produções.
- [ ] **Derivação** passo a passo de uma cadeia aceita (é a que vai ser mostrada na apresentação).
- [ ] Prova de que L1 **não é regular**: lema do bombeamento para linguagens regulares, aplicado à linguagem do projeto (ou referência técnica: Sipser / Hopcroft-Ullman).

## Etapa 3 — Especificação do AP (21–22/11)
- [ ] Estados (≥ 8), alfabeto de entrada, alfabeto da pilha, configuração inicial (estado inicial + símbolo de fundo da pilha).
- [ ] Tabela de transições `δ(q, a, X) → (p, γ)`.
- [ ] Critério de aceitação: **estado final ou pilha vazia** (escolher um e declarar), sempre com a entrada consumida por inteiro.
- [ ] Diagrama do AP.
- [ ] **Justificativa de que o AP reconhece L(GLC)**: relacionar as produções às operações de empilhar/desempilhar (ou à construção GLC → AP).
- [ ] Declarar se o AP é determinístico. Se não for, decidir como o simulador explora as alternativas.

## Etapa 4 — Especificação do ALL (22/11)
- [ ] Estados (≥ 8), alfabeto de entrada, alfabeto da fita (inclui os símbolos de marcação, ex.: `X`, `Y`, `Z`), configuração inicial.
- [ ] Fita: **n células graváveis + 2 marcadores de borda fixos** (`<` e `>`). O cabeçote lê os marcadores, nunca os sobrescreve e nunca passa deles.
- [ ] Tabela de transições `δ(q, a) → (p, b, L/R)`.
- [ ] Condições de aceitação e de rejeição (incluir rejeição por falta de transição).
- [ ] Diagrama do ALL.
- [ ] Prova de que L2 **não é livre de contexto**: lema do bombeamento para LLC (ou referência), e argumento de que é sensível ao contexto (o próprio ALL / uma gramática sensível ao contexto).

## Etapa 5 — Implementação (22–23/11)
Sugestão: **Python + CLI** (simples de rodar ao vivo e de reproduzir). As transições ficam como **tabelas de dados**, e o simulador só executa a tabela. A decisão tem que sair da execução das transições, não de um `if` contando símbolos.

Feito: `automato_pilha.py` (AP), `automato_linear.py` (ALL), `validador.py` (CLI + integração).

- [x] Validação do alfabeto: símbolo fora do alfabeto → mensagem de erro clara (vai ser registrada nos testes).
- [x] Simulador do AP com rastreamento passo a passo: **estado, posição de leitura, conteúdo da pilha**.
- [x] Simulador do ALL com rastreamento: **estado, fita inteira, posição do cabeçote**.
- [x] Fluxo integrado: AP → (se aceitar) ALL. Se o AP rejeitar, o ALL não executa.
- [x] Modos de uso: rodar uma cadeia com rastreamento (`--rastro`) e rodar só um módulo (`--modulo ap|all`).
- [x] Argumento de **terminação** (nas Etapas 3 e 4) (vai para o relatório): AP — cada passo consome símbolo ou o número de transições ε é limitado; ALL — fita finita, número finito de configurações e/ou cada varredura marca uma célula. Se houver não determinismo, explicar a exploração (ex.: busca em largura sobre configurações com conjunto de visitados).

## Etapa 6 — Testes (23/11)
- [ ] **AP:** ≥ 8 aceitas + ≥ 8 rejeitadas, todas distintas e com o alfabeto do módulo, incluindo ≥ 1 caso-limite (vazia ou a menor aceita).
- [ ] **ALL:** a mesma coisa.
- [ ] **Integração:** (1) aceita pelos dois; (2) rejeitada pelo AP; (3) aceita pelo AP e rejeitada pelo ALL.
- [ ] Teste com **símbolo fora do alfabeto**, registrando a mensagem exibida.
- [ ] Cada teste registra: **entrada, decisão esperada, decisão obtida, regra verificada**. Os testes ficam num arquivo de dados (CSV/JSON) e um script roda tudo e gera a tabela, que vai pronta para o relatório.
- [ ] Anotar **uma limitação observada** (é pedida no fim da apresentação).

Feito: casos em `testes/casos.csv` (9+9 no AP, 9+9 no ALL, 3 de integração, 2 de alfabeto); `python3 testes/rodar_testes.py` roda tudo, confere as exigências da lauda e gera `testes/resultados.md` e `testes/resultados.tex`.

Limitações observadas (candidatas para o fim da apresentação):
- O ALL faz O(n²) passos: 14 passos para 2 símbolos, 114 para 10, 1.344 para 40 e 7.854 para 100. Ele vai e volta na fita para cada par, porque só leva uma classe no estado por vez.
- O AP aceita frases sem nenhuma concordância (AP-A8), já que ele só conta. A divisão em dois módulos é obrigatória, não um detalhe de implementação.
- A entrada é codificada em símbolos: o programa não lê a frase em português por extenso.

> ⚠️ A lauda diz que "as cadeias selecionadas devem possuir 18 caracteres (no mínimo)", mas também pede caso-limite (entrada vazia / comprimento mínimo). **Confirmar com o professor** se os casos-limite ficam fora da regra dos 18. Na dúvida: todas as cadeias principais com 18+ e os casos-limite marcados à parte.

## Etapa 7 — Repositório e README (23–24/11)
Feito: `README.md`, `requirements.txt` (vazio: sem dependências) e `.gitignore`. Pendente: nomes da equipe, "o que a equipe verificou" na seção de IA, criar o repositório no GitHub e dar acesso ao professor.

- [ ] Código-fonte, dependências (`requirements.txt`, mesmo que vazio), dados de exemplo e arquivos de teste.
- [ ] README: como instalar, como executar e como repetir os testes (comandos prontos para copiar).
- [ ] Origem do código, dos diagramas e dos exemplos adaptados.
- [ ] **Declaração de uso de IA**: ferramenta, tarefas em que ajudou e o que a equipe verificou (este planejamento conta).

## Etapa 8 — Relatório técnico em LaTeX → PDF (24/11)
Feito: `relatorio/relatorio.tex` + `relatorio/tabela-testes.tex` (gerada pelos testes). Compilar no Overleaf subindo a pasta `relatorio/` inteira (pdfLaTeX). Pendente: nomes, contribuições, "o que a equipe verificou" e conferir a compilação. Diagramas com TikZ (pacote `automata`); tabelas de teste geradas pelo script da Etapa 6.

Seções:
1. Problema e contexto
2. Fontes consultadas
3. GLC + derivação + prova de que não é regular
4. Especificação do AP + justificativa GLC ↔ AP
5. LSC + prova de que não é LLC + especificação do ALL + limite da fita
6. Implementação: linguagem, interface, terminação, não determinismo
7. Testes (tabelas) e análise dos resultados, incluindo a limitação observada
8. Uso de IA e origem do material
9. Contribuição de cada integrante

## Etapa 9 — Slides e ensaio (24/11 + manhã de 25/11)
- [ ] Slides (até 15 min): problema → GLC/derivação → AP → ALL e dependência → demo → limitação.
- [ ] Demo ao vivo dos **3 cenários de integração**, com ≥ 1 rastreamento de cada autômato explicado (como a pilha e a fita levam à decisão).
- [ ] Cada integrante apresenta uma parte técnica.
- [ ] **Preparação para a arguição (vale 1,20 dos 3,0 pontos):** todos precisam conseguir explicar a relação GLC ↔ AP, justificar a regra do ALL e o limite da fita, e **prever à mão** a decisão para uma cadeia nova. Treinar: um propõe uma cadeia, o outro simula no papel e depois confere no programa.

## Etapa 10 — Entrega (25/11, antes da aula)
- [ ] Um integrante anexa no Classroom: relatório PDF, slides (PDF/PPTX), link do GitHub e nomes completos da equipe.
- [ ] Os outros registram a entrega com o mesmo link e dizem quem enviou os arquivos.
- [ ] Conferir se o professor tem acesso ao repositório.

---

## Onde vai a nota
| Critério | Pontos | Etapas |
|---|---|---|
| Domínio técnico individual (arguição) | 1,20 | 2–4, 9 |
| Apresentação e demonstração | 0,90 | 9 |
| Pesquisa e modelagem formal | 0,40 | 1–4 |
| Implementação e testes | 0,30 | 5–6 |
| Documentação, código e reprodutibilidade | 0,20 | 7–8 |

Conclusão: **70% da nota depende de cada um entender os autômatos**. A modelagem (etapas 1–4) é o caminho crítico, porque implementação, testes e slides dependem dela.
