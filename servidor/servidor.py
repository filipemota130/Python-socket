import os, socket
porta = 9000
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ip = 'localhost'
servidor.bind((ip, porta))

while True:
    servidor.listen(2)
    print("Esperando conexão...")

    connection, address = servidor.accept()

    if connection:
        print(f"Ocorreu uma conexão com o cliente {address}")
       
    opcao = connection.recv(1024).decode() #Recebe a opção desejada do cliente
    
    if (opcao == '1'):
        filelist = os.listdir()
        filelist = str(filelist) #Envia a lista de arquivos no servidor
        connection.send(filelist.encode())
        
        namefile = connection.recv(1024).decode() #Recebe a string do nome a fazer download
        
        try:
            with open(namefile, 'rb') as file:
                for line in file.readlines():
                    connection.send(line)
                print(f"Arquivo \"{namefile}\" enviado para o cliente {address}.")
        except FileNotFoundError as error:
            print(f"O cliente {address} requisitou um arquivo inexistente.")
            connection.send("erro".encode())
        print(f"A conexão com o cliente {address} foi encerrada.")
        connection.close()
    elif (opcao == '2'):
        namefile2 = connection.recv(1024).decode() #Recebe a string do nome a fazer upload
        
        nope = 0 
        with open(namefile2,'wb') as file:
            while True:
                data = connection.recv(1000000)
                if data == b'erro':
                    print(f"O cliente {address} tentou enviar um arquivo inexistente.")
                    nope = 1
                    break
                if not data:
                    break
                file.write(data)
            if nope == 0: print(f"Arquivo \"{namefile2}\" recebido.")
        if nope == 1: 
            os.remove(namefile2)
            print(f"A conexão com o cliente {address} foi encerrada.")      
    else:
        if opcao != '3': print(f"O cliente {address} enviou um pedido inválido.")
        print(f"A conexão com o cliente {address} foi encerrada.")
        connection.close()