"""Aplica uma diretriz preservando o AGENTS.md existente ou confere arquivos no GitHub."""

import argparse
import base64
import hashlib
import json
import subprocess
from pathlib import Path, PurePosixPath
from urllib.parse import quote


def api(endpoint, payload=None, optional=False):
    cmd = ["gh", "api", endpoint]
    if payload is not None:
        cmd += ["--method", "PUT", "--input", "-"]
    result = subprocess.run(
        cmd,
        input=json.dumps(payload) if payload is not None else None,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        if optional and "HTTP 404" in result.stderr:
            return None
        raise SystemExit(result.stderr.strip() or f"Falha ao consultar {endpoint}")
    return json.loads(result.stdout)


def content_endpoint(repository, path, ref=None):
    endpoint = f"repos/{repository}/contents/{quote(path, safe='/')}"
    return endpoint if ref is None else endpoint + "?ref=" + quote(ref, safe="")


def apply_rule(repository, rule_path):
    repo = api(f"repos/{repository}")
    branch = repo["default_branch"]
    resource = content_endpoint(repository, "AGENTS.md", branch)
    rule = rule_path.read_bytes().strip()
    if not rule:
        raise SystemExit("O arquivo de diretriz está vazio.")
    old = api(resource, optional=True)
    if old and old.get("type") != "file":
        raise SystemExit("O destino AGENTS.md precisa ser um arquivo regular.")
    current = base64.b64decode(old["content"]) if old else b""
    if rule in current:
        print(repository, "diretriz já presente")
        return
    # Preserva o texto existente e usa seu SHA para detectar edições concorrentes.
    new = current + (b"\n\n" if current else b"") + rule + b"\n"
    data = {
        "branch": branch,
        "message": "Registrar diretriz de publicação do código",
        "content": base64.b64encode(new).decode(),
    }
    if old:
        data["sha"] = old["sha"]
    commit = api(content_endpoint(repository, "AGENTS.md"), data)["commit"]["sha"]
    check = api(content_endpoint(repository, "AGENTS.md", commit))
    if base64.b64decode(check["content"]) != new:
        raise SystemExit("O conteúdo lido no GitHub diverge do enviado.")
    print(repository, commit)


def verify_files(repository, revision, root, paths):
    for text in paths:
        path = PurePosixPath(text)
        if path.is_absolute() or ".." in path.parts or not path.parts:
            raise SystemExit(f"Caminho inválido: {text}")
        data = (root / path).read_bytes()
        # O identificador do blob Git inclui o tipo e o comprimento, além dos bytes do arquivo.
        expected = hashlib.sha1(
            b"blob " + str(len(data)).encode() + b"\0" + data
        ).hexdigest()
        actual = api(content_endpoint(repository, str(path), revision))
        if actual.get("type") != "file" or actual.get("sha") != expected:
            raise SystemExit(f"Diferença em {path}")
        print(f"OK {path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="acao", required=True)
    apply = actions.add_parser("diretriz", help="Adiciona a regra à branch padrão.")
    apply.add_argument("repositorio", help="conta/repositorio")
    apply.add_argument("regra", type=Path)
    verify = actions.add_parser(
        "conferir", help="Compara os arquivos locais com uma revisão."
    )
    verify.add_argument("repositorio")
    verify.add_argument("revisao")
    verify.add_argument("raiz", type=Path)
    verify.add_argument("arquivos", nargs="+")
    args = parser.parse_args()
    if args.acao == "diretriz":
        apply_rule(args.repositorio, args.regra)
    else:
        verify_files(args.repositorio, args.revisao, args.raiz, args.arquivos)


if __name__ == "__main__":
    main()
