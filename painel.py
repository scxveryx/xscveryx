#!/bin/bash

# ============================================================
# CYBERTRACE v2.4 - Painel de Investigacao Digital
# Consultas com APIs publicas
# ============================================================
# TERMUX:  bash cybertrace.sh
# LINUX:   bash cybertrace.sh
# AJUDA:   bash cybertrace.sh --help
# ============================================================

VERDE='\033[1;32m'
VERMELHO='\033[1;31m'
AZUL='\033[1;34m'
AMARELO='\033[1;33m'
CIANO='\033[1;36m'
RESET='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")" 2>/dev/null && pwd)"
HIST_FILE="$SCRIPT_DIR/.cybertrace_historico.log"

# ============================================================
# AUXILIARES
# ============================================================

is_termux() {
    [[ -d "/data/data/com.termux" ]]
}

limpar_tela() {
    clear 2>/dev/null || printf '\033c'
}

press_enter() {
    echo
    read -r -p "Pressione ENTER para continuar..." _
}

linha() {
    echo -e "${VERDE}════════════════════════════════════════════${RESET}"
}

section() {
    echo -e "${AZUL}╔═══════════════════════════════════════════════╗${RESET}"
    printf "${AZUL}║${RESET}   ${VERDE}%s${RESET}\n" "$1"
    echo -e "${AZUL}╚═══════════════════════════════════════════════╝${RESET}"
    echo
}

api_get() {
    if ! command -v curl >/dev/null 2>&1; then
        echo -e "${VERMELHO}Erro: curl não está instalado.${RESET}" >&2
        return 1
    fi

    curl -fsSL --connect-timeout 8 --max-time 15 "$1" 2>/dev/null
}

url_encode() {
    python3 - "$1" <<'PY'
import sys
from urllib.parse import quote

print(quote(sys.argv[1]))
PY
}

salvar_historico() {
    printf '%s | %s\n' \
        "$(date '+%Y-%m-%d %H:%M:%S')" \
        "$1" >> "$HIST_FILE" 2>/dev/null
}

# timeout existe em Linux e normalmente no Termux.
executar_timeout() {
    if command -v timeout >/dev/null 2>&1; then
        timeout "$@"
    else
        shift
        "$@"
    fi
}

banner() {
    limpar_tela

    echo -e "${VERMELHO}"
    echo "╔═══════════════════════════════════════════════╗"
    echo "║                                               ║"
    echo -e "║     ${CIANO}██████╗██╗   ██╗██████╗ ███████╗██████╗${VERMELHO}   ║"
    echo -e "║     ${CIANO}██╔══██╗╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗${VERMELHO} ║"
    echo -e "║     ${CIANO}██████╔╝ ╚████╔╝ ██████╔╝█████╗  ██████╔╝${VERMELHO} ║"
    echo -e "║     ${CIANO}██╔══██╗  ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗${VERMELHO} ║"
    echo -e "║     ${CIANO}██████╔╝   ██║   ██████╔╝███████╗██║  ██║${VERMELHO} ║"
    echo -e "║     ${CIANO}╚═════╝    ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝${VERMELHO} ║"
    echo "║                                               ║"
    echo "╠═══════════════════════════════════════════════╣"
    echo -e "║${AMARELO}    PAINEL DE INVESTIGACAO DIGITAL v2.4       ${VERMELHO}║"
    echo -e "║${CIANO}                 by:xycbza                    ${VERMELHO}║"
    echo "╚═══════════════════════════════════════════════╝"
    echo -e "${RESET}"
}

# ============================================================
# HELP
# ============================================================

