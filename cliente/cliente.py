import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('localhost', 9000))
print("conectado ao servidor\n")

while True:
    namefile = str(input("insira o nome do arquivo(ou digite 'close' para fechar a conexão com o servidor): "))

    if namefile =='close':
        print("closing connection...")
        break
    client.send(namefile.encode())

    if client.recv(1000000).decode() == "erro":
        print("Arquivo não encontrado.")
    else:
        with open(namefile,'wb') as file:
            while True:
                data = client.recv(1000000)
                if not data:
                    break
                file.write(data)
        print(f"{namefile} recebido!")