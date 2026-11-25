# Publicação e conferência no GitHub

`publicacao.py` reúne as operações usadas para distribuir a diretriz e conferir os arquivos no destino. Requer Python 3 e a CLI `gh` autenticada, com leitura para conferência e escrita para registrar a regra.

- `python3 github/publicacao.py diretriz conta/repositorio AGENTS.md` acrescenta o texto do arquivo local ao AGENTS.md da branch padrão. Preserva as instruções existentes e verifica o commit criado. Repetir a operação com o mesmo texto mantém o arquivo como está.
- `python3 github/publicacao.py conferir conta/repositorio REVISAO . AGENTS.md memoria/README.md` compara os bytes de cada arquivo local com o blob Git correspondente. Aceita um commit ou branch. Usar o SHA do commit torna a verificação reproduzível. O programa imprime os caminhos conferidos e termina com erro se houver divergência.
