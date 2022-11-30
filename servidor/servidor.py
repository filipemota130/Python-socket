import socket
port= 9000
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ip = 'localhost'
servidor.bind((ip, port))

while True:
    servidor.listen(2)
    print("esperando conexão...")

    connection, address = servidor.accept()

    if connection:
        print("ocorreu uma conexão com o usuario", address)
        
    namefile = connection.recv(1024).decode()

    try:
        with open(namefile, 'rb') as file:
            for line in file.readlines():
                connection.send(line)
    except FileNotFoundError as error:
        print(error)
        connection.send("erro".encode())
    connection.close()