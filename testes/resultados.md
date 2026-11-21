# Resultados dos testes

Gerado por `python3 testes/rodar_testes.py`. Não editar à mão.

## Autômato de pilha (AP)

| ID | Entrada | Tam. | Esperado | Obtido | Regra verificada |
|---|---|---|---|---|---|
| AP-A1 | `o,a,x,y&osrO,A,X,Y&O.` | 21 | ACEITA | ACEITA | 5 sujeitos e 5 predicativos, pontuação correta (cenário 1) |
| AP-A2 | `o,a,x,y&osrO,A,O,Y&O.` | 21 | ACEITA | ACEITA | Estrutura correta; o AP não verifica a classe (cenário 3) |
| AP-A3 | `a,a,a,a&asrA,A,A,A&A.` | 21 | ACEITA | ACEITA | Todos os itens da mesma classe |
| AP-A4 | `y,x,a,o&ysrY,X,A,O&Y.` | 21 | ACEITA | ACEITA | Classes em outra ordem, contagem igual |
| AP-A5 | `o,o,o,o,o&osrO,O,O,O,O&O.` | 25 | ACEITA | ACEITA | n = 6: a pilha cresce até 6 S |
| AP-A6 | `x,y,x,y,x&ysrX,Y,X,Y,X&Y.` | 25 | ACEITA | ACEITA | n = 6 só com plurais |
| AP-A7 | `o,a,x,y,o,a&xsrO,A,X,Y,O,A&X.` | 29 | ACEITA | ACEITA | n = 7 |
| AP-A8 | `a,o,y,x&osrO,O,O,O&O.` | 21 | ACEITA | ACEITA | Nenhuma concordância, mas a contagem bate: o AP aceita |
| AP-A9 | `o&asrO&A.` | 9 | ACEITA | ACEITA | Caso-limite: menor cadeia aceita (n = 2) |
| AP-R1 | `o,a,x,y&osrO,A,X&Y.` | 19 | REJEITA | REJEITA | Falta um predicativo: '.' com S no topo (cenário 2) |
| AP-R2 | `o,a,x&ysrO,A,X,Y,O&A.` | 21 | REJEITA | REJEITA | Predicativos a mais: ',' com Z₀ no topo em q7 |
| AP-R3 | `o,a,x,y,osrO,A,X,Y,O.` | 21 | REJEITA | REJEITA | Falta o '&' antes do último item |
| AP-R4 | `o,a,x,y&orsO,A,X,Y&O.` | 21 | REJEITA | REJEITA | 'r' antes de 's' |
| AP-R5 | `o,a,,x,y&osrO,A,X,Y&O.` | 22 | REJEITA | REJEITA | Duas vírgulas seguidas |
| AP-R6 | `o,a,x,y&osrO,A,X,Y&O` | 20 | REJEITA | REJEITA | Sem o ponto final: termina em q10, não final |
| AP-R7 | `O,A,X,Y&OsrO,A,X,Y&O.` | 21 | REJEITA | REJEITA | Predicativos no lugar dos sujeitos |
| AP-R8 | `o,a,x,y&osrO,A,X,Y&O..` | 22 | REJEITA | REJEITA | Símbolo depois do ponto final |
| AP-R9 | (vazia) | 0 | REJEITA | REJEITA | Caso-limite: entrada vazia (termina em q0) |

## Autômato linearmente limitado (ALL)

