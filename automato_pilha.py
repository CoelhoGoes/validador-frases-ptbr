"""Autômato de pilha (AP) que reconhece L1 — especificação em docs/etapa-3-ap.md.

L1: c1,c2,...,c(n-1)&cn sr p1,p2,...,p(n-1)&pn .   com n >= 2
Determinístico, sem transições ε, aceitação por estado final (q11)
com a entrada inteira consumida.
"""

SUJEITOS = "oaxy"
PREDICATIVOS = "OAXY"
ALFABETO = SUJEITOS + PREDICATIVOS + ",&sr."
Z0 = "Z₀"
ESTADO_INICIAL = "q0"
FINAIS = {"q11"}


def _tabela():
    """δ(estado, lê, topo) = (novo estado, símbolos que substituem o topo — o 1º fica no topo)."""
    d = {}
    for c in SUJEITOS:
        d["q0", c, Z0] = ("q1", ("S", Z0))     # 1º sujeito: empilha
        d["q2", c, "S"] = ("q1", ("S", "S"))   # sujeito após vírgula: empilha
        d["q3", c, "S"] = ("q4", ("S", "S"))   # último sujeito: empilha
    for p in PREDICATIVOS:
        d["q6", p, "S"] = ("q7", ())           # 1º predicativo: desempilha
        d["q8", p, "S"] = ("q7", ())           # predicativo após vírgula: desempilha
        d["q9", p, "S"] = ("q10", ())          # último predicativo: desempilha
    d["q1", ",", "S"] = ("q2", ("S",))
    d["q1", "&", "S"] = ("q3", ("S",))
    d["q4", "s", "S"] = ("q5", ("S",))         # "são"
    d["q5", "r", "S"] = ("q6", ("S",))         # "respectivamente"
    d["q7", ",", "S"] = ("q8", ("S",))
    d["q7", "&", "S"] = ("q9", ("S",))
    d["q10", ".", Z0] = ("q11", (Z0,))         # fim: todos os sujeitos pareados
    return d


TRANSICOES = _tabela()


def executar(w):
    """Executa o AP sobre w.

    Retorna (aceita, rastro, motivo). Cada linha do rastro é
    (estado, posição de leitura a partir de 1, símbolo lido ou None no fim, pilha com o topo à esquerda),
    sempre a configuração ANTES do passo.
    """
    estado, pilha, rastro = ESTADO_INICIAL, [Z0], []   # pilha: topo no fim da lista
    for i, simbolo in enumerate(w):
        rastro.append((estado, i + 1, simbolo, "".join(reversed(pilha))))
        t = TRANSICOES.get((estado, simbolo, pilha[-1]))
        if t is None:
            return False, rastro, f"δ({estado}, '{simbolo}', {pilha[-1]}) não está definida"
        estado, escreve = t
        pilha[-1:] = reversed(escreve)
    rastro.append((estado, len(w) + 1, None, "".join(reversed(pilha))))
    if estado in FINAIS:
        return True, rastro, f"entrada consumida e {estado} é final"
    return False, rastro, f"entrada consumida, mas {estado} não é final"
