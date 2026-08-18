                    
import os
import socket
import urllib.request
import urllib.error
from urllib.parse import urlparse
import sys
import time
import subprocess
import ssl


class Painel1:
    def __init__(self):
        # Cores ANSI - Estilo Kali Linux
        self.C_CIANO = "\033[38;5;33m"
        self.C_KALI = "\033[38;5;33m"
        self.C_RED = "\033[38;5;196m"
        self.C_GREEN = "\033[38;5;46m"
        self.C_YELLOW = "\033[38;5;226m"
        self.C_GRAY = "\033[38;5;242m"
        self.C_WHITE = "\033[1;37m"
        self.C_PINK = "\033[38;5;206m"
        self.RESET = "\033[0m"

        # Senha padrão do painel
        self.SENHA_CORRETA = "203159"

    def obter_marca_celular(self):
        """Obtém a marca e o modelo do celular via comandos do Android."""
        try:
            marca = subprocess.check_output(
                "getprop ro.product.brand",
                shell=True,
                stderr=subprocess.DEVNULL
            ).decode().strip().capitalize()

            modelo = subprocess.check_output(
                "getprop ro.product.model",
                shell=True,
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
        """Saudação em voz compatível com Termux e PyCode."""
        mensagem = "Olá Eraz! Acesso concedido. Bem-vindo ao seu painel."

        # Tentativa 1: Termux
        resultado = os.system(
            f"termux-tts-speak -l pt '{mensagem}' >/dev/null 2>&1"
        )

        # Tentativa 2: pyttsx3
        if resultado != 0:
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
            os.system("clear")
            self.banner()

            print(
                f"{self.C_RED}┌── ( kali㉿scxveryx ) -[login]{self.RESET}"
            )

            senha = input(
                f"{self.C_RED}└─$ {self.RESET}"
                "Digite a senha de acesso: "
            ).strip()

            if senha == self.SENHA_CORRETA:
                print(
                    f"\n{self.C_GREEN}[+] Acesso concedido! "
                    f"Carregando o painel...{self.RESET}"
                )

                self.tocar_som_entrada()
                time.sleep(1.5)
                return True

            tentativas += 1
            restantes = max_tentativas - tentativas

            print(
                f"\n{self.C_RED}[!] Senha incorreta! "
                f"Tentativas restantes: {restantes}{self.RESET}"
            )

            time.sleep(1.5)

        os.system("clear")

        print(
            f"\n{self.C_RED}"
            "====================================================="
        )
        print(" [!] ALERTA DE SEGURANÇA: TENTATIVA DE INVASÃO DETECTADA")
        print(" [!] Acesso bloqueado! Você errou a senha 3 vezes.")
        print(
            "====================================================="
            f"{self.RESET}\n"
        )

        sys.exit(0)

    def banner(self):
        """Cabeçalho em ASCII Art."""
        dispositivo = self.obter_marca_celular()

        arte = f"""
{self.C_CIANO}
  ░██████   ░██ ░██                                ░██                ░███████                                    
 ░██   ░██  ░██ ░██                                ░██                ░██   ░██                                   
░██     ░██ ░██ ░████████   ░███████      ░████████  ░███████     ░██    ░██  ░███████  ░██    ░██  ░███████  
░██     ░██ ░██ ░██    ░██ ░██    ░██    ░██    ░██ ░██    ░██      ░██    ░██ ░██    ░██ ░██    ░██ ░██        
░██     ░██ ░██ ░██    ░██ ░██    ░██    ░██    ░██ ░█████████     ░██    ░██ ░█████████ ░██    ░██  ░███████  
 ░██   ░██  ░██ ░██    ░██ ░██    ░██    ░██   ░███ ░██              ░██   ░██  ░██        ░██   ░███        ░██ 
  ░██████   ░██ ░██    ░██  ░███████     ░█████░██  ░███████      ░███████    ░███████   ░█████░██  ░███████                                                                                                       
                                                                                                              
        print(arte)

        print(
            f"{self.C_CIANO}"
            "====================================================="
            f"{self.RESET}"
        )

        print(
            f"{self.C_CIANO}[+] Dev:{self.RESET} vantathegod"
        )

        print(
    f"{self.C_CIANO}[+] IP tracked:{self.RESET} "
    "Não disponível"
        )

        print(
            f"{self.C_CIANO}[+] Dispositivo:{self.RESET} "
            f"{dispositivo}"
        )

        print(
            f"{self.C_CIANO}[+] OS Target:{self.RESET} "
            "Android / Terminal"
        )

        print(
            f"{self.C_CIANO}"
            "====================================================="
            f"{self.RESET}\n"
        )

    def limpar_alvo(self, alvo):
        """Sanitiza e obtém o hostname de uma URL."""
        alvo = alvo.strip()

        if not alvo:
            return ""

        if not alvo.startswith(("http://", "https://")):
            alvo = "http://" + alvo

        try:
            parsed = urlparse(alvo)
            host = parsed.hostname

            if host:
                return host

        except Exception:
            pass

        return ""

    def scan_portas_nativo(self, alvo):
        """Escaneia portas TCP comuns do alvo informado."""
        alvo_limpo = self.limpar_alvo(alvo)

        if not alvo_limpo:
            print(
                f"{self.C_CIANO}"
                "[-] Endereço do alvo é inválido."
                f"{self.RESET}"
            )
            return

        print(
            f"\n{self.C_CIANO}[*] [SCAN] "
            f"Iniciando varredura em: "
            f"{self.C_WHITE}{alvo_limpo}{self.RESET}\n"
        )

        portas = [
            21, 22, 23, 25, 53,
            80, 110, 443, 8080, 3306
        ]

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

        try:
            ip = socket.gethostbyname(alvo_limpo)

            print(
                f"{self.C_CIANO}[+] Target IP: "
                f"{self.C_WHITE}{ip}{self.RESET}\n"
            )

        except socket.gaierror:
            print(
                f"{self.C_CIANO}"
                "[-] Falha ao resolver o endereço IP do alvo."
                f"{self.RESET}"
            )
            return

        print(
            f"{self.C_CIANO}"
            "PORTA     SERVIÇO      STATUS"
            f"{self.RESET}"
        )

        print(
            f"{self.C_CIANO}"
            "-----------------------------------"
            f"{self.RESET}"
        )

        for porta in portas:
            try:
                with socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM
                ) as sock:

                    sock.settimeout(0.6)

                    resultado = sock.connect_ex(
                        (ip, porta)
                    )

                nome_serv = servicos.get(
                    porta,
                    "DESCONHECIDO"
                )

                if resultado == 0:
                    status = (
                        f"{self.C_GREEN}"
                        "[ ABERTA ]"
                        f"{self.RESET}"
                    )
                else:
                    status = (
                        f"{self.C_CIANO}"
                        "[ FECHADA ]"
                        f"{self.RESET}"
                    )

                print(
                    f"{porta:<9} "
                    f"{nome_serv:<12} "
                    f"{status}"
                )

            except KeyboardInterrupt:
                print(
                    f"\n{self.C_CIANO}"
                    "[!] Scan interrompido."
                    f"{self.RESET}"
                )
                break

            except Exception as erro:
                print(
                    f"{porta:<9} "
                    f"{'DESCONHECIDO':<12} "
                    f"{self.C_CIANO}[ ERRO ]"
                    f"{self.RESET}"
                )

    def testar_ping(self, alvo):
        """Resolve o IP do alvo."""
        alvo_limpo = self.limpar_alvo(alvo)

        if not alvo_limpo:
            print(
                f"{self.C_CIANO}"
                "[-] Endereço do alvo é inválido."
                f"{self.RESET}"
            )
            return

        print(
            f"\n{self.C_CIANO}"
            "[*] [PING] Resolvendo endereço IP..."
            f"{self.RESET}\n"
        )

        try:
            ip = socket.gethostbyname(alvo_limpo)

            print(
                f" {self.C_CIANO}[+] HOST RESOLVIDO:"
                f"{self.RESET} {alvo_limpo} "
                f"{self.C_CIANO}-->{self.RESET} {ip}"
            )

        except socket.gaierror:
            print(
                f" {self.C_CIANO}"
                "[-] HOST INEXISTENTE OU NÃO RESOLVIDO"
                f"{self.RESET}"
            )

    def obter_headers(self, alvo):
        """Captura cabeçalhos HTTP/HTTPS do servidor web."""
        alvo_limpo = self.limpar_alvo(alvo)

        if not alvo_limpo:
            print(
                f"{self.C_CIANO}"
                "[-] Endereço do alvo é inválido."
                f"{self.RESET}"
            )
            return

        print(
            f"\n{self.C_CIANO}"
            "[*] [HTTP RECON] "
            "Analisando Headers da Aplicação..."
            f"{self.RESET}\n"
        )

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        # Tenta HTTPS primeiro
        urls = [
            f"https://{alvo_limpo}",
            f"http://{alvo_limpo}"
        ]

        for url in urls:
            try:
                req = urllib.request.Request(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0"
                    }
                )

                with urllib.request.urlopen(
                    req,
                    timeout=4,
                    context=ctx
                ) as res:

                    headers = res.info()

                    print(
                        f"{self.C_CIANO}[+] URL:{self.RESET} "
                        f"{url}"
                    )

                    print(
                        f"{self.C_CIANO}[+] Status:{self.RESET} "
                        f"{res.status}"
                    )

                    print(
                        f"{self.C_CIANO}[+] Server:{self.RESET} "
                        f"{headers.get('Server', 'Desconhecido')}"
                    )

                    print(
                        f"{self.C_CIANO}[+] Powered-By:{self.RESET} "
                        f"{headers.get('X-Powered-By', 'Não detectado')}"
                    )

                    print(
                        f"{self.C_CIANO}[+] Content-Type:{self.RESET} "
                        f"{headers.get('Content-Type', 'Não informado')}"
                    )

                    return

            except urllib.error.HTTPError as e:
                print(
                    f"{self.C_CIANO}"
                    f"[!] {url} retornou HTTP {e.code}"
                    f"{self.RESET}"
                )

            except urllib.error.URLError:
                continue

            except Exception as e:
                print(
                    f"{self.C_CIANO}"
                    f"[-] Erro na requisição: {e}"
                    f"{self.RESET}"
                )
                return

        print(
            f"{self.C_CIANO}"
            "[-] Não foi possível conectar ao servidor."
            f"{self.RESET}"
        )

    def scan_rede_local(self):
        """Procura dispositivos na rede local através da porta 80."""
        print(
            f"\n{self.C_CIANO}"
            "[*] [LAN SCAN] "
            "Varrendo a rede Wi-Fi local..."
            f"{self.RESET}\n"
        )

        try:
            s = socket.socket(
                socket.AF_INET,
                socket.SOCK_DGRAM
            )

            s.connect(("8.8.8.8", 80))

            ip_local = s.getsockname()[0]
            s.close()

            prefixo = ".".join(
                ip_local.split(".")[:-1]
            ) + "."

        except Exception:
            prefixo = "192.168.0."
            ip_local = ""

        print(
            f"{self.C_CIANO}"
            "IP DISPOSITIVO            STATUS           INFO"
            f"{self.RESET}"
        )

        print(
            f"{self.C_CIANO}"
            "-----------------------------------------------------"
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
                        info = (
                            f"{self.C_CIANO}"
                            "( Seu Celular )"
                            f"{self.RESET}"
                        )
                    else:
                        info = (
                            f"{self.C_CIANO}"
                            "( Dispositivo na Rede )"
                            f"{self.RESET}"
                        )

                    print(
                        f"{ip_teste:<25} "
                        f"{self.C_CIANO}[ ATIVO ]"
                        f"{self.RESET}      "
                        f"{info}"
                    )

                    encontrados += 1

            except KeyboardInterrupt:
                print(
                    f"\n{self.C_CIANO}"
                    "[!] Varredura cancelada."
                    f"{self.RESET}"
                )
                break

            except Exception:
                pass

        print(
            f"{self.C_CIANO}"
            "-----------------------------------------------------"
            f"{self.RESET}"
        )

        print(
            f"\n{self.C_CIANO}"
            f"[+] Concluído! "
            f"Dispositivos encontrados: {encontrados}"
            f"{self.RESET}"
        )

    def abrir_interface(self):
        """Inicia o painel principal"""
        self.autenticar()

        while True:
            os.system("clear")
            self.banner()

            print(
                f"{self.C_CIANO}"
                "┌── ( kali㉿vantathegod ) -[~/painel]"
                f"{self.RESET}"
            )

            print(
                f"{self.C_CIANO}"
                "└─► DIGA OQUE QUERES, FILHO DE DEUS:"
                f"{self.RESET}\n"
            )

            print(
                f"  {self.C_CIANO}[1]{self.RESET} "
                "PORT SCANNER (TCP Nativo)"
            )

            print(
                f"  {self.C_CIANO}[2]{self.RESET} "
                "RESOLVER IP / DNS"
            )

            print(
                f"  {self.C_CIANO}[3]{self.RESET} "
                "WEB BANNER GRABBING (HTTP)"
            )

            print(
                f"  {self.C_CIANO}[4]{self.RESET} "
                "DISPOSITIVOS NA REDE LOCAL (LAN Scan)"
            )

            print(
                f"  {self.C_CIANO}[5]{self.RESET} "
                "LIMPAR CONSOLE"
            )

            print(
                f"  {self.C_CIANO}[0]{self.RESET} "
                "ENCERRAR PAINEL"
            )

            print()

            try:
                opcao = input(
                    f"{self.C_CIANO}"
                    "┌── ( kali㉿vantathegod ) -[menu]\n"
                    f"└─$ {self.RESET}"
                ).strip()

            except KeyboardInterrupt:
                print(
                    f"\n\n{self.C_CIANO}"
                    "[!] Encerrando... Até mais, scxveryx!"
                    f"{self.RESET}"
                )
                break

            if opcao == "0":
                print(
                    f"\n{self.C_CIANO}"
                    "[!] Encerrando... Até mais, scxveryx!"
                    f"{self.RESET}"
                )
                break

            elif opcao == "5":
                continue

            elif opcao == "4":
                self.scan_rede_local()

                input(
                    f"\n{self.C_CIANO}"
                    "[Pressione ENTER para retornar ao menu]"
                    f"{self.RESET}"
                )

            elif opcao in ["1", "2", "3"]:
                alvo = input(
                    f"\n{self.C_CIANO}"
                    "[?] Digite o Alvo "
                    "(ex: site.com ou IP): "
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
                    f"\n{self.C_CIANO}"
                    "[Pressione ENTER para retornar ao menu]"
                    f"{self.RESET}"
                )

            else:
                print(
                    f"\n{self.C_CIANO}"
                    "[X] Opção inválida."
                    f"{self.RESET}"
                )

                input(
                    f"\n{self.C_CIANO}"
                    "[Pressione ENTER para continuar]"
                    f"{self.RESET}"
                )


if __name__ == "__olho__":
    painel = Painel1()
    painel.abrir_interface()
        