| ID | Entrada | Tam. | Esperado | Obtido | Regra verificada |
|---|---|---|---|---|---|
| ALL-A1 | `oaxyoaxyoOAXYOAXYO` | 18 | ACEITA | ACEITA | 9 pares, todos concordam |
| ALL-A2 | `ooooooooooOOOOOOOOOO` | 20 | ACEITA | ACEITA | 10 pares masculino singular |
| ALL-A3 | `aaaaaaaaaAAAAAAAAA` | 18 | ACEITA | ACEITA | 9 pares feminino singular |
| ALL-A4 | `xyxyxyxyxXYXYXYXYX` | 18 | ACEITA | ACEITA | Só plurais, alternando gênero |
| ALL-A5 | `yxayoxyaoYXAYOXYAO` | 18 | ACEITA | ACEITA | Classes misturadas, concordância cruzada |
| ALL-A6 | `oaxyoaxyoaOAXYOAXYOA` | 20 | ACEITA | ACEITA | 10 pares |
| ALL-A7 | `xxxyyyaaaXXXYYYAAA` | 18 | ACEITA | ACEITA | Blocos de mesma classe |
| ALL-A8 | `oyoyoyoyoOYOYOYOYO` | 18 | ACEITA | ACEITA | Alterna masculino singular e feminino plural |
| ALL-A9 | `oO` | 2 | ACEITA | ACEITA | Caso-limite: menor cadeia aceita (1 par) |
| ALL-R1 | `oaxyoaxyoOAXYOAXYA` | 18 | REJEITA | REJEITA | Último par discorda em gênero (o × A) |
| ALL-R2 | `oaxyoaxyoOAOYOAXYO` | 18 | REJEITA | REJEITA | 3º par discorda em número (x × O) |
| ALL-R3 | `oaxyoaxyoaOAXYOAXYO` | 19 | REJEITA | REJEITA | Sobra um sujeito (10 × 9) |
| ALL-R4 | `oaxyoaxyoOAXYOAXYOO` | 19 | REJEITA | REJEITA | Sobra um predicativo (9 × 10) |
| ALL-R5 | `oaxyoaxyoOAXYOAXYOa` | 19 | REJEITA | REJEITA | Sujeito depois dos predicativos |
| ALL-R6 | `OAXYOAXYOoaxyoaxyo` | 18 | REJEITA | REJEITA | Começa por predicativo |
| ALL-R7 | `oaxyoaxyoaxyoaxyoa` | 18 | REJEITA | REJEITA | Só sujeitos, nenhum predicativo |
| ALL-R8 | `oaxyoaxyoOYXAOYXAO` | 18 | REJEITA | REJEITA | Ordem aninhada (espelhada) em vez de cruzada: o 2º par falha |
| ALL-R9 | (vazia) | 0 | REJEITA | REJEITA | Caso-limite: entrada vazia |

## Fluxo completo (AP → ALL)

| ID | Entrada | Tam. | Esperado | Obtido | Regra verificada |
|---|---|---|---|---|---|
| INT-1 | `o,a,x,y&osrO,A,X,Y&O.` | 21 | ACEITA/ACEITA | ACEITA/ACEITA | Estrutura e concordância corretas |
| INT-2 | `o,a,x,y&osrO,A,X&Y.` | 19 | REJEITA/— | REJEITA/— | 5 sujeitos e 4 predicativos: o ALL não executa |
| INT-3 | `o,a,x,y&osrO,A,O,Y&O.` | 21 | ACEITA/REJEITA | ACEITA/REJEITA | Estrutura correta, 3º par discorda em número (os meninos … médico) |

## Símbolo fora do alfabeto

| ID | Entrada | Tam. | Esperado | Obtido | Regra verificada |
|---|---|---|---|---|---|
| ERR-1 | `o,a,x,b&osrO,A,X,Y&O.` | 21 | ERRO | ERRO | Símbolo 'b' fora do alfabeto do AP |
| ERR-2 | `oaxyoaxyo,OAXYOAXYO` | 19 | ERRO | ERRO | Vírgula fora do alfabeto do ALL |

### Mensagens de erro exibidas

- **ERR-1**: `Erro: o símbolo 'b' (posição 7) não pertence ao alfabeto de entrada {o, a, x, y, O, A, X, Y, ,, &, s, r, .}.`
- **ERR-2**: `Erro: o símbolo ',' (posição 10) não pertence ao alfabeto de entrada {o, a, x, y, O, A, X, Y}.`

## Conferência com as definições de L1 e L2

Todas as cadeias de comprimento ≤ 7 sobre {o,O,`,`,&,s,r,.} (AP) e ≤ 6 sobre o alfabeto do ALL: **ok (1260393 cadeias)**.
