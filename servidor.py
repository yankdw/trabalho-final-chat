import socket as sock
import threading as th

def receber_dados(sock_conn, ender):
    try:
        nome = sock_conn.recv(50).decode().strip()
        cliente = {'nome': nome, 'socket': sock_conn}
        lista_cliente.append(cliente)
        print(f"Conexão estabelecida com {nome} ({ender})")

        lista_usuarios = [c['nome'] for c in lista_cliente]
        mensagem_bem_vindo = f"Bem-vindo, {nome}!\nUsuários conectados: {', '.join(lista_usuarios)}"
        broadcast(lista_cliente, mensagem_bem_vindo)

        while True:
            mensagem = sock_conn.recv(1024).decode().strip()
            if not mensagem:
                raise Exception(f"Mensagem vazia de {nome}.")
            print(f"{nome} >> {mensagem}")

            if mensagem.startswith("/remover"):
                try:
                    _, nome_remover = mensagem.split(" ", 1)
                    if nome_remover:
                        remover_usuario_comando(sock_conn, lista_cliente, nome_remover)
                    else:
                        sock_conn.send("Uso incorreto do comando /remover. Formato: /remover <nome>".encode())
                except ValueError:
                    sock_conn.send("Uso incorreto do comando /remover. Formato: /remover <nome>".encode())
            
            elif mensagem.startswith("/unicast"):
                try:
                    _, nome_destinatario, msg = mensagem.split(" ", 2)
                    unicast(lista_cliente, nome_destinatario, f"{nome} (Unicast): {msg}")
                except ValueError:
                    sock_conn.send("Uso incorreto do comando /unicast. Formato: /unicast <nome> <mensagem>".encode())
            
            else:
                broadcast(lista_cliente, f"{nome}: {mensagem}")

    except Exception as e:
        print(f"Erro com o cliente {ender}: {e}")
        remover(cliente, lista_cliente)


def broadcast(lista_cliente, mensagem):
    for cliente in lista_cliente:
        try:
            cliente['socket'].send(mensagem.encode())
        except:
            remover(cliente, lista_cliente)


def remover(cliente, lista_cliente):
    if cliente in lista_cliente:
        lista_cliente.remove(cliente)
        cliente['socket'].close()
        print(f"Cliente {cliente['nome']} removido.")
        broadcast(lista_cliente, f"{cliente['nome']} saiu do chat.")

def remover_usuario_comando(sock_conn, lista_cliente, nome_remover):
    for cliente in lista_cliente:
        if cliente['nome'] == nome_remover:
            try:
                mensagem_remocao = f"{nome_remover} foi removido do chat pelo administrador."
                broadcast(lista_cliente, mensagem_remocao)

                remover(cliente, lista_cliente)
                sock_conn.send(f"{nome_remover} foi removido do chat.".encode())
                return
            except Exception as e:
                sock_conn.send(f"Erro ao tentar remover {nome_remover}: {e}".encode())
                return

    sock_conn.send(f"Cliente {nome_remover} não encontrado.".encode())

def unicast(lista_cliente, nome_destinatario, mensagem):
    for cliente in lista_cliente:
        if cliente['nome'] == nome_destinatario:
            try:
                cliente['socket'].send(mensagem.encode())
                print(f"Mensagem enviada para {nome_destinatario}: {mensagem}")
                return
            except Exception as e:
                print(f"Erro ao enviar mensagem para {nome_destinatario}: {e}")
                return
    print(f"Cliente {nome_destinatario} não encontrado para unicast.")

HOST = '26.206.166.193'  
PORTA = 8080            
lista_cliente = []

socket_server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
socket_server.bind((HOST, PORTA))
socket_server.listen()
print(f"Servidor rodando em {HOST}:{PORTA}...")

while True:
    try:
        sock_conn, ender = socket_server.accept()
        th_cliente = th.Thread(target=receber_dados, args=(sock_conn, ender))
        th_cliente.start()
    except KeyboardInterrupt:
        print("Servidor encerrado.")
        break
