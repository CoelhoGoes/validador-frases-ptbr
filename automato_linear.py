"""Autômato linearmente limitado (ALL) que reconhece L2 — especificação em docs/etapa-4-all.md.

L2 = { w h(w) | w ∈ {o,a,x,y}+ },  h(o)=O, h(a)=A, h(x)=X, h(y)=Y
Fita: '<' + n células + '>'. Os marcadores nunca são sobrescritos e o
cabeçote nunca sai deles. Determinístico.
"""

SUJEITOS = "oaxy"
PREDICATIVOS = "OAXY"
ALFABETO = SUJEITOS + PREDICATIVOS
ESQ, DIR = "<", ">"
ESTADO_INICIAL, ACEITA = "q0", "q_ac"
CARREGA = {"o": "q6", "a": "q7", "x": "q8", "y": "q9"}   # estado que "leva" a classe do sujeito
CLASSE = {q: c for c, q in CARREGA.items()}


def _tabela():
    """δ(estado, lê) = (novo estado, escreve, movimento)."""
    d = {("q0", ESQ): ("q1", ESQ, "R")}
    for c in SUJEITOS:
        d["q1", c] = ("q2", c, "R")                      # exige um sujeito
        d["q2", c] = ("q2", c, "R")
        d["q5", c] = (CARREGA[c], "*", "R")              # marca o sujeito e carrega a classe
    for p in PREDICATIVOS:
        d["q2", p] = ("q3", p, "R")
        d["q3", p] = ("q3", p, "R")
    d["q3", DIR] = ("q4", DIR, "L")                      # formato ok
    for s in ALFABETO + "*+":
        d["q4", s] = ("q4", s, "L")                      # volta ao '<'
    d["q4", ESQ] = ("q5", ESQ, "R")
    d["q5", "*"] = ("q5", "*", "R")
    d["q5", "+"] = ("q10", "+", "R")                     # acabaram os sujeitos
    for c, q in CARREGA.items():
        for s in SUJEITOS + "+":
            d[q, s] = (q, s, "R")
        d[q, c.upper()] = ("q4", "+", "L")               # concorda: marca e volta
    d["q10", "+"] = ("q10", "+", "R")
    d["q10", DIR] = (ACEITA, DIR, "L")
    return d


TRANSICOES = _tabela()


def _motivo(estado, simbolo):
    """Traduz a transição que faltou para o que ela significa na frase."""
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
    """Executa o ALL sobre w.

    Retorna (aceita, rastro, motivo). Cada linha do rastro é
    (estado, fita como texto, posição do cabeçote — 0 é o '<'), antes do passo.
    """
    fita, cabeca, estado, rastro = [ESQ, *w, DIR], 0, ESTADO_INICIAL, []
    while estado != ACEITA:
        rastro.append((estado, "".join(fita), cabeca))
        t = TRANSICOES.get((estado, fita[cabeca]))
        if t is None:
            motivo = _motivo(estado, fita[cabeca])
            return False, rastro, f"δ({estado}, '{fita[cabeca]}') não está definida: {motivo}"
        estado, fita[cabeca], mov = t
        cabeca += 1 if mov == "R" else -1
        assert 0 <= cabeca < len(fita), "o cabeçote saiu da fita"   # nunca ocorre: ver Etapa 4
    rastro.append((estado, "".join(fita), cabeca))
    return True, rastro, "todos os sujeitos e predicativos pareados"
