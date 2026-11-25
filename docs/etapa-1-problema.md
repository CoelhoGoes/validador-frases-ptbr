# Etapa 1 — Problema e linguagens (proposta)

## Problema: validador de frases com "respectivamente"

Em português, a construção com *respectivamente* liga os itens de duas listas **pela posição**: o 1º sujeito corresponde ao 1º predicativo, o 2º ao 2º, e assim por diante. Cada predicativo concorda em **gênero e número** com o seu sujeito.

> *O João, a Maria, os meninos, as meninas e o Pedro são, respectivamente, médico, advogada, engenheiros, professoras e músico.*

O validador verifica essas frases em duas etapas:

| Módulo | O que verifica | Classe |
|---|---|---|
| **AP** | A estrutura da frase: listas com vírgulas e "e" antes do último item, pelo menos 2 itens e **tantos predicativos quanto sujeitos** | Livre de contexto, não regular |
| **ALL** | A **concordância cruzada**: o i-ésimo predicativo concorda em gênero e número com o i-ésimo sujeito | Sensível ao contexto, não livre de contexto |

### Fundamentação
- **Por que não é livre de contexto:** dependências cruzadas (o 1º item liga ao 1º, o 2º ao 2º…) são o exemplo clássico de estrutura que não é livre de contexto. Shieber (1985) usou esse fato para mostrar que o alemão suíço não é livre de contexto.
- **O argumento com "respectivamente" tem histórico.** Bar-Hillel e Shamir (1960) o usaram para o inglês, e Pullum e Gazdar (1982) o contestaram, porque em inglês a correspondência é só de sentido: os adjetivos não mudam de forma. Em português, gênero e número ficam marcados na própria palavra (*médico* / *advogada* / *engenheiros*), então a dependência pode ser verificada na cadeia.
- **O que vale no trabalho:** a classificação é da **linguagem formal definida pela equipe** e se prova pelos lemas do bombeamento, sem depender de o português inteiro ser ou não livre de contexto. O relatório deve deixar essa distinção clara.

## Alfabeto (um caractere por palavra ou expressão)

Cada sujeito e cada predicativo cai em uma de 4 **classes de concordância**:

| Classe | Sujeito | Predicativo | Exemplo |
|---|---|---|---|
| masculino singular | `o` | `O` | o João … médico |
| feminino singular | `a` | `A` | a Maria … advogada |
| masculino plural | `x` | `X` | os meninos … engenheiros |
| feminino plural | `y` | `Y` | as meninas … professoras |

Minúscula = sujeito; maiúscula = predicativo da mesma classe.

| Símbolo | Papel |
|---|---|
| `,` | vírgula entre itens |
| `&` | o "e" antes do último item |
| `s` | "são" |
| `r` | "respectivamente" |
| `.` | fim da frase |

A frase do exemplo vira `o,a,x,y&osrO,A,X,Y&O.`

Formato: lista de sujeitos `s` `r` lista de predicativos `.`, em que cada lista é `item(,item)*&item`.

## L1 — linguagem do AP (livre de contexto, não regular)

Sejam C = {o,a,x,y} (sujeitos) e P = {O,A,X,Y} (predicativos).

L1 = { c₁,c₂,…,cₙ₋₁&cₙ `sr` p₁,p₂,…,pₙ₋₁&pₙ `.` | cᵢ ∈ C, pᵢ ∈ P, **n ≥ 2** }

O AP empilha um símbolo `S` por sujeito e desempilha um por predicativo. Ele **não olha a classe**: verifica só a pontuação, a ordem das partes e a quantidade.

- **Não regular:** L1 ∩ `(o,)*o&osr(O,)*O&O.` = { `(o,)ᵏo&osr(O,)ᵏO&O.` | k ≥ 0 }. Essa linguagem tem a forma aᵏbᵏ, que não é regular. Como as linguagens regulares são fechadas sob interseção, L1 também não é regular. A prova formal com o lema do bombeamento fica para a Etapa 2.

**Esboço do AP (12 estados, determinístico, aceitação por estado final com a entrada toda consumida):**

| Estado | Papel |
|---|---|
| q0 | espera o 1º sujeito (empilha `S`) |
| q1 | depois de um sujeito que não é o último: `,` → q2, `&` → q3 |
| q2 | depois da vírgula: espera um sujeito (empilha) → q1 |
| q3 | depois do `&`: espera o último sujeito (empilha) → q4 |
| q4 | espera `s` |
| q5 | espera `r` |
| q6 | espera o 1º predicativo (desempilha) |
| q7 | depois de um predicativo: `,` → q8, `&` → q9 |
| q8 | depois da vírgula: espera um predicativo (desempilha) → q7 |
| q9 | depois do `&`: espera o último predicativo (desempilha) → q10 |
| q10 | espera `.` com `Z₀` no topo, isto é, todos os sujeitos foram pareados |
| q11 | **final** |

Os casos de rejeição saem das transições que faltam. Se houver predicativos demais, não há como desempilhar com `Z₀` no topo. Se faltarem predicativos, o `.` chega com `S` no topo. A exigência de n ≥ 2 vem do próprio caminho: só se chega a q4 passando pelo `&`.

## L2 — linguagem do ALL (sensível ao contexto, não livre de contexto)

