import os,socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_server = 'localhost'
client.connect((ip_server, 9000))

namefile = str(input("insira o nome do arquivo: "))

client.send(namefile.encode())

with open(namefile,'wb') as file:
    while True:
        data = client.recv(1000000)
        if data == b'erro':
            print("arquivo inexistente")
            os.remove(namefile)
            exit()
        if not data:
            break
        file.write(data)
print(f"{namefile} recebido!")