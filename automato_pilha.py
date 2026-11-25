
SUJEITOS = "oaxy"
PREDICATIVOS = "OAXY"
ALFABETO = SUJEITOS + PREDICATIVOS + ",&sr."
Z0 = "Z₀"
ESTADO_INICIAL = "q0"
FINAIS = {"q11"}


def _tabela():
    d = {}
    for c in SUJEITOS:
        d["q0", c, Z0] = ("q1", ("S", Z0))
        d["q2", c, "S"] = ("q1", ("S", "S"))
        d["q3", c, "S"] = ("q4", ("S", "S"))
    for p in PREDICATIVOS:
        d["q6", p, "S"] = ("q7", ())
        d["q8", p, "S"] = ("q7", ())
        d["q9", p, "S"] = ("q10", ())
    d["q1", ",", "S"] = ("q2", ("S",))
    d["q1", "&", "S"] = ("q3", ("S",))
    d["q4", "s", "S"] = ("q5", ("S",))
    d["q5", "r", "S"] = ("q6", ("S",))
    d["q7", ",", "S"] = ("q8", ("S",))
    d["q7", "&", "S"] = ("q9", ("S",))
    d["q10", ".", Z0] = ("q11", (Z0,))
    return d


TRANSICOES = _tabela()


def executar(w):
    estado, pilha, rastro = ESTADO_INICIAL, [Z0], []
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
