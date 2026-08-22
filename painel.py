import os
import time
import urllib.request
import urllib.error
from collections import deque

# ==========================================
# CONFIGURAÇÃO
# ==========================================

URL = "http://127.0.0.1:8000/"
INTERVALO = 1
MAX_RPS = 5

historico = deque(maxlen=15)


# ==========================================
# CORES
# ==========================================

CIANO = "\033[96m"
VERDE = "\033[92m"
AMARELO = "\033[93m"
VERMELHO = "\033[91m"
BRANCO = "\033[97m"
RESET = "\033[0m"


# ==========================================
# TERMINAL
# ==========================================

def limpar():
    os.system("cls" if os.name == "nt" else "clear")


# ==========================================
# TESTE REAL
# ==========================================

def testar_servidor():
    inicio = time.perf_counter()

    try:
        with urllib.request.urlopen(URL, timeout=3) as resposta:
            resposta.read(1024)

        latencia = (time.perf_counter() - inicio) * 1000

        return True, latencia

    except (urllib.error.URLError, TimeoutError):
        return False, None


# ==========================================
# GRÁFICO
# ==========================================

def mostrar_grafico():

    print(f"{CIANO}LATÊNCIA — HISTÓRICO{RESET}")
    print()

    for valor in historico:

        tamanho = min(int(valor / 5), 45)

        if valor < 100:
            cor = VERDE
        elif valor < 300:
            cor = AMARELO
        else:
            cor = VERMELHO

        print(
            f"{valor:6.1f} ms | "
            f"{cor}{'#' * tamanho}{RESET}"
        )


# ==========================================
# PAINEL
# ==========================================

def painel(ok, latencia):

    limpar()

    print(CIANO + "=" * 60 + RESET)
    print(CIANO + "          PAINEL DE MONITORAMENTO" + RESET)
    print(CINZA if False else "")
    print(CIANO + "=" * 60 + RESET)

    print()
    print(f"{BRANCO}ALVO:{RESET} {URL}")
    print(f"{BRANCO}LIMITE:{RESET} {MAX_RPS} teste/s")
    print()

    if ok:
        print(
            VERDE +
            "[✓] SERVIDOR ONLINE"
            + RESET
        )

        print(
            f"{BRANCO}Latência:{RESET} "
            f"{latencia:.1f} ms"
        )

        historico.append(latencia)

    else:
        print(
            VERMELHO +
            "[!] SERVIDOR INDISPONÍVEL"
            + RESET
        )

    print()

    if historico:
        mostrar_grafico()

    print()
    print(CIANO + "=" * 60 + RESET)


# ==========================================
# PRINCIPAL
# ==========================================

def main():

    print(CIANO + "Monitor iniciado." + RESET)
    print(f"Servidor: {URL}")
    print()

    time.sleep(2)

    try:

        while True:

            inicio = time.perf_counter()

            ok, latencia = testar_servidor()

            painel(ok, latencia)

            # Mantém no máximo um teste por segundo
            tempo = time.perf_counter() - inicio
            espera = max(0, INTERVALO - tempo)

            time.sleep(espera)

    except KeyboardInterrupt:

        limpar()

        print(
            VERDE +
            "Monitor encerrado."
            + RESET
        )


if __name__ == "__main__":
    main()
