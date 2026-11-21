"""Roda os casos de testes/casos.csv e gera testes/resultados.md e testes/resultados.tex.

Uso:  python3 testes/rodar_testes.py
Saída 0 se todos os casos derem a decisão esperada e a conferência com as definições passar.
"""
import contextlib
import csv
import io
import itertools
import re
import sys
from pathlib import Path

PASTA = Path(__file__).resolve().parent
sys.path.insert(0, str(PASTA.parent))

import automato_linear  # noqa: E402
import automato_pilha  # noqa: E402
import validador  # noqa: E402

NOMES = {"AP": "Autômato de pilha (AP)", "ALL": "Autômato linearmente limitado (ALL)",
         "INTEGRACAO": "Fluxo completo (AP → ALL)", "ALFABETO": "Símbolo fora do alfabeto"}


def decisao(aceita):
    return "ACEITA" if aceita else "REJEITA"


def obter(modulo, w):
    """Devolve (decisão obtida, motivo/mensagem)."""
    if modulo == "AP":
        ok, _, motivo = automato_pilha.executar(w)
        return decisao(ok), motivo
    if modulo == "ALL":
        ok, _, motivo = automato_linear.executar(w)
        return decisao(ok), motivo
    if modulo == "INTEGRACAO":
        ok, _, motivo = automato_pilha.executar(w)
        if not ok:
            return "REJEITA/—", f"AP: {motivo}"
        ok2, _, motivo2 = automato_linear.executar(validador.para_all(w))
        return f"ACEITA/{decisao(ok2)}", f"ALL: {motivo2}"
    # ALFABETO / ALFABETO_ALL: passa pelo programa de verdade e captura a mensagem exibida
    args = [w] if modulo == "ALFABETO" else ["--modulo", "all", w]
    saida = io.StringIO()
    with contextlib.redirect_stdout(saida):
        codigo = validador.main(args)
    return ("ERRO" if codigo == 2 else f"código {codigo}"), saida.getvalue().strip()


def conferir_definicoes():
    """Compara os autômatos com as definições de L1 e L2 em todas as cadeias curtas."""
    h = dict(zip("oaxy", "OAXY"))

    def em_l1(s):
        return (re.fullmatch(r"[oaxy](,[oaxy])*&[oaxy]sr[OAXY](,[OAXY])*&[OAXY]\.", s) is not None
                and len(re.findall("[oaxy]", s)) == len(re.findall("[OAXY]", s)))

    def em_l2(s):
        k = len(s) // 2
        return len(s) >= 2 and len(s) % 2 == 0 and all(c in h for c in s[:k]) \
            and s[k:] == "".join(h.get(c, "?") for c in s[:k])

    n = 0
    for tam in range(8):
        for t in itertools.product("oO,&sr.", repeat=tam):
            s = "".join(t)
            n += 1
            if automato_pilha.executar(s)[0] != em_l1(s):
                return f"AP diverge de L1 em '{s}'"
    for tam in range(7):
        for t in itertools.product(automato_linear.ALFABETO, repeat=tam):
            s = "".join(t)
            n += 1
            if automato_linear.executar(s)[0] != em_l2(s):
                return f"ALL diverge de L2 em '{s}'"
    return f"ok ({n} cadeias)"


def tex(s):
    s = s.replace("\\", r"\textbackslash{}")
    for a, b in [("&", r"\&"), ("_", r"\_"), ("#", r"\#"), ("%", r"\%"), ("{", r"\{"), ("}", r"\}")]:
        s = s.replace(a, b)
    return s.replace("Z₀", "$Z_0$").replace("×", r"$\times$").replace("…", r"\ldots{}").replace("δ", r"$\delta$")


