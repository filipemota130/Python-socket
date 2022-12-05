import os,socket,ast,pick

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_server = 'localhost'
client.connect((ip_server, 9000))

opcao = str(input(">>> Transferência de Arquivos por TCP <<<\n[1] - Fazer download de um arquivo do servidor;\n[2] - Fazer upload de um arquivo para o servidor;\n[3] - Encerrar a conexão com o servidor.\nInforme sua escolha: "))
client.send(opcao.encode())

if (opcao == '1'):
    filelist = client.recv(4096).decode() #Recebe a lista de arquivos do servidor e mostra.
    filelist = ast.literal_eval(filelist)
        
    print("Lista de arquivos no servidor:\n")
        
    options = filelist
    option, index = pick.pick(options, "", indicator='=>', default_index=0)
    print(option)
    
    namefile = option
    client.send(namefile.encode()) #Envia uma string com o nome do arquivo a fazer download.

    nope = 0
    with open(namefile,'wb') as file:
        while True:
            data = client.recv(1000000)
            if data == b'erro':

                print("Arquivo inexistente.")
                nope = 1
                break
            if not data:
                break
            file.write(data)
        if nope == 0: print(f"Arquivo \"{namefile}\" recebido.")
    if nope == 1:
        os.remove(namefile)
        print("Conexão com o servidor encerrada.")
        exit()
elif (opcao == '2'):
    print("Lista de arquivos no cliente:\n", os.listdir()) #Mostra os arquivos no cliente.
    
    options2 = os.listdir()
    option2, index = pick.pick(options2, "", indicator='=>', default_index=0)
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
else: print("Input inválido. Conexão com o servidor encerrada.")