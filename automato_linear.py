
SUJEITOS = "oaxy"
PREDICATIVOS = "OAXY"
ALFABETO = SUJEITOS + PREDICATIVOS
ESQ, DIR = "<", ">"
ESTADO_INICIAL, ACEITA = "q0", "q_ac"
CARREGA = {"o": "q6", "a": "q7", "x": "q8", "y": "q9"}
CLASSE = {q: c for c, q in CARREGA.items()}


def _tabela():
    d = {("q0", ESQ): ("q1", ESQ, "R")}
    for c in SUJEITOS:
        d["q1", c] = ("q2", c, "R")
        d["q2", c] = ("q2", c, "R")
        d["q5", c] = (CARREGA[c], "*", "R")
    for p in PREDICATIVOS:
        d["q2", p] = ("q3", p, "R")
        d["q3", p] = ("q3", p, "R")
    d["q3", DIR] = ("q4", DIR, "L")
    for s in ALFABETO + "*+":
        d["q4", s] = ("q4", s, "L")
    d["q4", ESQ] = ("q5", ESQ, "R")
    d["q5", "*"] = ("q5", "*", "R")
    d["q5", "+"] = ("q10", "+", "R")
    for c, q in CARREGA.items():
        for s in SUJEITOS + "+":
            d[q, s] = (q, s, "R")
        d[q, c.upper()] = ("q4", "+", "L")
    d["q10", "+"] = ("q10", "+", "R")
    d["q10", DIR] = (ACEITA, DIR, "L")
    return d


TRANSICOES = _tabela()


def _motivo(estado, simbolo):
    if estado == "q1":
        return "não há sujeitos"
    if estado == "q2":
        return "não há predicativos"
    if estado == "q3":
        return "sujeito depois de predicativo"
    if estado in CLASSE and simbolo == DIR:
        return f"sobrou o sujeito '{CLASSE[estado]}' sem predicativo"
    if estado in CLASSE:
        return f"falta de concordância: sujeito '{CLASSE[estado]}' com predicativo '{simbolo}'"
    if estado == "q10":
        return f"sobrou o predicativo '{simbolo}' sem sujeito"
    return "configuração inesperada"


def executar(w):
    fita, cabeca, estado, rastro = [ESQ, *w, DIR], 0, ESTADO_INICIAL, []
    while estado != ACEITA:
        rastro.append((estado, "".join(fita), cabeca))
        t = TRANSICOES.get((estado, fita[cabeca]))
        if t is None:
            motivo = _motivo(estado, fita[cabeca])
            return False, rastro, f"δ({estado}, '{fita[cabeca]}') não está definida: {motivo}"
        estado, fita[cabeca], mov = t
        cabeca += 1 if mov == "R" else -1
        assert 0 <= cabeca < len(fita), "o cabeçote saiu da fita"
    rastro.append((estado, "".join(fita), cabeca))
    return True, rastro, "todos os sujeitos e predicativos pareados"