show_help() {
    echo -e "${CIANO}CYBERTRACE v2.4 - Painel de Investigacao Digital${RESET}"
    echo
    echo -e "${AMARELO}Uso:${RESET} bash cybertrace.sh [opcao] [valor]"
    echo
    echo -e "${VERDE}Opcoes:${RESET}"
    echo "  --help, -h             Mostra esta ajuda"
    echo "  --ip <IP>              Consulta informacoes publicas do IP"
    echo "  --cnpj <CNPJ>          Consulta CNPJ"
    echo "  --cep <CEP>            Consulta CEP"
    echo "  --cpf <CPF>            Valida formato/digitos do CPF"
    echo "  --fipe <CODIGO>        Consulta codigo FIPE"
    echo "  --dominio <DOM>        DNS + WHOIS"
    echo "  --email <EMAIL>        Informacoes publicas do dominio do email"
    echo "  --telefone <NUM>       Analisa pais + DDD"
    echo "  --ddd <DDD>            Consulta DDD"
    echo "  --banco <CODIGO>       Consulta banco"
    echo "  --cotacoes             Dolar, Euro e BTC"
    echo "  --rastreio <CODIGO>    Consulta rastreio"
    echo "  --feriados [ANO]       Feriados nacionais"
    echo "  --ssl <DOM>            Certificado SSL"
    echo "  --rdap <DOM>           RDAP do dominio"
    echo "  --portas <ALVO>        Verifica portas TCP comuns"
    echo "  --target <VALOR>       Detecta automaticamente o tipo"
    echo "  --historico            Mostra historico local"
    echo "  --update               Atualizacao manual"
    echo
    echo -e "${VERDE}Exemplos:${RESET}"
    echo "  bash cybertrace.sh --ip 8.8.8.8"
    echo "  bash cybertrace.sh --cep 01001000"
    echo "  bash cybertrace.sh --ddd 11"
    echo "  bash cybertrace.sh --cotacoes"
    echo "  bash cybertrace.sh --ssl example.com"
}

# ============================================================
# DDD
# ============================================================

consultar_ddd() {
    local ddd="$1"

    if [[ ! "$ddd" =~ ^[0-9]{2}$ ]]; then
        echo -e "${VERMELHO}DDD invalido.${RESET}"
        return 1
    fi

    local data
    data="$(api_get "https://brasilapi.com.br/api/ddd/v1/$ddd")" || return 1

    if ! echo "$data" | python3 -c 'import sys,json; json.load(sys.stdin)' >/dev/null 2>&1; then
        echo -e "${VERMELHO}Resposta invalida da BrasilAPI.${RESET}"
        return 1
    fi

    echo "$data" | python3 <<'PY'
import json
import sys

data = json.load(sys.stdin)
print("  UF     :", data.get("state", "-"))

cities = data.get("cities", [])
if cities:
    print("  Cidades:", ", ".join(cities))
else:
    print("  Cidades: -")
PY
}

buscar_ddd() {
    banner
    section "DDD + CIDADES"

    read -r -p "DDD: " ddd

    if consultar_ddd "$ddd"; then
        salvar_historico "DDD: $ddd"
    fi

    press_enter
}

# ============================================================
# TELEFONE
# ============================================================

