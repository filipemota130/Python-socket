import os,socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_server = '192.168.0.3'
client.connect((ip_server, 9000))

opcao = str(input("Escolha se quer fazer download ou upload:\n[1] - Fazer downlaod de um arquivo do servidor;\n[2] - Fazer upload de um arquivo para o servidor ;\n[3] - Finalizar o programa.\nInforme sua escolha:"))
client.send(opcao.encode())

if (opcao == '1'):
    filelist = client.recv(4096).decode() #Recebe a lista de arquivos do servidor e mostra
    print("Lista de arquivos no servidor:\n", filelist)
    
    namefile = str(input("insira o nome do arquivo: "))
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

elif (opcao == '2'):
    print("Lista de arquivos no cliente:\n", os.listdir()) #Mostra os arquivos no cliente
    
    namefile2 = str(input("insira o nome do arquivo: "))
    client.send(namefile2.encode()) #envia uma string com o nome do arquivo a fazer upload

    try: #Função que tava na parte de download do servidor p/ enviar o arquivo
        with open(namefile2, 'rb') as file:
            for line in file.readlines():
                client.send(line)
    except FileNotFoundError as error:
        print(error)
        client.send("erro".encode())
    client.close()

    