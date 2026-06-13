import socket as s
from concurrent.futures import ThreadPoolExecutor
import threading

open("resultado_scan.txt", "w").close()

print("Digite o IP ou domínio alvo:")
alvo = s.gethostbyname(input())

print("Digite a porta inicial:")
porta_inicial = int(input())

print("Digite a porta final:")
porta_final = int(input())

print(f"\nEscaneando {alvo}...\n")

porta_aberta_encontrada = False
trava = threading.Lock()

def escanear(porta):
    global porta_aberta_encontrada

    conexao = s.socket(s.AF_INET, s.SOCK_STREAM)
    conexao.settimeout(0.5)

    resultado = conexao.connect_ex((alvo, porta))

    if resultado == 0:
        porta_aberta_encontrada = True

        try:
            servico = s.getservbyport(porta)
        except:
            servico = "desconhecido"

        banner = ""

        if porta in [80, 443, 8080, 8000, 8443, 4433]:
            try:
                conexao.send(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = conexao.recv(1024).decode().strip()
            except:
                pass

        saida = f"\nPorta {porta}:{servico} está aberta."

        if banner:
            saida += f"\nBanner: {banner}"

        with trava:
            print(saida.strip())

            with open("resultado_scan.txt", "a") as arquivo:
                arquivo.write(saida + "\n")

    conexao.close()

with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(escanear, range(porta_inicial, porta_final + 1))

if not porta_aberta_encontrada:
    print("Nenhuma porta aberta encontrada.")
else:
    print("\nEscaneamento concluído.")
    print("Resultados salvos em resultado_scan.txt\n")