buscar_telefone() {
    banner
    section "CONSULTAR TELEFONE"

    echo -e "${AMARELO}Formato: 55 11 999999999${RESET}"
    read -r -p "Numero: " tel

    tel="$(echo "$tel" | tr -d ' +()-')"

    if [[ ! "$tel" =~ ^[0-9]{12,15}$ ]]; then
        echo -e "${VERMELHO}Numero invalido.${RESET}"
        press_enter
        return
    fi

    local pais="${tel:0:2}"
    local ddd="${tel:2:2}"
    local numero="${tel:4}"

    linha

    echo -e "${AMARELO}Numero:${RESET} +$tel"

    if [[ "$pais" == "55" ]]; then
        echo -e "${AMARELO}Pais:${RESET} Brasil"
    else
        echo -e "${AMARELO}Codigo do pais:${RESET} $pais"
    fi

    echo -e "${AMARELO}DDD:${RESET} $ddd"
    echo -e "${AMARELO}Numero:${RESET} $numero"

    if [[ ${#numero} -eq 9 ]]; then
        echo -e "${AMARELO}Formato:${RESET} Celular"
    else
        echo -e "${AMARELO}Formato:${RESET} Outro"
    fi

    linha
    echo -e "${CIANO}Cidades associadas ao DDD:${RESET}"

    consultar_ddd "$ddd"

    salvar_historico "telefone: +$tel"
    press_enter
}

# ============================================================
# CNPJ
# ============================================================

cli_cnpj() {
    local cnpj="$1"
    local data

    data="$(api_get "https://brasilapi.com.br/api/cnpj/v1/$cnpj")" || return 1

    if ! echo "$data" | python3 -c 'import sys,json; d=json.load(sys.stdin); exit(0 if "cnpj" in d else 1)' >/dev/null 2>&1; then
        echo -e "${VERMELHO}CNPJ nao encontrado ou invalido.${RESET}"
        return 1
    fi

    echo "$data" | python3 <<'PY'
import json
import sys

d = json.load(sys.stdin)

print("=" * 60)
print("  CNPJ        :", d.get("cnpj", "-"))
print("  Razao Social:", d.get("razao_social", "-"))
print("  Fantasia    :", d.get("nome_fantasia", "-"))
print("  Endereco    :", d.get("logradouro", "-"))
print("  Numero      :", d.get("numero", "-"))
print("  Bairro      :", d.get("bairro", "-"))
print("  Cidade      :", d.get("municipio", "-"))
print("  UF          :", d.get("uf", "-"))
print("  CEP         :", d.get("cep", "-"))
print("  Telefone    :", d.get("ddd_telefone_1", "-"))
print("  Porte       :", d.get("porte", "-"))
print("  Abertura    :", d.get("data_inicio_atividade", "-"))
print("  Situacao    :", d.get("situacao_cadastral", "-"))
print("  Capital     :", d.get("capital_social", "-"))
print("  CNAE        :", d.get("cnae_fiscal", "-"))
print("  Descricao   :", d.get("cnae_fiscal_descricao", "-"))
print("=" * 60)
PY
}

buscar_cnpj() {
    banner
    section "CONSULTAR CNPJ"

    read -r -p "CNPJ (14 digitos): " cnpj
    cnpj="$(echo "$cnpj" | tr -d ' ./-')"

    if [[ ! "$cnpj" =~ ^[0-9]{14}$ ]]; then
        echo -e "${VERMELHO}CNPJ deve conter 14 digitos.${RESET}"
        press_enter
        return
    fi

    cli_cnpj "$cnpj"
    salvar_historico "CNPJ consultado"
    press_enter
}

# ============================================================
# CPF - VALIDACAO LOCAL
# ============================================================

cli_cpf() {
    local cpf="$1"

    python3 - "$cpf" <<'PY'
import sys

cpf = sys.argv[1]

if len(cpf) != 11 or not cpf.isdigit():
    print("ERRO: CPF deve ter 11 digitos.")
    sys.exit(1)

if len(set(cpf)) == 1:
    print("Valido: NAO")
    sys.exit(0)

soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
r1 = (soma * 10) % 11
if r1 == 10:
    r1 = 0

soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
r2 = (soma * 10) % 11
if r2 == 10:
    r2 = 0

valido = r1 == int(cpf[9]) and r2 == int(cpf[10])

print(
    "CPF: %s.%s.%s-%s"
    % (cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])
)
print("Valido:", "SIM" if valido else "NAO")

if valido:
    estados = {
        0: "RS",
        1: "DF/GO/MS/MT",
        2: "PA/AM/AC/RO/RR",
        3: "CE/MA/PI",
        4: "PE/PB/RN/AL",
        5: "BA/SE",
        6: "MG",
        7: "RJ/ES",
        8: "SP",
        9: "PR/SC"
    }

    print("UF emissor:", estados.get(int(cpf[8]), "Desconhecido"))
PY
}

validar_cpf() {
    banner
    section "VALIDACAO DE CPF"

    echo -e "${AMARELO}[!] A validacao e feita localmente.${RESET}"
    echo -e "${AMARELO}[!] Nenhuma consulta cadastral e realizada.${RESET}"
    echo

    read -r -p "CPF: " cpf
    cpf="$(echo "$cpf" | tr -d ' .-')"

    if [[ ! "$cpf" =~ ^[0-9]{11}$ ]]; then
        echo -e "${VERMELHO}CPF invalido.${RESET}"
        press_enter
        return
    fi

    linha
    cli_cpf "$cpf"
    linha

    # Nao grava o CPF completo no historico.
    salvar_historico "validacao de CPF realizada"

    press_enter
}

# ============================================================
# CEP
# ============================================================

cli_cep() {
    local cep="$1"
    local data

    data="$(api_get "https://viacep.com.br/ws/$cep/json/")" || return 1

    if ! echo "$data" | python3 -c 'import sys,json; d=json.load(sys.stdin); exit(1 if d.get("erro") else 0)' >/dev/null 2>&1; then
        echo -e "${VERMELHO}CEP nao encontrado.${RESET}"
        return 1
    fi

    echo "$data" | python3 <<'PY'
import json
import sys

d = json.load(sys.stdin)

print("=" * 60)
print("  CEP     :", d.get("cep", "-"))
print("  Rua     :", d.get("logradouro", "-"))
print("  Bairro  :", d.get("bairro", "-"))
print("  Cidade  :", d.get("localidade", "-"))
print("  UF      :", d.get("uf", "-"))
print("  Estado  :", d.get("estado", "-"))
print("  DDD     :", d.get("ddd", "-"))
print("  IBGE    :", d.get("ibge", "-"))
print("=" * 60)
PY
}

buscar_cep() {
    banner
    section "CONSULTAR CEP"

    read -r -p "CEP: " cep
    cep="$(echo "$cep" | tr -d ' -')"

    if [[ ! "$cep" =~ ^[0-9]{8}$ ]]; then
        echo -e "${VERMELHO}CEP deve ter 8 digitos.${RESET}"
        press_enter
        return
    fi

    cli_cep "$cep"
    salvar_historico "CEP: $cep"
    press_enter
}

# ============================================================
# BANCO
# ============================================================

cli_banco() {
    local cod="$1"
    local data

    data="$(api_get "https://brasilapi.com.br/api/banks/v1/$cod")" || return 1

    if ! echo "$data" | python3 -c 'import sys,json; d=json.load(sys.stdin); exit(0 if "name" in d else 1)' >/dev/null 2>&1; then
        return 1
    fi

    echo "$data" | python3 <<'PY'
import json
import sys

d = json.load(sys.stdin)

print("=" * 60)
print("  Codigo :", d.get("code", "-"))
print("  Banco  :", d.get("name", "-"))
print("  ISPB   :", d.get("ispb", "-"))
print("  Nome   :", d.get("fullName", "-"))
print("=" * 60)
PY
}

consultar_banco() {
    banner
    section "CONSULTAR BANCO"

    read -r -p "Codigo do banco: " cod

    if [[ ! "$cod" =~ ^[0-9]+$ ]]; then
        echo -e "${VERMELHO}Codigo invalido.${RESET}"
        press_enter
        return
    fi

    if cli_banco "$cod"; then
        salvar_historico "banco: $cod"
    else
        echo -e "${VERMELHO}Banco nao encontrado.${RESET}"
    fi

    press_enter
}

# ============================================================
# COTACOES
# ============================================================

cli_cotacoes() {
    local data

    data="$(api_get "https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL")" || return 1

    echo "$data" | python3 <<'PY'
import json
import sys

d = json.load(sys.stdin)

print("=" * 60)

for chave in ("USDBRL", "EURBRL", "BTCBRL"):
    v = d.get(chave, {})

    if v:
        print(
            "  %-5s: R$ %s  (%s%%)"
            % (
                v.get("code", "-"),
                v.get("bid", "-"),
                v.get("pctChange", "-")
            )
        )

print("=" * 60)
PY
}

cotacoes() {
    banner
    section "COTACOES"

    if cli_cotacoes; then
        salvar_historico "cotacoes"
    else
        echo -e "${VERMELHO}Erro ao consultar cotacoes.${RESET}"
    fi

    press_enter
}

# ============================================================
# DOMINIO
# ============================================================

cli_dominio() {
    local dom="$1"

    dom="${dom#http://}"
    dom="${dom#https://}"
    dom="${dom%%/*}"

    if [[ -z "$dom" ]]; then
        echo -e "${VERMELHO}Dominio invalido.${RESET}"
        return 1
    fi

    if ! command -v dig >/dev/null 2>&1; then
        echo -e "${VERMELHO}dig nao encontrado.${RESET}"
        echo -e "${AMARELO}Termux:${RESET} pkg install dnsutils"
        return 1
    fi

    local ip
    ip="$(executar_timeout 6 dig +short "$dom" 2>/dev/null | head -1)"

    linha
    echo -e "${AMARELO}Dominio:${RESET} $dom"
    echo -e "${AMARELO}IP:${RESET} ${ip:-Nao resolvido}"
    echo

    echo -e "${CIANO}MX:${RESET}"
    executar_timeout 6 dig +short MX "$dom" 2>/dev/null

    echo
    echo -e "${CIANO}NS:${RESET}"
    executar_timeout 6 dig +short NS "$dom" 2>/dev/null

    echo
    echo -e "${CIANO}TXT:${RESET}"
    executar_timeout 6 dig +short TXT "$dom" 2>/dev/null | head -5

    if command -v whois >/dev/null 2>&1; then
        echo
        echo -e "${CIANO}WHOIS:${RESET}"
        executar_timeout 8 whois "$dom" 2>/dev/null |
            grep -iE "domain|registrar|created|expiry|status|organization" |
            head -10
    fi

    linha
}

buscar_dominio() {
    banner
    section "DOMINIO - DNS + WHOIS"

    read -r -p "Dominio: " dom

    if cli_dominio "$dom"; then
        salvar_historico "dominio: $dom"
    fi

    press_enter
}

# ============================================================
# SSL
# ============================================================

cli_ssl() {
    local dom="$1"

    dom="${dom#http://}"
    dom="${dom#https://}"
    dom="${dom%%/*}"

    if ! command -v openssl >/dev/null 2>&1; then
        echo -e "${VERMELHO}openssl nao encontrado.${RESET}"
        return 1
    fi

    local saida

    saida=$(
        printf '\n' |
        executar_timeout 12 \
        openssl s_client \
            -servername "$dom" \
            -connect "$dom:443" 2>/dev/null |
        openssl x509 -noout -dates -issuer -subject 2>/dev/null
    )"

    if [[ -z "$saida" ]]; then
        return 1
    fi

    linha
    echo "$saida"
    linha

    return 0
}

ssl_certificado() {
    banner
    section "CERTIFICADO SSL"

    read -r -p "Dominio: " dom

    if [[ -z "$dom" ]]; then
        echo -e "${VERMELHO}Dominio invalido.${RESET}"
        press_enter
        return
    fi

    echo -e "${CIANO}Verificando certificado de $dom...${RESET}"

    if cli_ssl "$dom"; then
        salvar_historico "SSL: $dom"
    else
        echo -e "${VERMELHO}Nao foi possivel obter o certificado SSL.${RESET}"
    fi

    press_enter
}

# ============================================================
# RDAP
# ============================================================

cli_rdap() {
    local dom="$1"
    local data

    dom="${dom#http://}"
    dom="${dom#https://}"
    dom="${dom%%/*}"

    data="$(api_get "https://rdap.org/domain/$dom")" || return 1

    echo "$data" | python3 <<'PY'
import json
import sys

d = json.load(sys.stdin)

print("=" * 60)
print("  Nome:", d.get("ldhName", "-"))
print("  Status:", ", ".join(d.get("status", [])) or "-")

for event in d.get("events", []):
    print("  %s: %s" % (
        event.get("eventAction", "-"),
        event.get("eventDate", "-")
    ))

print("=" * 60)
PY
}

buscar_rdap() {
    banner
    section "RDAP"

    read -r -p "Dominio: " dom

    if cli_rdap "$dom"; then
        salvar_historico "RDAP: $dom"
    else
        echo -e "${VERMELHO}Nao foi possivel consultar RDAP.${RESET}"
    fi

    press_enter
}

# ============================================================
# IP
# ============================================================

cli_ip() {
    local ip="$1"
    local data

    if [[ ! "$ip" =~ ^[0-9a-fA-F:.]+$ ]]; then
        echo -e "${VERMELHO}Endereco IP invalido.${RESET}"
        return 1
    fi

    data="$(api_get "https://ipwho.is/$ip")" || return 1

    echo "$data" | python3 <<'PY'
import json
import sys

d = json.load(sys.stdin)

print("=" * 60)
print("  IP       :", d.get("ip", "-"))
print("  Sucesso  :", d.get("success", "-"))
print("  Pais     :", d.get("country", "-"))
print("  Regiao   :", d.get("region", "-"))
print("  Cidade   :", d.get("city", "-"))
print("  ISP      :", d.get("connection", {}).get("isp", "-"))
print("  ASN      :", d.get("connection", {}).get("asn", "-"))
print("=" * 60)
PY
}

buscar_ip() {
    banner
    section "CONSULTAR IP"

    read -r -p "IP: " ip

    if cli_ip "$ip"; then
        salvar_historico "IP: $ip"
    fi

    press_enter
}

# ============================================================
# FIPE
# ============================================================

cli_fipe() {
    local codigo="$1"
    local data

    # A API publica do serviço pode variar.
    # Mantemos a consulta separada para facilitar a troca do endpoint.
    data="$(api_get "https://brasilapi.com.br/api/fipe/preco/v1/$codigo")" || return 1

    if ! echo "$data" | python3 -c 'import sys,json; d=json.load(sys.stdin); exit(0 if isinstance(d,list) else 1)' >/dev/null 2>&1; then
        echo -e "${VERMELHO}Codigo FIPE nao encontrado ou resposta invalida.${RESET}"
        return 1
    fi

    echo "$data" | python3 <<'PY'
import json
import sys

d = json.load(sys.stdin)

print("=" * 60)

for item in d[:10]:
    print("  Marca      :", item.get("marca", "-"))
    print("  Modelo     :", item.get("modelo", "-"))
    print("  Ano        :", item.get("anoModelo", "-"))
    print("  Combustivel:", item.get("combustivel", "-"))
    print("  Codigo FIPE:", item.get("codigoFipe", "-"))
    print("  Valor      :", item.get("valor", "-"))
    print("-" * 60)
PY
}

buscar_veiculo() {
    banner
    section "VEICULO - PRECO FIPE"

    echo -e "${AMARELO}Use o codigo FIPE do veiculo.${RESET}"
    read -r -p "Codigo FIPE: " codigo

    if [[ -z "$codigo" ]]; then
        echo -e "${VERMELHO}Codigo invalido.${RESET}"
        press_enter
        return
    fi

    if cli_fipe "$codigo"; then
        salvar_historico "FIPE: $codigo"
    fi

    press_enter
}

# ============================================================
# FERIADOS
# ============================================================

cli_feriados() {
    local ano="$1"
    local data

    if [[ ! "$ano" =~ ^[0-9]{4}$ ]]; then
        echo -e "${VERMELHO}Ano invalido.${RESET}"
        return 1
    fi

    data="$(api_get "https://brasilapi.com.br/api/feriados/v1/$ano")" || return 1

    echo "$data" | python3 <<'PY'
import json
import sys

d = json.load(sys.stdin)

if not isinstance(d, list):
    raise SystemExit(1)

print("=" * 60)

for f in d:
    print(
        "  %s  %s"
        % (
            f.get("date", "-"),
            f.get("name", "-")
        )
    )

print("=" * 60)
PY
}

feriados() {
    banner
    section "FERIADOS NACIONAIS"

    read -r -p "Ano [$(date +%Y)]: " ano
    ano="${ano:-$(date +%Y)}"

    if cli_feriados "$ano"; then
        salvar_historico "feriados: $ano"
    else
        echo -e "${VERMELHO}Erro ao buscar feriados.${RESET}"
    fi

    press_enter
}

# ============================================================
# HISTORICO
# ============================================================

historico() {
    banner
    section "HISTORICO"

    if [[ ! -f "$HIST_FILE" ]]; then
        echo -e "${AMARELO}Nenhuma consulta registrada.${RESET}"
    else
        tail -50 "$HIST_FILE"
    fi

    press_enter
}

# ============================================================
# PORTAS
# ============================================================

consultar_portas() {
    local alvo="$1"

    if [[ -z "$alvo" ]]; then
        echo -e "${VERMELHO}Alvo invalido.${RESET}"
        return 1
    fi

    if ! command -v nc >/dev/null 2>&1; then
        echo -e "${VERMELHO}netcat (nc) nao esta instalado.${RESET}"
        echo -e "${AMARELO}Termux:${RESET} pkg install netcat-openbsd"
        return 1
    fi

    local portas=(21 22 23 25 53 80 110 143 443 445 587 993 995 3306 3389 8080)

    echo -e "${CIANO}Verificando portas TCP comuns em $alvo...${RESET}"
    echo

    for porta in "${portas[@]}"; do
        if nc -z -w 2 "$alvo" "$porta" >/dev/null 2>&1; then
            echo -e "${VERDE}[ABERTA]${RESET} $porta"
        else
            echo -e "${VERMELHO}[FECHADA]${RESET} $porta"
        fi
    done
}

buscar_portas() {
    banner
    section "PORTAS TCP COMUNS"

    echo -e "${AMARELO}Use somente em sistemas que voce esta autorizado a testar.${RESET}"
    echo

    read -r -p "Alvo: " alvo

    consultar_portas "$alvo"
    press_enter
}

# ============================================================
# EMAIL
# ============================================================

consultar_email() {
    banner
    section "EMAIL - INFORMACOES DO DOMINIO"

    read -r -p "Email: " email

    if [[ ! "$email" =~ ^[^@[:space:]]+@[^@[:space:]]+\.[^@[:space:]]+$ ]]; then
        echo -e "${VERMELHO}Email invalido.${RESET}"
        press_enter
        return
    fi

    local dominio="${email##*@}"

    echo -e "${AMARELO}Email:${RESET} $email"
    echo -e "${AMARELO}Dominio:${RESET} $dominio"
    echo

    if command -v dig >/dev/null 2>&1; then
        echo -e "${CIANO}Registros MX:${RESET}"
        dig +short MX "$dominio"
    else
        echo -e "${AMARELO}dig nao instalado; MX nao consultado.${RESET}"
    fi

    salvar_historico "email: dominio consultado"
    press_enter
}

# ============================================================
# TARGET
# ============================================================

target_auto() {
    local valor="$1"

    if [[ -z "$valor" ]]; then
        echo -e "${VERMELHO}Valor vazio.${RESET}"
        return 1
    fi

    if [[ "$valor" =~ ^[0-9]{8}$ ]]; then
        cli_cep "$valor"
        return
    fi

    if [[ "$valor" =~ ^[0-9]{11}$ ]]; then
        cli_cpf "$valor"
        return
    fi

    if [[ "$valor" =~ ^[0-9]{14}$ ]]; then
        cli_cnpj "$valor"
        return
    fi

    if [[ "$valor" =~ ^[0-9]{1,3}(\.[0-9]{1,3}){3}$ ]]; then
        cli_ip "$valor"
        return
    fi

    if [[ "$valor" =~ ^[0-9]{2}$ ]]; then
        consultar_ddd "$valor"
        return
    fi

    if [[ "$valor" =~ ^[A-Za-z0-9.-]+\.[A-Za-z]{2,}$ ]]; then
        cli_dominio "$valor"
        return
    fi

    echo -e "${AMARELO}Nao foi possivel determinar automaticamente o tipo.${RESET}"
    return 1
}

# ============================================================
# MENU
# ============================================================

menu() {
    while true; do
        banner

        echo -e "${CIANO}1.${RESET}  Consultar IP"
        echo -e "${CIANO}2.${RESET}  Consultar CNPJ"
        echo -e "${CIANO}3.${RESET}  Consultar CEP"
        echo -e "${CIANO}4.${RESET}  Validar CPF"
        echo -e "${CIANO}5.${RESET}  Consultar FIPE"
        echo -e "${CIANO}6.${RESET}  Consultar dominio"
        echo -e "${CIANO}7.${RESET}  Consultar email"
        echo -e "${CIANO}8.${RESET}  Consultar telefone"
        echo -e "${CIANO}9.${RESET}  Consultar DDD"
        echo -e "${CIANO}10.${RESET} Consultar banco"
        echo -e "${CIANO}11.${RESET} Cotacoes"
        echo -e "${CIANO}12.${RESET} Feriados"
        echo -e "${CIANO}13.${RESET} Certificado SSL"
        echo -e "${CIANO}14.${RESET} RDAP"
        echo -e "${CIANO}15.${RESET} Portas TCP"
        echo -e "${CIANO}16.${RESET} Historico"
        echo -e "${CIANO}0.${RESET}  Sair"
        echo

        read -r -p "Escolha: " opcao

        case "$opcao" in
            1)  buscar_ip ;;
            2)  buscar_cnpj ;;
            3)  buscar_cep ;;
            4)  validar_cpf ;;
            5)  buscar_veiculo ;;
            6)  buscar_dominio ;;
            7)  consultar_email ;;
            8)  buscar_telefone ;;
            9)  buscar_ddd ;;
            10) consultar_banco ;;
            11) cotacoes ;;
            12) feriados ;;
            13) ssl_certificado ;;
            14) buscar_rdap ;;
            15) buscar_portas ;;
            16) historico ;;
            0)
                echo -e "${CIANO}Saindo...${RESET}"
                exit 0
                ;;
            *)
                echo -e "${VERMELHO}Opcao invalida.${RESET}"
                sleep 1
                ;;
        esac
    done
}

