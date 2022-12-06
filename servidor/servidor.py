import os, socket, threading
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ip_server = '192.168.0.111'
porta = 9000
servidor.bind((ip_server, porta))

def client_download(connection):
    filelist=[]
    for diretorio,sub,arquivos in os.walk('.'):
        for arquivo in arquivos:
            if os.path.exists(os.getcwd()+'/'+arquivo):
                filelist.append(arquivo)
    filelist = str(filelist)
    connection.send(filelist.encode()) #Envia a lista de arquivos contidos no servidor para o cliente.
        
    namefile = connection.recv(1024).decode() #Recebe o nome do arquivo ser mandado para o cliente.
    
    if namefile == 'end':
        print(f"A conexão com o cliente {address} foi encerrada.")
        connection.close()
    else:
        with open(namefile, 'rb') as file:
            for line in file.readlines():
                connection.send(line)
            print(f"Arquivo \"{namefile}\" enviado para o cliente {address}.")
        connection.close()

def client_upload(connection):
    namefile = connection.recv(1024).decode() #Recebe o nome a do arquivo a ser recebido.
    
    if namefile == 'end':
        print(f"A conexão com o cliente {address} foi encerrada.")
        connection.close()
    else:
        with open(namefile,'wb') as file:
            while True:
                data = connection.recv(100000000) #Recebe a informação que corresponde ao arquivo enviado pelo cliente.
                if not data:
                    break
                file.write(data) #Coloca a informação em um novo arquivo de mesmo nome que o original. 
            print(f"Arquivo \"{namefile}\" recebido.")

while True:
    servidor.listen(2)
    print("Esperando conexão...")
    connection, address = servidor.accept()

    if connection:
        print(f"Ocorreu uma conexão com o cliente {address}")
       
    opcao = connection.recv(1024).decode() #Recebe a opção escolhida pelo cliente.
    
    if (opcao == '1'): #Download.
        threading.Thread(target = client_download(connection), args = [connection])
        print(f"A conexão com o cliente {address} foi encerrada.")
    elif (opcao == '2'): #Upload.
        threading.Thread(target = client_upload(connection), args = [connection])
        print(f"A conexão com o cliente {address} foi encerrada.")
    else: #Outras.
        if opcao != '3': print(f"O cliente {address} enviou um pedido inválido.")
        print(f"A conexão com o cliente {address} foi encerrada.")
        connection.close()