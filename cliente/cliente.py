import os, socket, ast, pick

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_server = 'localhost'
client.connect((ip_server, 9000))

opcao = str(input(">>> Transferência de Arquivos por TCP <<<\n[1] - Fazer download de um arquivo do servidor;\n[2] - Fazer upload de um arquivo para o servidor;\n[3] - Encerrar a conexão com o servidor.\nInforme sua escolha: "))
client.send(opcao.encode())

if (opcao == '1'): #Download.
    filelist = client.recv(4096).decode() #Recebe a lista de arquivos do servidor.
    filelist = ast.literal_eval(filelist)
  
    options = filelist
    option, index = pick.pick(options, "Lista de arquivos no servidor:", indicator = '=>', default_index = 0)
    
    namefile = option
    client.send(namefile.encode()) #Envia o nome do arquivo a ser baixado.

    nope = 0
    with open(namefile,'wb') as file:
        while True:
            data = client.recv(1000000)
            if not data:
                break
            file.write(data)
        if nope == 0: print(f"Arquivo \"{namefile}\" recebido.")
    if nope == 1:
        os.remove(namefile)
        print("Conexão com o servidor encerrada.")
        exit()
        
elif (opcao == '2'): #Upload.
    options=[]
    for diretorio,sub,arquivos in os.walk(top='./'):
        for arquivo in arquivos:
            if os.path.exists(os.getcwd()+'/'+arquivo):
                options.append(arquivo)
    option, index = pick.pick(options, "Lista de arquivos no cliente:", indicator = '=>', default_index = 0)
        
    namefile = option
    client.send(namefile.encode()) #Envia o nome do arquivo a ser enviado ao servidor.

    with open(namefile, 'rb') as file:
        for line in file.readlines():
            client.send(line)
        print(f"Arquivo \"{namefile}\" enviado para o servidor.")
    print("Conexão com o servidor encerrada.")
    client.close()
elif (opcao == '3'): print("Conexão com o servidor encerrada.")
else: print("Input inválido. Conexão com o servidor encerrada.")