import os
import socket
import urllib.request
import urllib.error
from urllib.parse import urlparse
import sys
import time
import subprocess


class Painel1:
    def __init__(self):
       # Cores ANSI - Tema Verde
self.C_KALI = "\033[38;5;46m"      # Verde vivo
self.C_RED = "\033[38;5;82m"       # Verde claro
self.C_GREEN = "\033[38;5;46m"     # Verde
self.C_YELLOW = "\033[38;5;118m"   # Verde-amarelado
self.C_GRAY = "\033[38;5;70m"      # Verde acinzentado
self.C_WHITE = "\033[1;32m"        # Verde claro/negrito
self.C_PINK = "\033[38;5;48m"      # Verde água
self.RESET = "\033[0m"

        self.SENHA_CORRETA = "203159"

    def limpar_console(self):
        os.system("cls" if os.name == "nt" else "clear")

    def obter_marca_celular(self):
        """Obtém a marca e o modelo do celular via Android."""
        try:
            marca = subprocess.check_output(
                ["getprop", "ro.product.brand"],
                stderr=subprocess.DEVNULL
            ).decode().strip().capitalize()

            modelo = subprocess.check_output(
                ["getprop", "ro.product.model"],
                stderr=subprocess.DEVNULL
            ).decode().strip()

            if marca and modelo:
                return f"{marca} ({modelo})"
            elif marca:
                return marca
            else:
                return "Android Device"

        except Exception:
            return "Android Device"

    def tocar_som_entrada(self):
        """Tenta reproduzir uma saudação no Android/Termux."""
        mensagem = "Olá amigo! Acesso concedido. Bem-vindo ao seu painel."

        try:
            resultado = os.system(
                f'termux-tts-speak -l pt "{mensagem}" '
                '>/dev/null 2>&1'
            )

            if resultado != 0:
                raise RuntimeError("Termux TTS indisponível")

        except Exception:
            try:
                import pyttsx3

                engine = pyttsx3.init()
                engine.say(mensagem)
                engine.runAndWait()

            except Exception:
                print("\a")

    def autenticar(self):
        """Sistema de login com limite de 3 tentativas."""
        tentativas = 0
        max_tentativas = 3

        while tentativas < max_tentativas:
            self.limpar_console()
            self.banner()

            print(
                f"{self.C_WHITE}┌──("
                f"{self.C_RED}kali🔒vbought"
                f"{self.C_WHITE})-["
                f"{self.C_KALI}login"
                f"{self.C_WHITE}]{self.RESET}"
            )

            senha = input(
                f"{self.C_WHITE}└─{self.C_GREEN}$ "
                f"{self.RESET}Digite a senha de acesso: "
            ).strip()

            if senha == self.SENHA_CORRETA:
                print(
                    f"\n{self.C_GREEN}"
                    "[+] Acesso concedido! Carregando o painel..."
                    f"{self.RESET}"
                )

                self.tocar_som_entrada()
                time.sleep(1.5)
                return True

            tentativas += 1
            restantes = max_tentativas - tentativas

            print(
                f"\n{self.C_RED}[!] Senha incorreta! "
                f"Tentativas restantes: {restantes}"
                f"{self.RESET}"
            )

            time.sleep(1.5)

        self.limpar_console()

        print(
            f"\n{self.C_RED}"
            "=====================================================\n"
            " [!] ALERTA DE SEGURANÇA: ACESSO BLOQUEADO\n"
            " [!] Você errou a senha 3 vezes.\n"
            "====================================================="
            f"{self.RESET}\n"
        )

        return False

    def banner(self):
        """Exibe o cabeçalho ASCII."""
        dispositivo = self.obter_marca_celular()

        arte = r"""
.... NO! ...                  ... MNO! ...
   ..... MNO!! ...................... MNNOO! ...
 ..... MMNO! ......................... MNNOO!! .
.... MNOONNOO!   MMMMMMMMMMPPPOII!   MNNO!!!! .
 ... !O! NNO! MMMMMMMMMMMMMPPPOOOII!! NO! ....
    ...... ! MMMMMMMMMMMMMPPPPOOOOIII! ! ...
   ........ MMMMMMMMMMMMPPPPPOOOOOOII!! .....
   ........ MMMMMOOOOOOPPPPPPPPOOOOMII! ...
    ....... MMMMM..    OPPMMP    .,OMI! ....
     ...... MMMM::   o.,OPMP,.o   ::I!! ...
         .... NNM:::.,,OOPM!P,.::::!! ....
          .. MMNNNNNOOOOPMO!!IIPPO!!O! .....
         ... MMMMMNNNNOO:!!:!!IPPPPOO! ....
           .. MMMMMNNOOMMNNIIIPPPOO!! ......
          ...... MMMONNMMNNNIIIOO!..........
       ....... MN MOMMMNNNIIIIIO! OO ..........
    ......... MNO! IiiiiiiiiiiiI OOOO ...........
  ...... NNN.MNO! . O!!!!!!!!!O . OONO NO! ........
   .... MNNNNNO! ...OOOOOOOOOOO .  MMNNON!........
   ...... MNNNNO! .. PPPPPPPPP .. MMNON!........
      ...... OO! ................. ON! .......
         ................................
"""

        print(f"{self.C_KALI}{arte}{self.RESET}")

        print(
            f"{self.C_GRAY}"
            "====================================================="
            f"{self.RESET}"
        )

        print(
            f" {self.C_GRAY}[+] {self.C_GRAY} Dev:"
            f"{self.RESET} {self.C_GREEN}vbought{self.RESET}"
        )

        print(
            f" {self.C_GRAY}[+] Dispositivo:"
            f"{self.RESET} {self.C_YELLOW}"
            f"{dispositivo}{self.RESET}"
        )

        print(
            f" {self.C_GRAY}[+] Ambiente:"
            f"{self.RESET} Linux / Android"
        )

        print(
            f"{self.C_GRAY}"
            "====================================================="
            f"{self.RESET}\n"
        )

    def limpar_alvo(self, alvo):
        """Sanitiza a URL fornecida."""
        alvo = alvo.strip()

        if not alvo:
            return ""

        if not alvo.startswith(("http://", "https://")):
            alvo = "http://" + alvo

        try:
            parsed = urlparse(alvo)
            host = parsed.hostname

            return host if host else ""

        except Exception:
            return ""

    def scan_portas_nativo(self, alvo):
        """Verifica algumas portas TCP do host informado."""
        alvo_limpo = self.limpar_alvo(alvo)

        if not alvo_limpo:
            print(
                f"{self.C_RED}"
                "[-] Endereço do alvo é inválido."
                f"{self.RESET}"
            )
            return

        print(
            f"\n{self.C_KALI}[*] [SCAN] "
            f"Iniciando verificação em: "
            f"{self.C_WHITE}{alvo_limpo}{self.RESET}\n"
        )

        portas = [
            21, 22, 23, 25, 53,
            80, 110, 443, 8080, 3306
        ]

        try:
            ip = socket.gethostbyname(alvo_limpo)

            print(
                f"{self.C_GREEN}[+] Target IP: "
                f"{ip}{self.RESET}\n"
            )

        except socket.gaierror:
            print(
                f"{self.C_RED}"
                "[-] Falha ao resolver o endereço."
                f"{self.RESET}"
            )
            return

        servicos = {
            21: "FTP",
            22: "SSH",
            23: "TELNET",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            443: "HTTPS",
            8080: "PROXY",
            3306: "MYSQL"
        }

        print(
            f"{self.C_GRAY}"
            "PORTA     SERVIÇO      STATUS"
            f"{self.RESET}"
        )

        print(
            f"{self.C_GRAY}"
            "-----------------------------------"
            f"{self.RESET}"
        )

        for porta in portas:
            nome_serv = servicos.get(
                porta,
                "DESCONHECIDO"
            )

            try:
                with socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM
                ) as sock:

                    sock.settimeout(0.6)
                    resultado = sock.connect_ex(
                        (ip, porta)
                    )

                if resultado == 0:
                    print(
                        f"{porta:<9} "
                        f"{nome_serv:<12} "
                        f"{self.C_GREEN}"
                        "[ ABERTA ]"
                        f"{self.RESET}"
                    )
                else:
                    print(
                        f"{porta:<9} "
                        f"{nome_serv:<12} "
                        f"{self.C_RED}"
                        "[ FECHADA ]"
                        f"{self.RESET}"
                    )

            except KeyboardInterrupt:
                print(
                    f"\n{self.C_YELLOW}"
                    "[!] Scan interrompido."
                    f"{self.RESET}"
                )
                break

            except Exception as erro:
                print(
                    f"{porta:<9} "
                    f"{nome_serv:<12} "
                    f"{self.C_YELLOW}"
                    f"[ ERRO: {erro} ]"
                    f"{self.RESET}"
                )

    def testar_ping(self, alvo):
        """Resolve o nome do host para um endereço IP."""
        alvo_limpo = self.limpar_alvo(alvo)

        if not alvo_limpo:
            print(
                f"{self.C_RED}"
                "[-] Endereço inválido."
                f"{self.RESET}"
            )
            return

        print(
            f"\n{self.C_KALI}"
            "[*] [DNS] Resolvendo endereço IP..."
            f"{self.RESET}\n"
        )

        try:
            ip = socket.gethostbyname(alvo_limpo)

            print(
                f"{self.C_GREEN}[+] HOST:"
                f"{self.RESET} {alvo_limpo} "
                f"{self.C_GRAY}-->{self.RESET} {ip}"
            )

        except socket.gaierror:
            print(
                f"{self.C_RED}"
                "[-] Host inexistente ou não resolvido."
                f"{self.RESET}"
            )

    def obter_headers(self, alvo):
        """Obtém cabeçalhos HTTP de um servidor."""
        alvo_limpo = self.limpar_alvo(alvo)

        if not alvo_limpo:
            print(
                f"{self.C_RED}"
                "[-] Endereço inválido."
                f"{self.RESET}"
            )
            return

        print(
            f"\n{self.C_KALI}"
            "[*] [HTTP RECON] Obtendo headers..."
            f"{self.RESET}\n"
        )

        url = f"http://{alvo_limpo}"

        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            with urllib.request.urlopen(
                req,
                timeout=4
            ) as resposta:

                headers = resposta.info()

                print(
                    f"{self.C_GREEN}[+] Server:"
                    f"{self.RESET} "
                    f"{headers.get('Server', 'Desconhecido')}"
                )

                print(
                    f"{self.C_GREEN}[+] Powered-By:"
                    f"{self.RESET} "
                    f"{headers.get('X-Powered-By', 'Não detectado')}"
                )

                print(
                    f"{self.C_GREEN}[+] Content-Type:"
                    f"{self.RESET} "
                    f"{headers.get('Content-Type', 'Não informado')}"
                )

        except urllib.error.HTTPError as erro:
            print(
                f"{self.C_YELLOW}"
                f"[!] Código HTTP: {erro.code}"
                f"{self.RESET}"
            )

        except urllib.error.URLError as erro:
            print(
                f"{self.C_RED}"
                f"[-] Erro de conexão: {erro.reason}"
                f"{self.RESET}"
            )

        except Exception as erro:
            print(
                f"{self.C_RED}"
                f"[-] Erro: {erro}"
                f"{self.RESET}"
            )

    def scan_rede_local(self):
        """Verifica dispositivos da rede local."""
        print(
            f"\n{self.C_KALI}"
            "[*] [LAN SCAN] Verificando rede local..."
            f"{self.RESET}\n"
        )

        try:
            with socket.socket(
                socket.AF_INET,
                socket.SOCK_DGRAM
            ) as sock:

                sock.connect(("8.8.8.8", 80))
                ip_local = sock.getsockname()[0]

            prefixo = ".".join(
                ip_local.split(".")[:-1]
            ) + "."

        except Exception:
            prefixo = "192.168.0."
            ip_local = ""

        print(
            f"{self.C_GRAY}"
            "IP DISPOSITIVO       STATUS"
            f"{self.RESET}"
        )

        print(
            f"{self.C_GRAY}"
            "--------------------------------"
            f"{self.RESET}"
        )

        encontrados = 0

        for i in range(1, 255):
            ip_teste = f"{prefixo}{i}"

            try:
                with socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM
                ) as sock:

                    sock.settimeout(0.04)

                    resultado = sock.connect_ex(
                        (ip_teste, 80)
                    )

                if resultado == 0 or ip_teste == ip_local:
                    if ip_teste == ip_local:
                        info = "(Seu dispositivo)"
                    else:
                        info = "(Dispositivo na rede)"

                    print(
                        f"{ip_teste:<20} "
                        f"{self.C_GREEN}"
                        f"[ ATIVO ]"
                        f"{self.RESET} "
                        f"{info}"
                    )

                    encontrados += 1

            except KeyboardInterrupt:
                print(
                    f"\n{self.C_YELLOW}"
                    "[!] Varredura cancelada."
                    f"{self.RESET}"
                )
                break

            except Exception:
                pass

        print(
            f"{self.C_GRAY}"
            "--------------------------------"
            f"{self.RESET}"
        )

        print(
            f"\n{self.C_GREEN}"
            f"[+] Concluído! "
            f"Dispositivos encontrados: {encontrados}"
            f"{self.RESET}"
        )

    def abrir_interface(self):
        if not self.autenticar():
            return

        while True:
            self.limpar_console()
            self.banner()

            print(
                f"{self.C_WHITE}┌──("
                f"{self.C_KALI}kali㉿vbought-termux"
                f"{self.C_WHITE})-["
                f"{self.C_GRAY}~/painel"
                f"{self.C_WHITE}]{self.RESET}"
            )

            print(
                f"{self.C_WHITE}"
                "└─► Opções disponíveis:"
                f"{self.RESET}\n"
            )

            print(
                f"  {self.C_KALI}[1]{self.RESET} "
                "Port Scanner TCP"
            )

            print(
                f"  {self.C_KALI}[2]{self.RESET} "
                "Resolver IP / DNS"
            )

            print(
                f"  {self.C_KALI}[3]{self.RESET} "
                "Web Banner Grabbing"
            )

            print(
                f"  {self.C_KALI}[4]{self.RESET} "
                "Dispositivos na Rede Local"
            )

            print(
                f"  {self.C_KALI}[5]{self.RESET} "
                "Limpar Console"
            )

            print(
                f"  {self.C_RED}[0]{self.RESET} "
                "Encerrar Painel\n"
            )

            try:
                opcao = input(
                    f"{self.C_WHITE}┌──("
                    f"{self.C_KALI}kali㉿vbought"
                    f"{self.C_WHITE})-["
                    f"{self.C_RED}menu"
                    f"{self.C_WHITE}]\n"
                    f"└─{self.C_GREEN}$ "
                    f"{self.RESET}"
                ).strip()

            except KeyboardInterrupt:
                print(
                    f"\n\n{self.C_RED}"
                    "[!] Encerrando..."
                    f"{self.RESET}"
                )
                break

            if opcao == "0":
                print(
                    f"\n{self.C_RED}"
                    "[!] Encerrando..."
                    f"{self.RESET}"
                )
                break

            elif opcao == "5":
                continue

            elif opcao == "4":
                self.scan_rede_local()

                input(
                    f"\n{self.C_GRAY}"
                    "[Pressione ENTER para retornar]"
                    f"{self.RESET}"
                )

            elif opcao in ("1", "2", "3"):
                alvo = input(
                    f"\n{self.C_YELLOW}"
                    "[?] Digite o host ou IP: "
                    f"{self.RESET}"
                ).strip()

                if not alvo:
                    continue

                if opcao == "1":
                    self.scan_portas_nativo(alvo)

                elif opcao == "2":
                    self.testar_ping(alvo)

                elif opcao == "3":
                    self.obter_headers(alvo)

                input(
                    f"\n{self.C_GRAY}"
                    "[Pressione ENTER para retornar]"
                    f"{self.RESET}"
                )

            else:
                print(
                    f"\n{self.C_RED}"
                    "[X] Opção inválida."
                    f"{self.RESET}"
                )

                input(
                    f"\n{self.C_GRAY}"
                    "[Pressione ENTER para continuar]"
                    f"{self.RESET}"
                )


if __name__ == "__main__":
    painel = Painel1()
    painel.abrir_interface()
