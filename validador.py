"""Validador de frases com "respectivamente": AP (estrutura) → ALL (concordância cruzada).

Uso:
    python validador.py "o,a,x,y&osrO,A,X,Y&O."            # fluxo completo
    python validador.py --rastro "o,a,x,y&osrO,A,X,Y&O."   # com rastreamento
    python validador.py --modulo ap  "o&asrO&A."           # só o AP
    python validador.py --modulo all "oaxyoOAXYO"          # só o ALL

Código de saída: 0 = aceita, 1 = rejeita, 2 = símbolo fora do alfabeto.
"""
import argparse
import sys

import automato_linear
import automato_pilha


def simbolo_invalido(w, alfabeto):
    """Devolve a mensagem de erro do 1º símbolo fora do alfabeto, ou None."""
    for i, s in enumerate(w, 1):
        if s not in alfabeto:
            return (f"Erro: o símbolo '{s}' (posição {i}) não pertence ao alfabeto de entrada "
                    f"{{{', '.join(alfabeto)}}}.")
    return None


def para_all(w):
    """Entrada do ALL: só sujeitos e predicativos, na ordem (sem ',', '&', 's', 'r', '.')."""
    return "".join(s for s in w if s in automato_linear.ALFABETO)


def mostrar_rastro_ap(rastro):
    print(f"{'passo':>5}  {'estado':<6} {'pos':>3}  {'lê':<3} pilha (topo à esquerda)")
    for k, (estado, pos, simbolo, pilha) in enumerate(rastro):
        lido = "fim" if simbolo is None else simbolo
        print(f"{k:>5}  {estado:<6} {pos:>3}  {lido:<3} {pilha}")


def mostrar_rastro_all(rastro):
    print(f"{'passo':>5}  {'estado':<6} {'cab':>3}  fita (cabeçote entre colchetes)")
    for k, (estado, fita, cabeca) in enumerate(rastro):
        marcada = "".join(f"[{c}]" if i == cabeca else c for i, c in enumerate(fita))
        print(f"{k:>5}  {estado:<6} {cabeca:>3}  {marcada}")


def rodar(nome, modulo, mostrar, w, rastro):
    aceita, passos, motivo = modulo.executar(w)
    if rastro:
        print(f"\n[{nome}] rastreamento de '{w}':")
        mostrar(passos)
    print(f"[{nome}] {'ACEITA' if aceita else 'REJEITA'}: {motivo}")
    return aceita


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cadeia", help="cadeia de entrada (use aspas)")
    ap.add_argument("--modulo", choices=["ap", "all"], help="roda só um dos reconhecedores")
    ap.add_argument("--rastro", action="store_true", help="mostra o rastreamento passo a passo")
    args = ap.parse_args(argv)
    w = args.cadeia

    alfabeto = automato_linear.ALFABETO if args.modulo == "all" else automato_pilha.ALFABETO
    erro = simbolo_invalido(w, alfabeto)
    if erro:
        print(erro)
        return 2

    print(f"Entrada: '{w}' ({len(w)} símbolos)")
    if args.modulo == "ap":
        return 0 if rodar("AP", automato_pilha, mostrar_rastro_ap, w, args.rastro) else 1
    if args.modulo == "all":
        return 0 if rodar("ALL", automato_linear, mostrar_rastro_all, w, args.rastro) else 1

    if not rodar("AP", automato_pilha, mostrar_rastro_ap, w, args.rastro):
        print("[ALL] não executado (o AP rejeitou)")
        print("Decisão final: REJEITA")
        return 1
    ok = rodar("ALL", automato_linear, mostrar_rastro_all, para_all(w), args.rastro)
    print(f"Decisão final: {'ACEITA' if ok else 'REJEITA'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
