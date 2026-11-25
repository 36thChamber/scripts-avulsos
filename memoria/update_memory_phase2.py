"""Reorganiza seções de duas cópias Markdown com marcadores escolhidos pelo usuário."""

import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("origem", type=Path)
parser.add_argument("plano", type=Path)
parser.add_argument("saida", type=Path, help="Pasta nova para os resultados")
args = parser.parse_args()
plan = json.loads(args.plano.read_text())
index = (args.origem / "MEMORY.md").read_text()
summary = (args.origem / "memory_summary.md").read_text()
start = index.index(plan["inicio_indice"])
end = index.index(plan["fim_indice"], start + len(plan["inicio_indice"]))
index = plan["novo_bloco_indice"] + index[:start] + index[end:]
for old, new in plan.get("substituicoes", []):
    if not old or old not in summary:
        raise ValueError("Trecho do resumo não encontrado")
    summary = summary.replace(old, new)
start = summary.index(plan["inicio_resumo"])
end = summary.index(plan["fim_resumo"], start + len(plan["inicio_resumo"]))
summary = summary[:start] + plan["novo_bloco_resumo"] + summary[end:]
# Os três marcadores delimitam dois blocos contíguos que trocam de posição.
first, second, limit = plan["reordenar"]
a = summary.index(first)
b = summary.index(second, a + len(first))
c = summary.index(limit, b + len(second))
summary = summary[:a] + summary[b:c] + summary[a:b] + summary[c:]
args.saida.mkdir(parents=True, exist_ok=False)
(args.saida / "MEMORY.md").write_text(index)
(args.saida / "memory_summary.md").write_text(summary)
