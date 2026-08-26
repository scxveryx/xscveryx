#!/bin/bash

# ============================================================
# CYBERTRACE v2.4 - Painel de Investigacao Digital
# Consultas com APIs publicas reais
# ------------------------------------------------------------
# TERMUX:  bash install.sh
# LINUX:   bash install.sh --linux
# AJUDA:   bash cybertrace.sh --help
# ============================================================

VERDE='\033[1;32m'
VERMELHO='\033[1;31m'
AZUL='\033[1;34m'
AMARELO='\033[1;33m'
CIANO='\033[1;36m'
RESET='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HIST_FILE="$SCRIPT_DIR/.cybertrace_historico.log"

# ============================================================
# AUXILIARES
# ============================================================
is_termux() { command -v termux-open-url &>/dev/null; }

url_encode() {
    python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$1" 2>/dev/null
}

api_get() {
    curl -s --max-time 12 "$1" 2>/dev/null
}

press_enter() {
    echo ""
    read -r -p "Pressione ENTER para continuar..." _
}

banner() {
    clear
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
    echo -e "║${AMARELO}    PAINEL DE INVESTIGACAO DIGITAL v2.4   ${VERMELHO}║"
    echo -e "║${CIANO} by:xycbza ${VERMELHO}║"
    echo "╚═══════════════════════════════════════════════╝"
    echo -e "${RESET}"
}

section() {
    echo -e "${AZUL}╔═══════════════════════════════════════════════╗${RESET}"
    echo -e "${AZUL}║${RESET}   ${VERDE}$1${RESET}"
    echo -e "${AZUL}╚═══════════════════════════════════════════════╝${RESET}"
    echo ""
}

linha() {
    echo -e "${VERDE}════════════════════════════════════════════${RESET}"
}

salvar_historico() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') | $1" >> "$HIST_FILE" 2>/dev/null
}
# ============================================================
# HELP
# ============================================================
show_help() {
    echo -e "${CIANO}CYBERTRACE v2.4 - Painel de Investigacao Digital${RESET}"
    echo -e "${AMARELO}Uso:${RESET} bash cybertrace.sh [opcao] [valor]"
    echo ""
    echo -e "${VERDE}Opcoes:${RESET}"
    echo -e "  ${AMARELO}sem argumentos${RESET}    -> Menu interativo"
    echo -e "  ${AMARELO}--help, -h${RESET}        -> Mostra esta ajuda"
    echo -e "  ${AMARELO}--ip <IP>${RESET}         -> IP detalhado"
    echo -e "  ${AMARELO}--cnpj <CNPJ>${RESET}     -> CNPJ (BrasilAPI)"
    echo -e "  ${AMARELO}--cep <CEP>${RESET}       -> CEP (ViaCEP)"
    echo -e "  ${AMARELO}--cpf <CPF>${RESET}       -> Valida CPF + UF"
    echo -e "  ${AMARELO}--fipe <CODIGO>${RESET}   -> Preco FIPE do veiculo"
    echo -e "  ${AMARELO}--dominio <DOM>${RESET}   -> DNS + WHOIS"
    echo -e "  ${AMARELO}--email <EMAIL>${RESET}   -> MX + Gravatar + HIBP"
    echo -e "  ${AMARELO}--telefone <NUM>${RESET}  -> DDD + cidades"
    echo -e "  ${AMARELO}--redes <USER>${RESET}    -> Username nas redes"
    echo -e "  ${AMARELO}--tempo <CIDADE>${RESET}  -> Previsao do tempo"
    echo -e "  ${AMARELO}--banco <COD>${RESET}     -> Nome do banco (ISPB)"
    echo -e "  ${AMARELO}--cotacoes${RESET}        -> Dolar, Euro, BTC"
    echo -e "  ${AMARELO}--rastreio <COD>${RESET}  -> Rastreio de encomenda"
    echo -e "  ${AMARELO}--feriados [ANO]${RESET}  -> Feriados nacionais"
    echo -e "  ${AMARELO}--ssl <DOM>${RESET}       -> Certificado SSL"
    echo -e "  ${AMARELO}--rdap <DOM>${RESET}      -> WHOIS JSON via RDAP"
    echo -e "  ${AMARELO}--portas <ALVO>${RESET}   -> Portas comuns abertas"
    echo -e "  ${AMARELO}--target <VALOR>${RESET}  -> Auto-detecta e consulta"
    echo -e "  ${AMARELO}--historico${RESET}       -> Historico de consultas"
    echo -e "  ${AMARELO}--update${RESET}          -> Atualiza do GitHub"
    echo ""
    echo -e "${VERDE}Exemplos:${RESET}"
    echo "  bash cybertrace.sh --ip 8.8.8.8"
    echo "  bash cybertrace.sh --target 52998224725"
    echo "  bash cybertrace.sh --cotacoes"
    echo "  bash cybertrace.sh --ddd 11"
    exit 0
}

