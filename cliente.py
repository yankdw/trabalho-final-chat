import socket
import threading


def cliente_chat():
    HOST = '26.206.166.193'  
    PORTA = 8080            

    nome = input("Digite seu nome: ")
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORTA))


    cliente.send(nome.encode())


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


    while True:
        mensagem = input()
        if mensagem.lower() == "/sair":
            cliente.close()
            break
        cliente.send(mensagem.encode())


cliente_chat()
