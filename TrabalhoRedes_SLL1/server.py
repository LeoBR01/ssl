import random
import os
from socket import *
import math
import ssl

class Fim_exc(BaseException):
    pass


#Criando contexto SSL
def createContext():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('Certificados Cliente\certificate.pem')
    context.load_cert_chain(certfile='Certificador Servidor\certificate.pem', keyfile='Certificador Servidor\key.pem')
    return context

context = createContext()

serverPort = 12000

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket = context.wrap_socket(serverSocket, server_side= True)

serverSocket.bind(("localhost", serverPort))

serverSocket.listen(1)

print ('O servidor esta pronto para receber conexoes')


print ('Aguardando conexao...')
while True:
    connectionSocket, addr = serverSocket.accept()
    print ('Nova conexao recebida!')
    print ('Aguardando envio do arquivo')

    filename = (connectionSocket.recv(1024).decode()).split(":")[1]

    try:
        try:
            arquivo = open(filename, 'rb')
        except:
            print('Erro ao abrir arquivo', filename)
            connectionSocket.sendall('NotAvailable'.encode())
            connectionSocket.close()
            raise Fim_exc('Acabou!')
            
        size = os.path.getsize(filename)
        print('Abriu arquivo', filename, 'de tamanho', size)
        
        connectionSocket.sendall(("Tamanho:" + str(size)).encode())
        
        pacotes = size/1024
        verifica_pacote = size%1024
        
        if verifica_pacote == 0:
            c = 0
            while c <= pacotes:
                dados = arquivo.read(1024)
                connectionSocket.sendall(dados)
                c += 1
        else:
            c = 0
            while c <= (math.floor(pacotes) + 1):
                dados = arquivo.read(1024)
                connectionSocket.sendall(dados)
                c += 1
        connectionSocket.close()
    except Fim_exc:
        print("Fim!!!!")
    except:
        print('Erro de conexão')
        exit()
        

#print ('Servidor processando o arquivo')

#print ('Fechando socket...')