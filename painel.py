import os
import socket
import urllib.request
import urllib.error
from urllib.parse import urlparse
import sys
import time
import subprocess

class Painel1:
    def __init__ ( self ) :
        # Cores ANSI - Estilo Kali Linux
        self.C_KALI = "\033[38;5;33m"     # Azul Kali
        self.C_RED = "\033[38;5;196m"     # Vermelho
        self.C_GREEN = "\033[38;5;46m"    # Verde Neon
        self.C_YELLOW = "\033[38;5;226m"  # Amarelo
        self.C_GRAY = "\033[38;5;242m"    # Cinza
        self.C_WHITE = "\033[1;37m"       # Branco Negrito
        self.C_PINK = "\033[38;5;206m"    # Rosa
        self.RESET = "\033[0m"

        # Senha padrão do seu painel
        self.SENHA_CORRETA = "203159"

    def obter_marca_celular ( self ) :
        """Obtém a marca e o modelo do celular via comandos do Android"""
        try:
            marca = subprocess.check_output ( "getprop ro.product.brand", shell=True ) .decode (  ) .strip (  ) .capitalize ( )
            modelo = subprocess.check_output ( "getprop ro.product.model", shell=True ) .decode (  ) .strip ( )
            
            if marca and modelo:
                return f"{marca} ({modelo} ) "
            elif marca:
                return marca
            else:
                return "Android Device"
        except Exception:
            return "Android Device"

    def tocar_som_entrada ( self ) :
        """Saudação em voz compatível com Termux e PyCode"""
        mensagem = "Olá Eraz! Acesso concedido. Bem-vindo ao seu painel."
        
        # Tentativa 1: Voz via Termux
        res = os.system ( f"termux-tts-speak -l pt '{mensagem}' >/dev/null 2>&1 &")
        
        # Tentativa 2: Se estiver no PyCode / Pydroid e o Termux não responder
        if res != 0:
            try:
                import pyttsx3
                engine = pyttsx3.init ( )
                engine.say ( mensagem)
                engine.runAndWait ( )
            except Exception:
                print ( "\a")

    def autenticar ( self ) :
        """Sistema de Login com limite de 3 tentativas"""
        tentativas = 0
        max_tentativas = 3

        while tentativas < max_tentativas:
            os.system ( 'clear')
            self.banner ( )
            print ( f"{self.C_RED}┌── ( {self.C_RED}kali🔒scxveryx{self.C_RED} ) -[{self.C_RED}login{self.C_RED}]{self.RESET}")
            senha = input ( f"{self.C_RED}└─{self.C_RED}$ {self.RESET}Digite a senha de acesso: " ) .strip ( )

            if senha == self.SENHA_CORRETA:
                print ( f"\n{self.C_RED}[+] Acesso concedido! Carregando o painel...{self.RESET}")
                self.tocar_som_entrada ( )
                time.sleep ( 1.5)
                return True
            else:
                tentativas += 1
                restantes = max_tentativas - tentativas
                print ( f"\n{self.C_RED}[!] Senha incorreta! Tentativas restantes: {restantes}{self.RESET}")
                time.sleep ( 1.5)

        os.system ( 'clear')
        print ( f"\n{self.C_RED}=====================================================")
        print ( " [!] ALERTA DE SEGURANÇA: TENTATIVA DE INVASÃO DETECTADA")
        print ( " [!] Acesso Bloqueado! Você errou a senha 3 vezes.")
        print ( f"====================================================={self.RESET}\n")
        sys.exit ( )

    def banner ( self ) :
        """Cabeçalho em ASCII Art Ajeitado com a mensagem"""
        dispositivo = self.obter_marca_celular ( )
        
        print ( f" {self.C_RED}██▓ ███▄ ▄███▓ ██▓███   █    ██ ▄▄▄█████▓ ███▄ ▄███▓ ██▓ ██▓     ██▓    ▓█████  ██▀███  
                              ▓██▒▓██▒▀█▀ ██▒▓██░  ██▒ ██  ▓██▒▓  ██▒ ▓▒▓██▒▀█▀ ██▒▓██▒▓██▒    ▓██▒    ▓█   ▀ ▓██ ▒ ██▒
                              ▒██▒▓██    ▓██░▓██░ ██▓▒▓██  ▒██░▒ ▓██░ ▒░▓██    ▓██░▒██▒▒██░    ▒██░    ▒███   ▓██ ░▄█ ▒
                              ░██░▒██    ▒██ ▒██▄█▓▒ ▒▓▓█  ░██░░ ▓██▓ ░ ▒██    ▒██ ░██░▒██░    ▒██░    ▒▓█  ▄ ▒██▀▀█▄  
                              ░██░▒██▒   ░██▒▒██▒ ░  ░▒▒█████▓   ▒██▒ ░ ▒██▒   ░██▒░██░░██████▒░██████▒░▒████▒░██▓ ▒██▒
                              ░▓  ░ ▒░   ░  ░▒▓▒░ ░  ░░▒▓▒ ▒ ▒   ▒ ░░   ░ ▒░   ░  ░░▓  ░ ▒░▓  ░░ ▒░▓  ░░░ ▒░ ░░ ▒▓ ░▒▓░
                              ▒ ░░  ░      ░░▒ ░     ░░▒░ ░ ░     ░    ░  ░      ░ ▒ ░░ ░ ▒  ░░ ░ ▒  ░ ░ ░  ░  ░▒ ░ ▒░
                              ▒ ░░      ░   ░░        ░░░ ░ ░   ░      ░      ░    ▒ ░  ░ ░     ░ ░      ░     ░░   ░ 
                              ░         ░               ░                     ░    ░      ░  ░    ░  ░   ░  ░   ░ {self.RESET}")
        print ( f"{self.C_RED}====================================================={self.RESET}")
        print ( f" {self.C_RED}[+] {self.C_RED}Dev:{self.RESET}{self.C_RED}scxveryx{self.RESET}")
        print ( f" {self.C_RED}[+] Ip tracked{self.RESET}")
        print ( f" {self.C_RED}[+] Dispositivo:{self.RESET} {self.C_RED}{dispositivo}{self.RESET}")
        print ( f" {self.C_RED}[+] OS Target:{self.C_RED} computer {self.RESET}")
        print ( f"{self.C_RED}====================================================={self.RESET}\n")

    def limpar_alvo ( self, alvo ) :
        """Sanitiza e limpa a URL fornecida"""
        alvo = alvo.strip ( )
        if not alvo.startswith ( "http://") and not alvo.startswith ( "https://" ) :
            alvo = "http://" + alvo
        try:
            parsed = urlparse ( alvo)
            host = parsed.hostname
            return host if host else ""
        except Exception:
            return ""

    def scan_portas_nativo ( self, alvo ) :
        """Escaneia as portas TCP sem travar o terminal"""
        alvo_limpo = self.limpar_alvo ( alvo)
        if not alvo_limpo:
            print ( f"{self.C_RED}[-] Endereço do alvo é inválido.{self.RESET}")
            return

        print ( f"\n{self.C_RED}[*] [SCAN] Iniciando varredura em: {self.C_WHITE}{alvo_limpo}{self.RESET}\n")
        portas = [21, 22, 23, 25, 53, 80, 110, 443, 8080, 3306]
        
        try:
            ip = socket.gethostbyname ( alvo_limpo)
            print ( f"{self.C_RED}[+] Target IP: {ip}{self.RESET}\n")
        except socket.gaierror:
            print ( f"{self.C_RED}[-] Falha ao resolver o endereço IP do alvo.{self.RESET}")
            return

        print ( f"{self.C_RED}PORTA     SERVIÇO      STATUS{self.RESET}")
        print ( f"{self.C_RED}-----------------------------------{self.RESET}")
        
        servicos = {21:"FTP", 22:"SSH", 23:"TELNET", 25:"SMTP", 53:"DNS", 80:"HTTP", 110:"POP3", 443:"HTTPS", 8080:"PROXY", 3306:"MYSQL"}

        for porta in portas:
            try:
                s = socket.socket ( socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout ( 0.6)
                resultado = s.connect_ex (  ( ip, porta ) )
                
                nome_serv = servicos.get ( porta, "DESCONHECIDO")
                if resultado == 0:
                    print ( f"{porta:<9} {nome_serv:<12} {self.C_GREEN}[ ABERTA ]{self.RESET}")
                else:
                    print ( f"{porta:<9} {nome_serv:<12} {self.C_RED}[ fechada ]{self.RESET}")
                s.close ( )
            except KeyboardInterrupt:
                print ( f"\n{self.C_RED}[!] Scan interrompido.{self.RESET}")
                break
            except Exception:
                print ( f"{porta:<9} {nome_serv:<12} {self.C_YELLOW}[ ERRO ]{self.RESET}")

    def testar_ping ( self, alvo ) :
        """Busca o IP do alvo"""
        alvo_limpo = self.limpar_alvo ( alvo)
        if not alvo_limpo:
            print ( f"{self.C_RED}[-] Endereço do alvo é inválido.{self.RESET}")
            return

        print ( f"\n{self.C_RED}[*] [PING] Resolvendo endereço IP...{self.RESET}\n")
        try:
            ip = socket.gethostbyname ( alvo_limpo)
            print ( f" {self.C_RED}[+] HOST ATIVO:{self.RESET} {alvo_limpo} {self.C_GRAY}-->{self.RESET} {ip}")
        except Exception:
            print ( f" {self.C_RED}[-] HOST INATIVO OU INEXISTENTE{self.RESET}")

    def obter_headers ( self, alvo ) :
        """Captura os cabeçalhos HTTP do servidor web"""
        alvo_limpo = self.limpar_alvo ( alvo)
        if not alvo_limpo:
            print ( f"{self.C_RED}[-] Endereço do alvo é inválido.{self.RESET}")
            return

        print ( f"\n{self.C_RED}[*] [HTTP RECON] Analisando Headers da Aplicação...{self.RESET}\n")
        
        import ssl
        ctx = ssl.create_default_context ( )
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        url = f"http://{alvo_limpo}"
        try:
            req = urllib.request.Request ( url, headers={'User-Agent': 'Mozilla/5.0 (KaliLinux ) '})
            with urllib.request.urlopen ( req, timeout=4, context=ctx) as res:
                headers = res.info ( )
                print ( f" {self.C_RED}[+] Server:{self.RESET} {headers.get ( 'Server', 'Desconhecido' ) }")
                print ( f" {self.C_RED}[+] Powered-By:{self.RESET} {headers.get ( 'X-Powered-By', 'Não detectado' ) }")
                print ( f" {self.C_RED}[+] Content-Type:{self.RESET} {headers.get ( 'Content-Type', 'Não informado' ) }")
        except urllib.error.HTTPError as e:
            print ( f" {self.C_RED}[!] Código HTTP: {e.code}{self.RESET}")
        except urllib.error.URLError as e:
            print ( f" {self.C_RED}[-] Erro de conexão/URL: {e.reason}{self.RESET}")
        except Exception as e:
            print ( f" {self.C_RED}[-] Erro na requisição Web: {e}{self.RESET}")

    def scan_rede_local ( self ) :
        """Varre a rede Wi-Fi local procurando aparelhos/IPs ativos"""
        print ( f"\n{self.C_RED}[*] [LAN SCAN] Varrendo a rede Wi-Fi local por dispositivos ativos...{self.RESET}\n")
        
        try:
            s = socket.socket ( socket.AF_INET, socket.SOCK_DGRAM)
            s.connect (  ( "8.8.8.8", 80 ) )
            ip_local = s.getsockname (  ) [0]
            s.close ( )
            prefixo = ".".join ( ip_local.split ( "." ) [:-1]) + "."
        except Exception:
            prefixo = "192.168.0."
            ip_local = ""

        print ( f"{self.C_RED}IP DISPOSITIVO            STATUS           INFO{self.RESET}")
        print ( f"{self.C_RED}-----------------------------------------------------{self.RESET}")

        encontrados = 0
        for i in range ( 1, 255 ) :
            ip_teste = f"{prefixo}{i}"
            try:
                sock = socket.socket ( socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout ( 0.04)
                resultado = sock.connect_ex (  ( ip_teste, 80 ) )
                sock.close ( )

                if resultado == 0 or ip_teste == ip_local:
                    info = f"{self.C_RED} ( Seu Celular ) {self.RESET}" if ip_teste == ip_local else f"{self.C_GRAY} ( Dispositivo na Rede ) {self.RESET}"
                    print ( f"{ip_teste:<25} {self.C_RED}[ ATIVO ]{self.RESET}      {info}")
                    encontrados += 1
            except KeyboardInterrupt:
                print ( f"\n{self.C_RED}[!] Varredura cancelada.{self.RESET}")
                break
            except Exception:
                pass

        print ( f"{self.C_RED}-----------------------------------------------------{self.RESET}")
        print ( f"\n{self.C_RED}[+] Concluído! Dispositivos ativos encontrados: {encontrados}{self.RESET}")

    def abrir_interface ( self ) :
        self.autenticar ( )

        while True:
            os.system ( 'clear')
            self.banner ( )
            
            print ( f"{self.C_RED}┌── ( {self.C_RED}kali㉿scxveryx{self.C_RED} ) -[{self.C_RED}~/painel{self.C_RED}]{self.RESET}")
            print ( f"{self.C_RED}└─► Opções disponíveis:{self.RESET}\n")
            
            print ( f"  {self.C_RED}[1]{self.RESET} Port Scanner (TCP Nativo ) ")
            print ( f"  {self.C_RED}[2]{self.RESET} Resolver IP / DNS")
            print ( f"  {self.C_RED}[3]{self.RESET} Web Banner Grabbing (HTTP ) ")
            print ( f"  {self.C_RED}[4]{self.RESET} Dispositivos na Rede Local (LAN Scan ) ")
            print ( f"  {self.C_RED}[5]{self.RESET} Limpar Console")
            print ( f"  {self.C_RED}[0]{self.RESET} Encerrar Painel")
            print ( "")

            try:
                opcao = input ( f"{self.C_RED}┌── ( {self.C_RED}kali㉿scxveryx{self.C_RED} ) -[{self.C_RED}menu{self.C_RED}]\n└─{self.C_RED}$ {self.RESET}" ) .strip ( )
            except KeyboardInterrupt:
                print ( f"\n\n{self.C_RED}[!] Encerrando... Até mais, scxveryx!{self.RESET}")
                break
            
            if opcao == '0':
                print ( f"\n{self.C_RED}[!] Encerrando... Até mais, scxveryx!{self.RESET}")
                break
                
            elif opcao == '5':
                continue

            elif opcao == '4':
                self.scan_rede_local ( )
                input ( f"\n{self.C_RED}[Pressione ENTER para retornar ao menu]{self.RESET}")

            elif opcao in ['1', '2', '3']:
                alvo = input ( f"\n{self.C_RED}[?] Digite o Alvo (ex: site.com ou IP ) : {self.RESET}" ) .strip ( )
                if not alvo:
                    continue

                if opcao == '1':
                    self.scan_portas_nativo ( alvo)
                elif opcao == '2':
                    self.testar_ping ( alvo)
                elif opcao == '3':
                    self.obter_headers ( alvo)

                input ( f"\n{self.C_RED}[Pressione ENTER para retornar ao menu]{self.RESET}")
            else:
                print ( f"\n{self.C_RED}[X] Opção inválida.{self.RESET}")
                input ( f"\n{self.C_RED}[Pressione ENTER para continuar]{self.RESET}")

if __name__ == "__main__":
    painel = Painel1 ( )
    painel.abrir_interface (  ) 
