import os,socket, threading, ast
ip_server = '192.168.0.3'

while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip_server, 9000))

    opcao = str(input("Escolha se quer fazer download ou upload:\n[1] - Fazer download de um arquivo do servidor;\n[2] - Fazer upload de um arquivo para o servidor ;\n[3] - Finalizar o programa.\nInforme sua escolha:"))
    client.send(opcao.encode())

    if (opcao == '1'):
        filelist = client.recv(4096).decode() #Recebe a lista de arquivos do servidor e mostra
        filelist = filelist.replace("'.git',", '')
        filelist = ast.literal_eval(filelist)
        
        print("Lista de arquivos no servidor:\n")
        
        for i in range(len(filelist)):
            print(f'{i+1}: {filelist[i]}')
        
                
            
        id_arquivo = int(input("Insira o ID do arquivo: "))
        if id_arquivo > len(filelist):
            namefile = ''
        else :
            namefile = filelist[id_arquivo -1]
        client.send(namefile.encode()) #envia uma string com o nome do arquivo a fazer download

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
        client.close()
    
    elif (opcao == '2'):
        print("Lista de arquivos no cliente:") #Mostra os arquivos no cliente
    
        for i in range(len(os.listdir())):
            print(f'{i+1}: {os.listdir()[i]}')
        
                
        id_arquivo = int(input("Insira o ID do arquivo: "))
        if id_arquivo > len(os.listdir()):
            namefile2 = ''
        else :
            namefile2 = os.listdir()[id_arquivo -1]
        client.send(namefile2.encode()) #envia uma string com o nome do arquivo a fazer upload

        try: #Função que tava na parte de download do servidor p/ enviar o arquivo
            with open(namefile2, 'rb') as file:
                for line in file.readlines():
                    client.send(line)
        except FileNotFoundError as error:
            print(error)
            client.send("erro".encode())
        client.close()

    elif (opcao == '3'):
        client.close()
        exit()
        