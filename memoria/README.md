# Edição de índices Markdown

Execute com Python 3 sobre cópias de documentos locais. Os dois utilitários leem o plano em JSON e escrevem os resultados em uma pasta nova. Os planos de exemplo usam texto fictício.

| Arquivo | Finalidade | Entradas, execução e efeitos |
| --- | --- | --- |
| [consolidate_memory.py](consolidate_memory.py) | Prepara uma versão revisada de dois documentos Markdown a partir de um plano local. | Passe a pasta de origem com MEMORY.md e memory_summary.md, o plano JSON e uma pasta de saída nova. Exemplo de plano em consolidacao.exemplo.json. |
| [update_memory_phase2.py](update_memory_phase2.py) | Substitui e reorganiza seções dos dois documentos conforme os marcadores do plano. | Passe origem, plano JSON e pasta de saída nova. O exemplo reorganizacao.exemplo.json mostra os marcadores para substituir e reordenar seções. |
