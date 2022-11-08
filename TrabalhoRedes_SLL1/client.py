from socket import *
import ssl

def createContext():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('Certificador Servidor\certificate.pem')
    context.load_cert_chain(certfile='Certificados Cliente\certificate.pem', keyfile='Certificados Cliente\key.pem')
    return context

context = createContext()

serverName = 'localhost'
serverPort = 12000
try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket = context.wrap_socket(clientSocket, server_side= False, server_hostname='localhost')
    clientSocket.connect((serverName,serverPort))
except:
    print('Erro de Conexão')
    clientSocket.close()
    exit()
    
filename = input('Entre com o nome do arquivo: ')

clientSocket.send(('Pedido:' + str(filename)).encode())

texto = clientSocket.recv(1024).decode()

if texto == 'NotAvailable':
    print('Erro de disponibilidade do arquivo')
    clientSocket.close()
    exit()
else:
    size = texto.split(":")[1]

arquivo = open(filename, 'wb')


pacotes = int(size)/1024
verifica_pacote = int(size)%1024

if verifica_pacote == 0:
    c=0
    while c <= pacotes:
        dados = clientSocket.recv(1024)
        arquivo.write(dados)
        print(c)
        c += 1
else:
    c=0
    while c <= (pacotes + 1):
        dados = clientSocket.recv(1024)
        arquivo.write(dados)
        print(c)
        c += 1
        

arquivo.close()

clientSocket.close()