#!/usr/bin/env python3
import socket
import threading
import ssl

def client_thread(client_socket, clientes, usernames):
    username = client_socket.recv(1024).decode()
    usernames[client_socket] = username

    for cliente in clientes:
        if cliente is not client_socket:
            cliente.sendall(f'\n [+] El usuario {username} ha entrado al chat ! \n\n'.encode())

    while True:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break

            for cliente in clientes:
                if cliente is not client_socket:
                    cliente.sendall(f'{message}\n'.encode())
        except:
            break



def server_program():
    host = 'localhost'
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1) # time wait problem
    server_socket.bind((host,port))
     # Añadiendo cifrado E2E
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='server-cert.pem', keyfile='server-key.key')
    server_socket = context.wrap_socket(server_socket, server_side=True)

    server_socket.listen()

    print('\n [+] El servidor esta en escucha de conexiones entrantes...')
    clientes = []
    usernames = {}

    while True: # aceptando conexion del clientes
        client_socket, address = server_socket.accept()
        clientes.append(client_socket)

        print(f'\n [-] Se ha conectado un nuevo cliente : {address}')

        thread = threading.Thread(target=client_thread, args=(client_socket,clientes,usernames))
        thread.daemon = True
        thread.start()

    client_socket.close()

if __name__ == '__main__':
    server_program()
