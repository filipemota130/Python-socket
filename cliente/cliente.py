import os, socket, ast, pick

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_server = '192.168.0.103'
client.connect((ip_server, 9000))

opcao = str(input(">>> Transferência de Arquivos por TCP <<<\n[1] - Fazer download de um arquivo do servidor;\n[2] - Fazer upload de um arquivo para o servidor;\n[3] - Encerrar a conexão com o servidor.\nInforme sua escolha: "))
client.send(opcao.encode())

if (opcao == '1'): #Download.
    filelist = client.recv(4096).decode() #Recebe a lista de arquivos do servidor.
    filelist = ast.literal_eval(filelist)
    
    options = filelist
    if "servidor.py" in options:
        options.remove('servidor.py')
    options.append("[Encerrar]")
    option, index = pick.pick(options, "Lista de arquivos no servidor:", indicator = '=>', default_index = 0)
    
    if option == '[Encerrar]':
        client.send('end'.encode())
        client.close()
        exit()
        
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
    for diretorio,sub,arquivos in os.walk('./'):
        if str(diretorio) != "./":
            break
        for arquivo in arquivos:
            options.append(arquivo)
    options.remove('cliente.py')
    if options == []:
        print('Diretório vazio.')
        client.send('end'.encode())
        client.close()
        exit()
    options.append("[Encerrar]")
    option, index = pick.pick(options, "Lista de arquivos no cliente:", indicator = '=>', default_index = 0)

    if option == '[Encerrar]':
        client.send('end'.encode())
        client.close()
        exit()    
        
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