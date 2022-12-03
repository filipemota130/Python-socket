import os, socket, threading
ip = '192.168.0.3'
port= 9000


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


def Main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    servidor.bind((ip, port))

    while True:
        servidor.listen(5)
        print("esperando conexão...")

        connection, address = servidor.accept()

        if connection:
            print("ocorreu uma conexão com o usuario", address)
        
        opcao = connection.recv(1024).decode() #Recebe a opção desejada do cliente
        
        if (opcao == '1'):
            thread = threading.Thread(target=download, args=[connection])
            thread.start()
    
        elif (opcao == '2'):
            thread = threading.Thread(target=upload, args=[connection])
            thread.start()
        
        elif (opcao == '3'):
            connection.close()

Main()