# Etapa 2 — Gramática livre de contexto (GLC) de L1

## Linguagem

C = {`o`, `a`, `x`, `y`} (sujeitos) e P = {`O`, `A`, `X`, `Y`} (predicativos).

L1 = { c₁,c₂,…,cₙ₋₁&cₙ `sr` p₁,p₂,…,pₙ₋₁&pₙ `.` | cᵢ ∈ C, pᵢ ∈ P, n ≥ 2 }

**Alfabeto:** Σ = {`o`, `a`, `x`, `y`, `O`, `A`, `X`, `Y`, `,`, `&`, `s`, `r`, `.`}

**Regra de formação:** uma lista de n ≥ 2 sujeitos, com vírgula entre os itens e `&` antes do último; depois `s` ("são") e `r` ("respectivamente"); depois uma lista de **n** predicativos com a mesma pontuação; por fim `.`. As classes dos itens são livres em L1: a concordância fica com o ALL.

## Gramática

G = (V, Σ, R, S)

- **Não terminais:** V = {S, L, C, P}
- **Terminais:** Σ (acima)
- **Símbolo inicial:** S
- **Produções (R):**

```
(1) S → L & P .
(2) L → C , L , P
(3) L → C & C s r P
(4) C → o      (5) C → a      (6) C → x      (7) C → y
(8) P → O      (9) P → A      (10) P → X     (11) P → Y
```

| Não terminal | Significado |
|---|---|
| S | a frase inteira |
| L | o "miolo": todos os sujeitos, `sr` e todos os predicativos menos o último |
| C | um sujeito (uma das 4 classes) |
| P | um predicativo (uma das 4 classes) |

## Por que G gera exatamente L1

**Contagem.** Cada aplicação de (2) gera **um** C e **um** P. A produção (3) gera dois C e um P, e (1) gera mais um P. Com k aplicações de (2), a frase tem k + 2 sujeitos e k + 2 predicativos. Assim n = k + 2 ≥ 2, e as duas listas têm sempre o mesmo tamanho.

**Pontuação.** Por indução em k, L gera exatamente as cadeias

  c₁,…,cₖ₊₁&cₖ₊₂ `sr` p₁,…,pₖ₊₁

- **k = 0:** a produção (3) dá `c₁&c₂srp₁`. ✓
- **Passo:** (2) coloca `c ,` à esquerda e `, p` à direita de uma cadeia gerada por L com k − 1. A lista de sujeitos ganha um item no começo, com vírgula, e a lista de predicativos ganha um no fim, também com vírgula. ✓

A produção (1) completa com `&pₙ.`, que é o último predicativo depois do `&`. Logo L(G) ⊆ L1. Para a inclusão contrária, toda cadeia de L1 com n itens é derivada aplicando (2) n − 2 vezes, depois (3), e escolhendo as classes com (4)–(11). Logo L(G) = L1.

**Observação para a arguição.** Na produção (2), o sujeito e o predicativo gerados **juntos** são o 1º sujeito e o **penúltimo** predicativo, ou seja, um par aninhado, de fora para dentro. A GLC consegue garantir que as quantidades batem, mas os pares que ela forma são aninhados, não cruzados. Por isso a concordância "1º com 1º, 2º com 2º" fica fora do alcance dela e vai para o ALL.

## Derivação de uma cadeia aceita

Cadeia do cenário 1 (aceita pelo AP e pelo ALL): `o,a,x,y&osrO,A,X,Y&O.` (n = 5, então k = 3 aplicações de (2)).

Derivação mais à esquerda:

| Passo | Forma sentencial | Produção |
|---|---|---|
| 0 | S | |
| 1 | L&P. | (1) |
| 2 | C,L,P&P. | (2) |
| 3 | o,L,P&P. | (4) |
| 4 | o,C,L,P,P&P. | (2) |
| 5 | o,a,L,P,P&P. | (5) |
| 6 | o,a,C,L,P,P,P&P. | (2) |
| 7 | o,a,x,L,P,P,P&P. | (6) |
| 8 | o,a,x,C&CsrP,P,P,P&P. | (3) |
| 9 | o,a,x,y&CsrP,P,P,P&P. | (7) |
| 10 | o,a,x,y&osrP,P,P,P&P. | (4) |
| 11 | o,a,x,y&osrO,P,P,P&P. | (8) |
| 12 | o,a,x,y&osrO,A,P,P&P. | (9) |
| 13 | o,a,x,y&osrO,A,X,P&P. | (10) |
| 14 | o,a,x,y&osrO,A,X,Y&P. | (11) |
| 15 | o,a,x,y&osrO,A,X,Y&O. | (8) |

Árvore de derivação (resumida):

```
S
├── L
│   ├── C → o
│   ├── ,
│   ├── L
│   │   ├── C → a
│   │   ├── ,
│   │   ├── L
│   │   │   ├── C → x
│   │   │   ├── ,
│   │   │   ├── L
│   │   │   │   ├── C → y
│   │   │   │   ├── &
│   │   │   │   ├── C → o
│   │   │   │   ├── s
│   │   │   │   ├── r
│   │   │   │   └── P → O
│   │   │   ├── ,
│   │   │   └── P → A
│   │   ├── ,
│   │   └── P → X
│   ├── ,
│   └── P → Y
├── &
├── P → O
└── .
```

A árvore mostra o aninhamento: `o` (1º sujeito) e `Y` (4º predicativo) nascem da mesma produção. Na árvore, os pares de concordância corretos (o↔O, a↔A, x↔X, y↔Y, o↔O) nunca saem do mesmo nó.

## L1 não é regular (lema do bombeamento)

Duas propriedades de toda cadeia de L1:
- **(P1)** o número de símbolos de C é igual ao número de símbolos de P;
- **(P2)** não há dois símbolos de C seguidos (entre dois sujeitos sempre há `,` ou `&`).

**Prova.** Suponha que L1 seja regular, com comprimento de bombeamento p. Tome

  w = (o,)ᵖ o&o sr (O,)ᵖ O&O.

Então w ∈ L1 (n = p + 2) e |w| ≥ p. Pelo lema, w = xyz com |xy| ≤ p, |y| ≥ 1 e xyⁱz ∈ L1 para todo i ≥ 0. Como |xy| ≤ p, y está dentro do prefixo (o,)ᵖ e só contém `o` e `,`. Tome i = 0:

- **Caso 1, y contém algum `o`:** xz tem menos sujeitos e o mesmo número de predicativos. Isso viola (P1), então xz ∉ L1.
- **Caso 2, y não contém `o`:** como não há duas vírgulas seguidas em (o,)ᵖ, y = `,`. Ao removê-la, dois `o` ficam colados em xz. Isso viola (P2), então xz ∉ L1.

Nos dois casos há contradição, logo **L1 não é regular**. ∎

Intuição para a apresentação: para conferir se há tantos predicativos quanto sujeitos, é preciso lembrar um número ilimitado (n). Um autômato finito tem memória fixa; o AP resolve isso com a pilha.