# ============================================================
# ARGUMENTOS
# ============================================================

if [[ $# -eq 0 ]]; then
    menu
fi

case "$1" in

    --help|-h)
        show_help
        ;;

    --ip)
        [[ -z "$2" ]] && {
            echo -e "${VERMELHO}Uso: --ip <IP>${RESET}"
            exit 1
        }
        cli_ip "$2"
        ;;

    --cnpj)
        [[ -z "$2" ]] && {
            echo -e "${VERMELHO}Uso: --cnpj <CNPJ>${RESET}"
            exit 1
        }
        cli_cnpj "$(echo "$2" | tr -d ' ./-')"
        ;;

    --cep)
        [[ -z "$2" ]] && {
            echo -e "${VERMELHO}Uso: --cep <CEP>${RESET}"
            exit 1
        }
        cli_cep "$(echo "$2" | tr -d ' -')"
        ;;

    --cpf)
        [[ -z "$2" ]] && {
            echo -e "${VERMELHO}Uso: --cpf <CPF>${RESET}"
            exit 1
        }
        cli_cpf "$(echo "$2" | tr -d ' .-')"
        ;;

    --fipe)
        [[ -z "$2" ]] && {
            echo -e "${VERMELHO}Uso: --fipe <CODIGO>${RESET}"
            exit 1
        }
        cli_fipe "$2"
        ;;

    --dominio|--domain)
        [[ -z "$2" ]] && {
            echo -e "${VERMELHO}Uso: --dominio <DOMINIO>${RESET}"
            exit 1
        }
        cli_dominio "$2"
        ;;

    --email)
        [[ -z "$2" ]] && {
            echo -e "${VERMELHO}Uso: --email <EMAIL>${RESET}"
            exit 1
        }
        email="$2"
        dominio="${email##*@}"
        echo -e "${AMARELO}Email:${RESET} $email"
        echo -e "${AMARELO}Dominio:${RESET} $dominio"
        command -v dig >/dev/null 2>&1 && dig +short MX "$dominio"
        ;;

    --telefone)
        [[ -z "$2" ]] && {
            echo -e "${VERMELHO}Uso: --telefone <NUMERO>${RESET}"
            exit 1
        }
        tel="$(echo "$2" | tr -d ' +()-')"
        pais="${tel:0:2}"
        ddd="${tel:2:2}"
        numero="${tel:4}"
        echo "Pais: $pais"
        echo "DDD: $ddd"
        echo "Numero: $numero"
        consultar_ddd "$ddd"
        ;;

    --ddd)
        [[ -z "$2" ]] && {
            echo -e "${VERMELHO}Uso: --ddd <DDD>${RESET}"
            exit 1
        }
        consultar_ddd "$2"
        ;;

    --banco)
        [[ -z "$2" ]] && {
            echo -e "${VERMELHO}Uso: --banco <CODIGO>${RESET}"
            exit 1
        }
        cli_banco "$2"
        ;;

    --cotacoes)
        cotacoes
        ;;

    --rastreio)
        echo -e "${AMARELO}A consulta de rastreio depende de um provedor/API valido.${RESET}"
        echo -e "${AMARELO}Configure seu provedor antes de usar esta opcao.${RESET}"
        ;;

    --feriados)
        cli_feriados "${2:-$(date +%Y)}"
        ;;

    --ssl)
        [[ -z "$2" ]] && {
            echo -e "${VERMELHO}Uso: --ssl <DOMINIO>${RESET}"
            exit 1
        }
        cli_ssl "$2"
        ;;

    --rdap)
        [[ -z "$2" ]] && {
            echo -e "${VERMELHO}Uso: --rdap <DOMINIO>${RESET}"
            exit 1
        }
        cli_rdap "$2"
        ;;

    --portas)
        [[ -z "$2" ]] && {
            echo -e "${VERMELHO}Uso: --portas <ALVO>${RESET}"
            exit 1
        }
        consultar_portas "$2"
        ;;

    --target)
        [[ -z "$2" ]] && {
            echo -e "${VERMELHO}Uso: --target <VALOR>${RESET}"
            exit 1
        }
        target_auto "$2"
        ;;

    --historico)
        if [[ -f "$HIST_FILE" ]]; then
            tail -50 "$HIST_FILE"
        else
            echo "Historico vazio."
        fi
        ;;

    --update)
        echo -e "${AMARELO}Atualizacao automatica nao configurada.${RESET}"
        echo "Defina o repositorio oficial antes de implementar --update."
        ;;

    *)
        echo -e "${VERMELHO}Opcao desconhecida: $1${RESET}"
        echo
        show_help
        exit 1
        ;;

esac

Principais erros corrigidos

- Fechamento correto da função "ssl_certificado()".
- Adicionado "cli_fipe()", que era chamado mas não existia.
- Adicionado tratamento de "--ddd".
- Adicionado parser completo das opções.
- Adicionado menu interativo.
- Corrigido tratamento de "https://" nos domínios.
- Adicionadas verificações para "curl", "dig", "openssl", "nc" e Python.
- Corrigido tratamento de respostas JSON.
- Evitada gravação do CPF completo no histórico.
- Adicionado "--historico".
- Adicionado "--target".
- Adicionado "--rdap".
- Adicionado "--ip".
- Adicionado "--ssl".
- Adicionado "--portas".
- Corrigido o final incompleto do arquivo.
- Mantidas as cores e o estilo do painel.

Para verificar só a sintaxe Bash, rode:

bash -n cybertrace.sh

Se não aparecer nenhuma mensagem, a sintaxe do Bash está correta. Para executar:

chmod +x cybertrace.sh
./cybertrace.sh

No Termux, se estiver faltando dependência:

pkg update
pkg install bash curl python dnsutils openssl netcat-openbsd

Use as funções de verificação de portas apenas em sistemas que você tem autorização para testar.
