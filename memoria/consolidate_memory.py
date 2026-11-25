"""Prepara cópias do índice e do resumo de memória combinando textos fornecidos localmente."""

import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("origem", type=Path)
parser.add_argument(
    "plano", type=Path, help="JSON com prefixo e substituicoes (pares de textos)"
)
parser.add_argument("saida", type=Path, help="Pasta nova para as duas cópias")
args = parser.parse_args()
plan = json.loads(args.plano.read_text())
index = (args.origem / "MEMORY.md").read_text()
summary = (args.origem / "memory_summary.md").read_text()
for old, new in plan["substituicoes"]:
    if not old or old not in summary:
        raise ValueError("Trecho do resumo não encontrado")
    summary = summary.replace(old, new, 1)
# A edição pública recebe todo o conteúdo pessoal por arquivo local.
args.saida.mkdir(parents=True, exist_ok=False)
(args.saida / "MEMORY.md").write_text(plan["prefixo"] + index)
(args.saida / "memory_summary.md").write_text(summary)
