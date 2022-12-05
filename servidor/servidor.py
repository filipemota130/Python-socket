import os, socket, threading
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ip = 'localhost'
porta = 9000
servidor.bind((ip, porta))

def download(connection): #função download
    filelist = os.listdir()
    filelist = str(filelist) #Envia a lista de arquivos no servidor
    connection.send(filelist.encode())
        
    namefile = connection.recv(1024).decode() #Recebe a string do nome a fazer download
        
    try:
        with open(namefile, 'rb') as file:
            for line in file.readlines():
                connection.send(line)
    except FileNotFoundError as error:
        print(error)
        connection.send("erro".encode())
    connection.close()

def upload(connection):
    namefile2 = connection.recv(1024).decode() #Recebe a string do nome a fazer upload
        
    with open(namefile2,'wb') as file:
        while True:
            data = connection.recv(1000000)
            if data == b'erro':
                print("arquivo inexistente")
                os.remove(namefile2)
                exit()
            if not data:
                break
            file.write(data)
        print(f"{namefile2} recebido!")

while True:
    servidor.listen(2)
    print("Esperando conexão...")

    connection, address = servidor.accept()

    if connection:
        print(f"Ocorreu uma conexão com o cliente {address}")
       
    opcao = connection.recv(1024).decode() #Recebe a opção desejada do cliente
    
    if (opcao == '1'):
        threading.Thread(target=download(connection), args=[connection])
    elif (opcao == '2'):
        threading.Thread(target=upload(connection), args=[connection])
    else:
        if opcao != '3': print(f"O cliente {address} enviou um pedido inválido.")
        print(f"A conexão com o cliente {address} foi encerrada.")
        connection.close()