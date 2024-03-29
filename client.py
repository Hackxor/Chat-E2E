#!/usr/bin/env python3
import socket
import threading
import ssl
from tkinter import *
from tkinter.scrolledtext import ScrolledText

def send_message(event, client_socket, username, text_widget, entry_widget):
    message = entry_widget.get()
    client_socket.sendall(f'{username} > {message}'.encode())

    entry_widget.delete(0, END)
    text_widget.configure(state='normal')
    text_widget.insert(END, f'{username} > {message} \n')
    text_widget.configure(state='disabled')

def receive_message(client_socket, text_widget):
    while True:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break

            text_widget.configure(state='normal')
            text_widget.insert(END,message)
            text_widget.configure(state='disabled')

        except:
            
            break

def client_program():
    # conectando el cliente al servidor
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Añadiendo cifrado E2E
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations('server-cert.pem')  # Puedes cambiar esto según tus necesidades
    client_socket = context.wrap_socket(client_socket, server_hostname=host)

    client_socket.connect((host,port))

    username = input(f'\n [+] Introduce tu usuario : ')
    client_socket.sendall(username.encode())

    # creando ventana y añadiendo estilos y forma de distribuirlo
    window = Tk()
    window.title('Chat')

    text_widget = ScrolledText(window, state='disabled')
    text_widget.pack(padx=5, pady=5)
    
    entry_widget = Entry(window)
    entry_widget.bind('<Return>', lambda event: send_message(event, client_socket, username, text_widget, entry_widget) )
    entry_widget.pack(padx=5, pady=5, fill=BOTH, expand=1)

    thread = threading.Thread(target=receive_message, args=(client_socket, text_widget))
    thread.daemon = True
    thread.start()

    window.mainloop()
    client_socket.close()

if __name__ == '__main__':
    client_program()