O ALL recebe só a sequência de classes, sem a pontuação: os sujeitos seguidos dos predicativos. Para o exemplo, a entrada é `oaxyoOAXYO`. O programa faz essa extração depois que o AP aceita, do mesmo jeito que o exemplo da lauda passa ao ALL o trecho após `#`.

L2 = { w · h(w) | w ∈ C⁺ }, onde h(o)=O, h(a)=A, h(x)=X, h(y)=Y

- **Não livre de contexto:** L2 ∩ o⁺a⁺O⁺A⁺ = { oⁱ aʲ Oⁱ Aʲ | i, j ≥ 1 }. Essa linguagem não é livre de contexto (lema do bombeamento para LLC; é a mesma estrutura cruzada de Shieber). Como as LLC são fechadas sob interseção com regulares, L2 também não é LLC.
- **Sensível ao contexto:** é reconhecida por um ALL, e as linguagens sensíveis ao contexto são exatamente as reconhecidas por ALLs (Kuroda, 1964).

**Fita:** `<` + n células + `>`. Alfabeto da fita: Γ = C ∪ P ∪ {`*`, `+`, `<`, `>`}, em que `*` marca um sujeito já pareado e `+` marca um predicativo já pareado.

**Esboço do ALL (11 estados de trabalho + 1 de aceitação; versão final na [Etapa 4](etapa-4-all.md)):**

| Estado | Papel |
|---|---|
| q0 | no `<`, move para a direita |
| q1 | exige ao menos um sujeito |
| q2 | lê sujeitos até o 1º predicativo (se chegar ao `>`, rejeita) |
| q3 | lê predicativos até o `>`. Se aparecer um sujeito aqui, rejeita (ordem errada) |
| q4 | volta ao `<` (usado depois do formato e depois de cada pareamento) |
| q5 | pula os `*` e marca o sujeito seguinte com `*`, indo para o estado de "carregar" a sua classe. Se encontrar `+`, todos os sujeitos foram pareados → q10 |
| q6 | carrega **o**: procura o 1º predicativo não marcado. Se for `O`, marca `+`; se não, rejeita |
| q7 | carrega **a**: o mesmo, exigindo `A` |
| q8 | carrega **x**: o mesmo, exigindo `X` |
| q9 | carrega **y**: o mesmo, exigindo `Y` |
| q10 | verificação final: só pode haver `+` até o `>` |
| q_ac | aceitação (a rejeição acontece quando falta a transição; não há estado próprio) |

As fases são duas: q0–q3 conferem o formato (sujeitos e depois predicativos) e q5–q10 fazem o pareamento, com q4 voltando ao início entre uma coisa e outra. Cada classe precisa do seu próprio estado de "carregar", porque o estado é a única memória que o cabeçote leva de um lado da fita para o outro. É por isso que incluir o número aumentou o ALL.

**Terminação:** cada volta do laço q5 → q6..q9 → q4 → q5 marca duas células, e a fita tem n células, então há no máximo n/2 voltas, cada uma com O(n) movimentos. Os demais estados só andam em uma direção até um marcador de borda.

## Cadeias dos três cenários de integração (todas com 18+ caracteres)

O comprimento de uma frase com n itens é 4n + 1, então n ≥ 5 garante pelo menos 18 caracteres.

| Cenário | Entrada | AP | ALL | Motivo |
|---|---|---|---|---|
| Aceita pelos dois | `o,a,x,y&osrO,A,X,Y&O.` (21) | aceita | aceita | 5 sujeitos, 5 predicativos, todos concordam |
| Rejeitada pelo AP | `o,a,x,y&osrO,A,X&Y.` (19) | rejeita | — | 5 sujeitos e 4 predicativos |
| AP aceita, ALL rejeita | `o,a,x,y&osrO,A,O,Y&O.` (21) | aceita | rejeita | 3º par: *os meninos … médico* (`x` × `O`), erro de **número** |

**Casos-limite:**
- AP: a menor frase aceita é `o&asrO&A.` (9 caracteres).
- ALL: a menor cadeia aceita é `oO`. Para os testes do ALL isolado com 18+ caracteres, use |w| ≥ 9 (ex.: `oaxyoaxyoOAXYOAXYO`).

## Referências
- BAR-HILLEL, Y.; SHAMIR, E. Finite-state languages: formal representations and adequacy problems. *Bulletin of the Research Council of Israel*, v. 8F, p. 155–166, 1960. Reimpresso em BAR-HILLEL, Y. *Language and Information*. Addison-Wesley, 1964.
- PULLUM, G. K.; GAZDAR, G. Natural languages and context-free languages. *Linguistics and Philosophy*, v. 4, n. 4, p. 471–504, 1982.
- SHIEBER, S. M. Evidence against the context-freeness of natural language. *Linguistics and Philosophy*, v. 8, n. 3, p. 333–343, 1985.
- KURODA, S.-Y. Classes of languages and linear-bounded automata. *Information and Control*, v. 7, n. 2, p. 207–223, 1964.
- SIPSER, M. *Introdução à Teoria da Computação*. 2. ed. Cengage, 2007.
- HOPCROFT, J. E.; MOTWANI, R.; ULLMAN, J. D. *Introduction to Automata Theory, Languages, and Computation*. 3. ed. Pearson, 2006.

> Conferir as páginas e edições das referências na fonte antes de colocá-las no relatório.

## Em aberto
- [ ] A equipe aprova o problema?
- [ ] Confirmar com o professor a regra dos 18 caracteres × casos-limite.
