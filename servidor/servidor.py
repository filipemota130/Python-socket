import socket

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind(('localhost', 9000))
servidor.listen(1)

print("Esperando conexões")

connection, address = servidor.accept()

if connection:
    print("ocorreu uma conexão com o usuario", address)
    
namefile = connection.recv(1024).decode()

try:
    with open(namefile, 'rb') as file:
        for data in file.readlines():
            connection.send(data)
        print("arquivo enviado!!")
        connection.close()
except FileNotFoundError as error:
    print(error)
    connection.send("erro".encode())