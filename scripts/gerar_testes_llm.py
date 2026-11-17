#!/usr/bin/env python3
"""Prepara e consulta os perfis de ablação pela API Groq."""
import argparse
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

RAIZ = Path(__file__).resolve().parents[1]
ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
CABECALHOS = {
    "Content-Type": "application/json",
    "User-Agent": "analise-empirica-testes-llms/1.0",
}
PARAMETROS = {
    "model": "openai/gpt-oss-120b",
    "temperature": 0,
    "max_completion_tokens": 4096,
    "reasoning_effort": "low",
    "stream": False,
}
PACOTES = {"aluguel": "aluguelcarros", "poquer": "poquer", "academico": "academico"}
BLOCOS = ("Código", "Especificação", "Análise")
CONDICOES = {
    "completa": None,
    "sem-codigo": "Código",
    "sem-especificacao": "Especificação",
    "sem-analise": "Análise",
}
PERFIS = tuple(f"{funcao}-{condicao}" for funcao in PACOTES for condicao in CONDICOES)
ERROS_TEMPORARIOS = {429, 500, 502, 503, 504}


def json_bytes(dados):
    return (json.dumps(dados, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sha256(conteudo):
    return hashlib.sha256(conteudo).hexdigest()


def agora():
    return datetime.now(timezone.utc).isoformat()


def codigo_sem_javadoc(codigo):
    # Reconhece literais e comentários para preservar delimitadores dentro de strings.
    elementos = re.compile(
        r'^[ \t]*/\*\*.*?\*/[ \t]*(?:\n|$)|"{3}(?:\\.|(?!"{3}).)*"{3}|"(?:\\.|[^"\\])*"|'
        r"'(?:\\.|[^'\\])*'|//[^\r\n]*|/\*.*?\*/|\n(?:[ \t]*\n){2,}",
        re.DOTALL | re.MULTILINE,
    )

    def preservar(elemento):
        trecho = elemento.group()
        if trecho.lstrip().startswith("/**"):
            return "" if trecho.endswith("\n") else " "
        if trecho.startswith("\n"):
            return "\n\n"
        return trecho

    return elementos.sub(preservar, codigo)


def preparar(analises, plano):
    prompts = {}
    fontes = {}
    analises_originais = {}
    for funcao, pacote in PACOTES.items():
        modelo = RAIZ / "docs" / funcao / "prompt-ablação-template.md"
        modelo_bytes = modelo.read_bytes()
        analise = (analises / f"{funcao}.md").read_bytes()
        linhas = analise.decode("utf-8").splitlines()
        texto_analise = "\n".join(
            linha for linha in linhas if not linha.lstrip().startswith("> Orientação:")
        ).strip()
        if not texto_analise:
            raise ValueError(f"Análise vazia: {funcao}.md")
        fontes[modelo.relative_to(RAIZ).as_posix()] = sha256(modelo_bytes)
        fontes[f"analises/{funcao}.md"] = sha256(analise)
        analises_originais[funcao] = analise

        partes = re.split(r"(?m)^## (Código|Especificação|Análise)\n", modelo_bytes.decode("utf-8").replace("\r\n", "\n"))
        if tuple(partes[1::2]) != BLOCOS:
            raise ValueError(f"Blocos inesperados no modelo de {funcao}")
        campos = re.findall(r"\[[^\]\n]+\]", partes[6])
        if any(campo in texto_analise for campo in campos):
            raise ValueError(f"Preencha todos os campos do modelo de análise: {funcao}.md")
        base = partes[0]
        codigos = []
        for arquivo in sorted((RAIZ / "src/main/java/br/com" / pacote).glob("*.java")):
            caminho = arquivo.relative_to(RAIZ).as_posix()
            conteudo = arquivo.read_bytes()
            fontes[caminho] = sha256(conteudo)
            codigo = codigo_sem_javadoc(conteudo.decode('utf-8').replace('\r\n', '\n')).rstrip()
            codigos.append(f"`{caminho}`\n\n```java\n{codigo}\n```")
        if not codigos:
            raise ValueError(f"Nenhum fonte Java encontrado para {funcao}")
        codigo_esperado = "\n" + "\n\n".join(codigos) + "\n\n"
        if partes[2] != codigo_esperado:
            raise ValueError(f"Bloco Código do modelo de {funcao} diverge dos fontes sem Javadoc")
        blocos = {
            "Código": partes[2],
            "Especificação": partes[4],
            "Análise": "\n" + texto_analise + "\n",
        }
        for condicao, omitido in CONDICOES.items():
            perfil = f"{funcao}-{condicao}"
            prompt = base + "".join(f"## {nome}\n{blocos[nome]}" for nome in BLOCOS if nome != omitido)
            prompts[perfil] = prompt.encode("utf-8")

    plano.mkdir(parents=True)
    pasta_analises = plano / "analises"
    pasta_analises.mkdir()
    for funcao, analise in analises_originais.items():
        (pasta_analises / f"{funcao}.md").write_bytes(analise)
    for perfil, prompt in prompts.items():
        (plano / f"{perfil}.md").write_bytes(prompt)
    manifesto = {
        "criado_em_utc": agora(), "endpoint": ENDPOINT, "parametros": PARAMETROS,
        "script_sha256": sha256(Path(__file__).read_bytes()), "ordem": list(PERFIS),
        "prompts_sha256": {perfil: sha256(prompt) for perfil, prompt in prompts.items()},
        "fontes_sha256": fontes,
    }
    (plano / "manifesto.json").write_bytes(json_bytes(manifesto))


def carregar_plano(plano):
    manifesto = json.loads((plano / "manifesto.json").read_bytes())
    if (manifesto["endpoint"] != ENDPOINT or manifesto["parametros"] != PARAMETROS
            or manifesto["ordem"] != list(PERFIS)
            or manifesto["script_sha256"] != sha256(Path(__file__).read_bytes())):
        raise ValueError("O manifesto não corresponde à configuração deste script")
    prompts = {}
    for funcao in PACOTES:
        caminho = f"analises/{funcao}.md"
        if sha256((plano / caminho).read_bytes()) != manifesto["fontes_sha256"][caminho]:
            raise ValueError(f"Análise alterada após o congelamento: {caminho}")
    for perfil in PERFIS:
        prompt = (plano / f"{perfil}.md").read_bytes()
        if sha256(prompt) != manifesto["prompts_sha256"][perfil]:
            raise ValueError(f"Prompt alterado após o congelamento: {perfil}")
        prompts[perfil] = prompt
    return manifesto, prompts


class SemRedirecionamento(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def requisitar(corpo, chave):
    pedido = Request(
        ENDPOINT, data=corpo, method="POST",
        headers={**CABECALHOS, "Authorization": f"Bearer {chave}"},
    )
    try:
        with build_opener(SemRedirecionamento()).open(pedido, timeout=120) as resposta:
            return resposta.status, resposta.headers, resposta.read()
    except HTTPError as erro:
        with erro:
            return erro.code, erro.headers, erro.read()


def gravar_evento(saida, evento):
    with (saida / "eventos.jsonl").open("ab") as log:
        log.write(json.dumps(evento, ensure_ascii=False).encode("utf-8") + b"\n")


def classificar_resposta(status, bruto, pasta, evento):
    if status != 200:
        return "erro_http"
    try:
        dados = json.loads(bruto)
        escolha = dados["choices"][0]
        mensagem = escolha["message"]["content"]
        motivo = escolha["finish_reason"]
        if mensagem is not None and not isinstance(mensagem, str):
            raise ValueError("Conteúdo inesperado")
    except (ValueError, KeyError, IndexError, TypeError):
        return "resposta_invalida"
    evento.update(
        id_resposta=dados.get("id"), modelo_retornado=dados.get("model"),
        system_fingerprint=dados.get("system_fingerprint"), uso=dados.get("usage"),
        motivo_termino=motivo,
    )
    if mensagem:
        (pasta / "resposta.txt").write_text(mensagem, encoding="utf-8")
    if motivo == "length":
        return "truncada"
    if motivo == "stop" and mensagem and mensagem.strip():
        return "ok"
    return "resposta_incompleta"


def consultar(saida, perfil, prompt, chave):
    pasta = saida / perfil
    pasta.mkdir(exist_ok=True)
    corpo = json_bytes({**PARAMETROS, "messages": [{"role": "user", "content": prompt.decode("utf-8")}]})
    for nome, conteudo in (("prompt.md", prompt), ("requisicao.json", corpo)):
        arquivo = pasta / nome
        if arquivo.exists() and arquivo.read_bytes() != conteudo:
            raise ValueError(f"Evidência existente difere do plano: {arquivo}")
        arquivo.write_bytes(conteudo)

    # Uma resposta HTTP 200 encerra o perfil, inclusive quando veio truncada.
    anteriores = sorted((pasta / "tentativas").glob("*"))
    for anterior in anteriores:
        registro = anterior / "metadados.json"
        if not registro.is_file():
            raise ValueError(f"Tentativa interrompida em {anterior}. Preserve-a e use outra saída para reproduzir.")
        dados = json.loads(registro.read_bytes())
        if dados.get("http") == 200:
            return dados["estado"]
    inicio = len(anteriores)
    for indice in range(1, 4):
        numero = inicio + indice
        tentativa = pasta / "tentativas" / f"{numero:03d}"
        tentativa.mkdir(parents=True)
        evento = {
            "perfil": perfil, "tentativa": numero, "inicio_utc": agora(), "endpoint": ENDPOINT,
            "requisicao_sha256": sha256(corpo), "cabecalhos_requisicao": CABECALHOS,
            "evidencia": tentativa.relative_to(saida).as_posix(),
        }
        inicio_tempo = time.monotonic()
        try:
            status, headers, bruto = requisitar(corpo, chave)
        except (URLError, TimeoutError, OSError) as erro:
            evento.update(estado="falha_transporte", tipo_erro=type(erro).__name__)
        else:
            headers = {k.lower(): v for k, v in headers.items()}
            permitidos = {k: v.replace(chave, "[credencial omitida]") for k, v in headers.items()
                          if k.startswith("x-ratelimit-") or k in {"date", "retry-after", "x-request-id", "content-type"}}
            seguro = bruto.replace(chave.encode(), b"[credencial omitida]")
            (tentativa / "resposta-bruta.json").write_bytes(seguro)
            evento.update(http=status, cabecalhos=permitidos, credencial_omitida=seguro != bruto,
                          resposta_sha256=sha256(seguro))
            evento["estado"] = classificar_resposta(status, seguro, tentativa, evento)
        evento.update(fim_utc=agora(), duracao_s=round(time.monotonic() - inicio_tempo, 3))
        espera = None
        if evento.get("http") in ERROS_TEMPORARIOS and indice < 3:
            valor = evento["cabecalhos"].get("retry-after")
            try:
                espera = max(1, int(valor)) if valor is not None else (60 if evento["http"] == 429 else 5 * indice)
            except ValueError:
                try:
                    data = parsedate_to_datetime(valor)
                    espera = max(1, math.ceil((data - datetime.now(timezone.utc)).total_seconds()))
                except (ValueError, TypeError, OverflowError):
                    espera = 60
            evento["espera_s"] = espera
        (tentativa / "metadados.json").write_bytes(json_bytes(evento))
        gravar_evento(saida, evento)
        if espera is None:
            return evento["estado"]
        print(f"{perfil}: HTTP {evento['http']}, nova tentativa em {espera}s", flush=True)
        time.sleep(espera)


def executar(saida, manifesto, prompts, chave):
    if any(chave.encode() in prompt for prompt in prompts.values()):
        raise ValueError("Uma análise contém a chave da API. Remova-a antes de consultar.")
    saida.mkdir(parents=True, exist_ok=True)
    trava = saida / ".em-execucao"
    trava.mkdir()
    try:
        plano = saida / "plano.json"
        if plano.exists():
            if json.loads(plano.read_bytes()) != manifesto:
                raise ValueError("A saída pertence a outro plano. Escolha um diretório novo.")
        else:
            if any(p != trava for p in saida.iterdir()):
                raise ValueError("A saída deve ser nova ou pertencer ao mesmo plano.")
            plano.write_bytes(json_bytes(manifesto))
        gravar_evento(saida, {
            "evento": "inicio_execucao", "data_utc": agora(), "python": platform.python_version(),
            "sistema": platform.platform(), "perfis": list(prompts),
        })
        resumo = saida / "resumo.json"
        resultados = json.loads(resumo.read_bytes()) if resumo.exists() else {}
        for perfil, prompt in prompts.items():
            estado = consultar(saida, perfil, prompt, chave)
            resultados[perfil] = estado
            print(f"{perfil}: {estado}", flush=True)
            resumo.write_bytes(json_bytes(resultados))
            if estado in {"falha_transporte", "erro_http"}:
                # Retome com a mesma saída após resolver autenticação ou cota.
                break
        return int(any(resultados.get(perfil) != "ok" for perfil in prompts))
    finally:
        trava.rmdir()


def carregar_chave():
    chave = os.environ.get("GROQ_API_KEY", "").strip()
    if chave:
        return chave

    try:
        linhas = (RAIZ / ".env").read_text(encoding="utf-8-sig").splitlines()
    except FileNotFoundError:
        return ""
    for linha in linhas:
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue
        nome, separador, valor = linha.removeprefix("export ").partition("=")
        if separador and nome.strip() == "GROQ_API_KEY":
            valor = valor.strip()
            if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in ("'", '"'):
                valor = valor[1:-1]
            return valor.strip()
    return ""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    comandos = parser.add_subparsers(dest="comando", required=True)
    preparacao = comandos.add_parser("preparar", help="Gera e congela os 12 prompts")
    preparacao.add_argument("--analises", type=Path, default=Path("analises"))
    preparacao.add_argument("--plano", type=Path, default=Path("plano-llm"))
    verificacao = comandos.add_parser("verificar", help="Valida os hashes sem consultar a API")
    verificacao.add_argument("--plano", type=Path, default=Path("plano-llm"))
    geracao = comandos.add_parser("gerar", help="Consulta o plano congelado")
    geracao.add_argument("--plano", type=Path, default=Path("plano-llm"))
    geracao.add_argument("--saida", type=Path, default=Path("evidencias"))
    geracao.add_argument("--perfil", choices=PERFIS)
    piloto = comandos.add_parser("piloto", help="Testa a API com um exemplo alheio à atividade")
    piloto.add_argument("--saida", type=Path, default=Path("evidencias-piloto"))
    args = parser.parse_args()
    try:
        if args.comando == "preparar":
            preparar(RAIZ / args.analises, RAIZ / args.plano)
            print(f"12 prompts congelados em {RAIZ / args.plano}")
            return 0
        if args.comando == "verificar":
            carregar_plano(RAIZ / args.plano)
            print("Configuração e 12 prompts conferidos.")
            return 0
        chave = carregar_chave()
        if not chave:
            raise ValueError("Preencha GROQ_API_KEY no arquivo .env da raiz. Use .env.example como modelo.")
        if args.comando == "piloto":
            manifesto = {"tipo": "piloto", "endpoint": ENDPOINT, "parametros": PARAMETROS}
            prompts = {"piloto": b"Responda apenas com a soma de 2 e 3."}
        else:
            manifesto, prompts = carregar_plano(RAIZ / args.plano)
            if args.perfil:
                prompts = {args.perfil: prompts[args.perfil]}
        saida = RAIZ / args.saida
        print(f"Evidências da API: {saida}", flush=True)
        return executar(saida, manifesto, prompts, chave)
    except (OSError, ValueError, KeyError) as erro:
        parser.exit(2, f"Erro: {erro}\n")


if __name__ == "__main__":
    sys.exit(main())