# ============================================================
# DDD (BrasilAPI) - substitui a tabela fixa do v2.3
# ============================================================
consultar_ddd() {
    local ddd="$1"
    if [[ ! "$ddd" =~ ^[0-9]{2}$ ]]; then
        echo -e "${VERMELHO}DDD invalido.${RESET}"
        return 1
    fi
    local data
    data=$(api_get "https://brasilapi.com.br/api/ddd/v1/$ddd")
    if echo "$data" | python3 -c "import sys,json; json.load(sys.stdin)" 2>/dev/null; then
        echo "$data" | python3 -c "
import sys, json
d = json.load(sys.stdin)
uf = d.get('state','')
cities = d.get('cities', [])
print('  UF     : ' + uf)
print('  Cidades: ' + (', '.join(cities) if cities else '-'))
" 2>/dev/null
    else
        echo -e "${AMARELO}  DDD nao encontrado na BrasilAPI.${RESET}"
    fi
}

# ============================================================
# TELEFONE (DDD dinamico)
# ============================================================
buscar_telefone() {
    banner
    section "CONSULTAR TELEFONE (DDD dinamico)"
    echo -e "${AMARELO}Formato: 55 11 999999999 (pais DDD numero)${RESET}"
    echo -ne "${AMARELO}Numero: ${RESET}"
    read -r tel
    tel=$(echo "$tel" | tr -d ' +-')
    if [[ ${#tel} -lt 12 ]]; then
        echo -e "${VERMELHO}Numero muito curto (use codigo do pais + DDD)${RESET}"
        press_enter
        return
    fi
    local pais="${tel:0:2}"
    local ddd="${tel:2:2}"
    local numero="${tel:4}"
    linha
    echo -e "${AMARELO}Numero completo:${RESET} +$tel"
    echo -e "${AMARELO}Pais:${RESET} $( [[ "$pais" == "55" ]] && echo "Brasil" || echo "$pais" )"
    echo -e "${AMARELO}DDD:${RESET} $ddd"
    echo -e "${AMARELO}Numero:${RESET} $numero"
    echo -e "${AMARELO}Tipo:${RESET} $( [[ ${#numero} -eq 9 ]] && echo "Celular" || echo "Fixo" )"
    linha
    echo ""
    echo -e "${CIANO}Cidades do DDD $ddd:${RESET}"
    consultar_ddd "$ddd"
    salvar_historico "telefone: +$tel"
    press_enter
}

# ============================================================
# VEICULO (FIPE por codigo - corrige o bug da placa)
# ============================================================
buscar_veiculo() {
    banner
    section "VEICULO - PRECO FIPE (codigo)"
    echo -e "${AMARELO}Dados por placa exigem Detran (pago/LGPD).${RESET}"
    echo -e "${CIANO}Consulte o preco FIPE pelo CODIGO, achado em:${RESET}"
    echo -e "${CIANO}  https://veiculos.fipe.org.br${RESET}"
    echo -n "${AMARELO}Codigo FIPE (ex: 001004-0): ${RESET}"
    read -r cod
    [[ -z "$cod" ]] && { echo -e "${VERMELHO}Invalido${RESET}"; press_enter; return; }
    echo -e "${CIANO}Consultando BrasilAPI/FIPE...${RESET}"
    if cli_fipe "$cod"; then
        salvar_historico "FIPE: $cod"
    fi
    press_enter
}

# ============================================================
# CNPJ (BrasilAPI)
# ============================================================
cli_cnpj() {
    local cnpj="$1"
    local data
    data=$(api_get "https://brasilapi.com.br/api/cnpj/v1/$cnpj")
    if echo "$data" | python3 -c "import sys,json; d=json.load(sys.stdin); exit(0 if 'cnpj' in d else 1)" 2>/dev/null; then
        echo "$data" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('=' * 60)
print('  CNPJ        : %s' % d.get('cnpj',''))
print('  Razao Social: %s' % d.get('razao_social',''))
print('  Fantasia    : %s' % d.get('nome_fantasia',''))
print('  Endereco    : %s, %s - %s' % (d.get('logradouro',''), d.get('numero',''), d.get('bairro','')))
print('  Cidade/UF   : %s/%s - %s' % (d.get('municipio',''), d.get('uf',''), d.get('cep','')))
print('  Telefone    : %s' % d.get('ddd_telefone_1',''))
print('  Email       : %s' % d.get('email',''))
print('  Porte       : %s' % d.get('porte',''))
print('  Abertura    : %s' % d.get('data_inicio_atividade',''))
print('  Situacao    : %s' % d.get('situacao_cadastral',''))
print('  Capital     : R$ %s' % d.get('capital_social',''))
print('  CNAE        : %s - %s' % (d.get('cnae_fiscal',''), d.get('cnae_fiscal_descricao','')))
print('=' * 60)
" 2>/dev/null
    else
        echo -e "${VERMELHO}CNPJ nao encontrado ou invalido.${RESET}"
    fi
}

buscar_cnpj() {
    banner
    section "CNPJ REAL (BrasilAPI - Receita Federal)"
    echo -ne "${AMARELO}CNPJ (14 digitos): ${RESET}"
    read -r cnpj
    cnpj=$(echo "$cnpj" | tr -d ' ./-')
    if [[ ${#cnpj} -ne 14 ]]; then
        echo -e "${VERMELHO}CNPJ deve ter 14 digitos${RESET}"
        press_enter
        return
    fi
    echo -e "${CIANO}Consultando Receita Federal via BrasilAPI...${RESET}"
    cli_cnpj "$cnpj"
    salvar_historico "CNPJ: $cnpj"
    press_enter
}

# ============================================================
# CPF (validacao de digitos + UF)
# ============================================================
cli_cpf() {
    local cpf
    cpf=$(echo "$1" | tr -d ' .-')
    python3 -c "
import sys
cpf = sys.argv[1]
if len(cpf) != 11 or not cpf.isdigit():
    print('ERRO: CPF deve ter 11 digitos')
    sys.exit(1)
d1, d2 = int(cpf[9]), int(cpf[10])
r1 = (sum(int(cpf[i])*(10-i) for i in range(9))*10) % 11
r2 = (sum(int(cpf[i])*(11-i) for i in range(10))*10) % 11
if r1 == 10: r1 = 0
if r2 == 10: r2 = 0
v = (r1 == d1 and r2 == d2)
e = {0:'RS',1:'DF/GO/MS/MT',2:'PA/AM/AC/RO/RR',3:'CE/MA/PI',4:'PE/PB/RN/AL',5:'BA/SE',6:'MG',7:'RJ/ES',8:'SP',9:'PR/SC'}
print('CPF: %s.%s.%s-%s' % (cpf[:3], cpf[3:6], cpf[6:9], cpf[9:]))
print('Valido: %s' % ('SIM' if v else 'NAO'))
if v:
    print('UF emissor: %s' % e.get(int(cpf[8]), 'Desconhecido'))
" "$cpf" 2>/dev/null
}

validar_cpf() {
    banner
    section "VALIDACAO DE CPF"
    echo -e "${VERMELHO}[!] Dados reais de CPF sao protegidos por lei (LGPD)${RESET}"
    echo -n "${AMARELO}CPF (11 digitos): ${RESET}"
    read -r cpf
    cpf=$(echo "$cpf" | tr -d ' .-')
    if [[ ${#cpf} -ne 11 ]]; then
        echo -e "${VERMELHO}CPF invalido${RESET}"
        press_enter
        return
    fi
    linha
    cli_cpf "$cpf"
    linha
    salvar_historico "CPF: $cpf"
    press_enter
}

# ============================================================
# DOMINIO (DNS + WHOIS)
# ============================================================
cli_dominio() {
    local dom="$1"
    local ip
    ip=$(timeout 6 dig +short "$dom" 2>/dev/null | head -1)
    linha
    echo -e "${AMARELO}Dominio:${RESET} $dom"
    echo -e "${AMARELO}IP:${RESET} ${ip:-Nao resolvido}"
    echo ""
    echo -e "${CIANO}Registros DNS:${RESET}"
    echo -e "${AMARELO}MX:${RESET}"
    timeout 6 dig +short MX "$dom" 2>/dev/null | while read -r l; do echo "   $l"; done
    echo -e "${AMARELO}NS:${RESET}"
    timeout 6 dig +short NS "$dom" 2>/dev/null | while read -r l; do echo "   $l"; done
    echo -e "${AMARELO}TXT (5):${RESET}"
    timeout 6 dig +short TXT "$dom" 2>/dev/null | head -5 | while read -r l; do echo "   $l"; done
    echo ""
    if command -v whois &>/dev/null; then
        echo -e "${CIANO}WHOIS (resumo):${RESET}"
        timeout 8 whois "$dom" 2>/dev/null | grep -iE "registrant|owner|email|created|expir|name|organization|status" | head -8
    else
        echo -e "${AMARELO}whois nao instalado - use RDAP para mais dados.${RESET}"
    fi
    linha
}

buscar_dominio() {
    banner
    section "CONSULTAR DOMINIO (DNS + WHOIS)"
    echo -n "${AMARELO}Dominio: ${RESET}"
    read -r dom
    [[ -z "$dom" ]] && { echo -e "${VERMELHO}Invalido${RESET}"; press_enter; return; }
    cli_dominio "$dom"
    salvar_historico "dominio: $dom"
    press_enter
}

# ============================================================
# CEP (ViaCEP)
# ============================================================
cli_cep() {
    local cep="$1"
    local data
    data=$(api_get "https://viacep.com.br/ws/$cep/json/")
    if echo "$data" | python3 -c "import sys,json; d=json.load(sys.stdin); exit(0 if 'erro' not in d else 1)" 2>/dev/null; then
        echo "$data" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('=' * 60)
print('  CEP     : %s' % d.get('cep',''))
print('  Rua     : %s' % d.get('logradouro',''))
print('  Bairro  : %s' % d.get('bairro',''))
print('  Cidade  : %s' % d.get('localidade',''))
print('  UF      : %s (%s)' % (d.get('uf',''), d.get('estado','')))
print('  DDD     : %s' % d.get('ddd',''))
print('  IBGE    : %s' % d.get('ibge',''))
print('=' * 60)
" 2>/dev/null
    else
        echo -e "${VERMELHO}CEP nao encontrado.${RESET}"
    fi
}

buscar_cep() {
    banner
    section "CONSULTAR CEP (ViaCEP API)"
    echo -n "${AMARELO}CEP: ${RESET}"
    read -r cep
    cep=$(echo "$cep" | tr -d ' -')
    if [[ ${#cep} -ne 8 ]]; then
        echo -e "${VERMELHO}CEP deve ter 8 digitos${RESET}"
        press_enter
        return
    fi
    echo -e "${CIANO}Consultando ViaCEP...${RESET}"
    cli_cep "$cep"
    salvar_historico "CEP: $cep"
    press_enter
}

# ============================================================
# BANCO (ISPB - BrasilAPI) - NOVO
# ============================================================
cli_banco() {
    local cod="$1"
    local data
    data=$(api_get "https://brasilapi.com.br/api/banks/v1/$cod")
    if echo "$data" | python3 -c "import sys,json; d=json.load(sys.stdin); exit(0 if 'name' in d else 1)" 2>/dev/null; then
        echo "$data" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('=' * 60)
print('  Codigo: %s' % d.get('code',''))
print('  Banco : %s' % d.get('name',''))
print('  ISPB  : %s' % d.get('ispb',''))
print('  Nome  : %s' % d.get('fullName',''))
print('=' * 60)
" 2>/dev/null
        return 0
    fi
    return 1
}

consultar_banco() {
    banner
    section "CONSULTAR BANCO (BrasilAPI)"
    echo -e "${AMARELO}Ex: 260 Nubank, 341 Itau, 237 Bradesco, 001 BB${RESET}"
    echo -n "${AMARELO}Codigo do banco: ${RESET}"
    read -r cod
    [[ -z "$cod" ]] && { echo -e "${VERMELHO}Invalido${RESET}"; press_enter; return; }
    echo -e "${CIANO}Consultando...${RESET}"
    if cli_banco "$cod"; then
        salvar_historico "banco: $cod"
    else
        echo -e "${VERMELHO}Banco nao encontrado (tente 001, 237, 341, 260).${RESET}"
    fi
    press_enter
}

# ============================================================
# DDD (menu) - NOVO
# ============================================================
buscar_ddd() {
    banner
    section "DDD + CIDADES (BrasilAPI)"
    echo -n "${AMARELO}DDD: ${RESET}"
    read -r ddd
    [[ -z "$ddd" ]] && { echo -e "${VERMELHO}Invalido${RESET}"; press_enter; return; }
    salvar_historico "DDD: $ddd"
    consultar_ddd "$ddd"
    press_enter
}

# ============================================================
# COTACOES (AwesomeAPI) - NOVO
# ============================================================
cli_cotacoes() {
    local data
    data=$(api_get "https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL")
    if echo "$data" | python3 -c "import sys,json; json.load(sys.stdin)" 2>/dev/null; then
        echo "$data" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('=' * 60)
for k in ('USDBRL','EURBRL','BTCBRL'):
    v = d.get(k, {})
    if v:
        print('  %-5s: R$ %s (variacao %s%%)' % (v.get('code',''), v.get('bid',''), v.get('pctChange','')))
print('=' * 60)
" 2>/dev/null
        return 0
    fi
    return 1
}

cotacoes() {
    banner
    section "COTACOES (Dolar, Euro, BTC)"
    if cli_cotacoes; then
        salvar_historico "cotacoes"
    else
        echo -e "${VERMELHO}Erro ao consultar cotacoes.${RESET}"
    fi
    press_enter
}

# ============================================================
# RASTREIO (Linketrack API gratuita) - NOVO
# ============================================================
cli_rastreio() {
    local cod="$1"
    local data
    # Credenciais: use LINKETRACK_USER/LINKETRACK_TOKEN do ambiente se existirem
    local user="${LINKETRACK_USER:-teste}"
    local token="${LINKETRACK_TOKEN:-teste}"
    data=$(curl -s --max-time 15 "https://api.linketrack.com/track/json?user=$user&token=$token&codigo=$cod" 2>/dev/null)
    if echo "$data" | python3 -c "import sys,json; d=json.load(sys.stdin); exit(0 if d.get('eventos') else 1)" 2>/dev/null; then
        echo "$data" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('=' * 60)
print('  Codigo : %s' % d.get('codigo',''))
print('  Servico: %s' % d.get('servico',''))
print('  Eventos:')
for e in d.get('eventos', [])[:8]:
    print('    [%s %s] %s' % (e.get('data',''), e.get('hora',''), e.get('local','')))
    print('        %s' % e.get('status',''))
print('=' * 60)
" 2>/dev/null
        return 0
    fi
    echo -e "${AMARELO}Dica: cadastre-se gratis em linketrack.com e rode:${RESET}"
    echo -e "${AMARELO}  LINKETRACK_USER=seu LINKETRACK_TOKEN=seu bash cybertrace.sh --rastreio CODIGO${RESET}"
    return 1
}

rastrear() {
    banner
    section "RASTREAR ENCOMENDA (Correios)"
    echo -e "${AMARELO}Codigo: LU123456789BR (PAC/SEDEX)${RESET}"
    echo -n "${AMARELO}Codigo de rastreio: ${RESET}"
    read -r cod
    [[ -z "$cod" ]] && { echo -e "${VERMELHO}Invalido${RESET}"; press_enter; return; }
    echo -e "${CIANO}Rastreando...${RESET}"
    if cli_rastreio "$cod"; then
        salvar_historico "rastreio: $cod"
    else
        echo -e "${VERMELHO}Nao encontrado (confira o codigo ou tente de novo).${RESET}"
    fi
    press_enter
}

# ============================================================
# FERIADOS (BrasilAPI) - NOVO
# ============================================================
cli_feriados() {
    local ano="$1"
    local data
    data=$(api_get "https://brasilapi.com.br/api/feriados/v1/$ano")
    if echo "$data" | python3 -c "import sys,json; d=json.load(sys.stdin); exit(0 if isinstance(d,list) and d else 1)" 2>/dev/null; then
        echo "$data" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('=' * 60)
for f in d:
    print('  %s  %s' % (f.get('date',''), f.get('name','')))
print('=' * 60)
" 2>/dev/null
        return 0
    fi
    return 1
}

feriados() {
    banner
    section "FERIADOS NACIONAIS"
    echo -n "${AMARELO}Ano (padrao: atual): ${RESET}"
    read -r ano
    ano="${ano:-$(date +%Y)}"
    echo -e "${CIANO}Buscando feriados de $ano...${RESET}"
    if cli_feriados "$ano"; then
        salvar_historico "feriados $ano"
    else
        echo -e "${VERMELHO}Erro ao buscar feriados.${RESET}"
    fi
    press_enter
}

# ============================================================
# SSL (certificado) - NOVO
# ============================================================
cli_ssl() {
    local dom="$1"
    if ! command -v openssl &>/dev/null; then
        echo -e "${VERMELHO}openssl nao encontrado (pkg install openssl-tool).${RESET}"
        return 1
    fi
    local saida
    saida=$(echo | timeout 12 openssl s_client -servername "$dom" -connect "$dom:443" 2>/dev/null | openssl x509 -noout -dates -issuer 2>/dev/null)
    if [[ -n "$saida" ]]; then
        linha
        echo "$saida"
        linha
        return 0
    fi
    return 1
}

ssl_certificado() {
    banner
    section "CERTIFICADO SSL"
    echo -n "${AMARELO}Dominio: ${RESET}"
    read -r dom
    [[ -z "$dom" ]] && { echo -e "${VERMELHO}Invalido${RESET}"; press_enter; return; }
    echo -e "${CIANO}Verificando certificado de $dom...${RESET}"
    if cli_ssl "$dom"; then
        salvar_historico "ssl: $dom"
    else
        echo -e "${VERMELHO}Nao foi pos
