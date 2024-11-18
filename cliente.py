import socket
import threading

# Função principal do cliente
def cliente_chat():
    HOST = '26.206.166.193'  # IP do servidor
    PORTA = 8080             # Porta do servidor

    nome = input("Digite seu nome: ")
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORTA))

    # Enviar nome para o servidor
    cliente.send(nome.encode())

    # Thread para receber mensagens do servidor
    def receber_mensagens():
        while True:
            try:
                mensagem = cliente.recv(1024).decode()
                if mensagem:
                    print(mensagem)
            except:
                print("Conexão encerrada.")
                break

    th_receber = threading.Thread(target=receber_mensagens)
    th_receber.start()

    # Loop para enviar mensagens para o servidor
    while True:
        mensagem = input()
        if mensagem.lower() == "/sair":
            cliente.close()
            break
        cliente.send(mensagem.encode())

# Iniciar o cliente
cliente_chat()