def main():
    casos = list(csv.DictReader(open(PASTA / "casos.csv", encoding="utf-8")))
    problemas = []
    for c in casos:
        c["obtido"], c["motivo"] = obter(c["modulo"], c["entrada"])
        c["ok"] = c["obtido"] == c["esperado"]
        if not c["ok"]:
            problemas.append(f"{c['id']}: esperado {c['esperado']}, obtido {c['obtido']}")

    # exigências da lauda para os testes de módulo
    for mod, alfabeto in [("AP", automato_pilha.ALFABETO), ("ALL", automato_linear.ALFABETO)]:
        linhas = [c for c in casos if c["modulo"] == mod]
        entradas = [c["entrada"] for c in linhas]
        if len(set(entradas)) != len(entradas):
            problemas.append(f"{mod}: há cadeias repetidas")
        if any(s not in alfabeto for w in entradas for s in w):
            problemas.append(f"{mod}: há cadeia com símbolo fora do alfabeto do módulo")
        for d in ("ACEITA", "REJEITA"):
            if sum(c["esperado"] == d for c in linhas) < 8:
                problemas.append(f"{mod}: menos de 8 casos {d}")
        for c in linhas:
            if len(c["entrada"]) < 18 and "Caso-limite" not in c["regra"]:
                problemas.append(f"{c['id']}: menos de 18 símbolos e não é caso-limite")

    definicoes = conferir_definicoes()
    if not definicoes.startswith("ok"):
        problemas.append(definicoes)

    # relatórios
    md = ["# Resultados dos testes", "", "Gerado por `python3 testes/rodar_testes.py`. Não editar à mão.", ""]
    tx = ["% Gerado por testes/rodar_testes.py. Não editar à mão.", "% Requer \\usepackage{longtable}"]
    for grupo in ["AP", "ALL", "INTEGRACAO", "ALFABETO"]:
        linhas = [c for c in casos if c["modulo"].startswith(grupo)]
        md += [f"## {NOMES[grupo]}", "", "| ID | Entrada | Tam. | Esperado | Obtido | Regra verificada |",
               "|---|---|---|---|---|---|"]
        tx += [f"\\subsection*{{{NOMES[grupo]}}}", "\\begin{longtable}{l p{5.2cm} r l l p{5cm}}",
               "\\textbf{ID} & \\textbf{Entrada} & \\textbf{Tam.} & \\textbf{Esperado} & \\textbf{Obtido} & "
               "\\textbf{Regra verificada} \\\\ \\hline \\endhead"]
        for c in linhas:
            w = c["entrada"]
            marca = "" if c["ok"] else " ✗"
            md.append(f"| {c['id']} | `{w}` | {len(w)} | {c['esperado']} | {c['obtido']}{marca} | {c['regra']} |"
                      if w else f"| {c['id']} | (vazia) | 0 | {c['esperado']} | {c['obtido']}{marca} | {c['regra']} |")
            tx.append(f"{c['id']} & \\texttt{{{tex(w) or '(vazia)'}}} & {len(w)} & {tex(c['esperado'])} & "
                      f"{tex(c['obtido'])} & {tex(c['regra'])} \\\\")
        tx.append("\\end{longtable}")
        md.append("")
        if grupo == "ALFABETO":
            md += ["### Mensagens de erro exibidas", ""]
            tx += ["\\paragraph{Mensagens de erro exibidas}", "\\begin{itemize}"]
            for c in linhas:
                md.append(f"- **{c['id']}**: `{c['motivo']}`")
                tx.append(f"\\item \\textbf{{{c['id']}}}: \\texttt{{{tex(c['motivo'])}}}")
            tx.append("\\end{itemize}")
            md.append("")
    md += ["## Conferência com as definições de L1 e L2", "",
           f"Todas as cadeias de comprimento ≤ 7 sobre {{o,O,`,`,&,s,r,.}} (AP) e ≤ 6 sobre o alfabeto do ALL: "
           f"**{definicoes}**.", ""]
    (PASTA / "resultados.md").write_text("\n".join(md), encoding="utf-8")
    (PASTA / "resultados.tex").write_text("\n".join(tx) + "\n", encoding="utf-8")

    total = len(casos)
    print(f"{total - sum(not c['ok'] for c in casos)}/{total} casos com a decisão esperada")
    print(f"conferência com as definições: {definicoes}")
    for p in problemas:
        print("FALHA:", p)
    print("tabelas: testes/resultados.md, testes/resultados.tex")
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
