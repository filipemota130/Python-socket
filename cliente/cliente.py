import os,socket,ast,pick

ip_server= 'localhost'
while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip_server, 9000))

    opcao = str(input("Escolha se quer fazer download ou upload:\n[1] - Fazer download de um arquivo do servidor;\n[2] - Fazer upload de um arquivo para o servidor ;\n[3] - Finalizar o programa.\nInforme sua escolha:"))
    client.send(opcao.encode())

    if (opcao == '1'):
        filelist = client.recv(4096).decode() #Recebe a lista de arquivos do servidor e mostra.
        filelist = ast.literal_eval(filelist)
    
        options = filelist
        option, index = pick.pick(options, "Lista de arquivos no servidor:", indicator='=>', default_index=0)
        print(option)
        
        namefile = option
        client.send(namefile.encode()) #Envia uma string com o nome do arquivo a fazer download.
        try: #Função que tava na parte de download do servidor p/ enviar o arquivo
            with open(namefile2, 'rb') as file:
                for line in file.readlines():
                    client.send(line)
        except FileNotFoundError as error:
            print(error)
            client.send("erro".encode())
        client.close()

    elif (opcao == '2'):

        options2 = os.listdir()
        option2, index = pick.pick(options2, "Lista de arquivos no cliente:", indicator='=>', default_index=0)
        print(option2)
            
        namefile2 = option2
        client.send(namefile2.encode()) #Envia uma string com o nome do arquivo a fazer upload.

        try: #Função que tava na parte de download do servidor p/ enviar o arquivo.
            with open(namefile2, 'rb') as file:
                for line in file.readlines():
                    client.send(line)
                print(f"Arquivo \"{namefile2}\" enviado para o servidor.")
        except FileNotFoundError as error:
            print("Arquivo inexistente.")
            client.send("erro".encode())
        print("Conexão com o servidor encerrada.")
        client.close()
    elif (opcao == '3'): print("Conexão com o servidor encerrada.")

