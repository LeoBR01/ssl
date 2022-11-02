from socket import *
import ssl

def createContext():
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('Certificados Cliente\certificate.pem')
    context.load_cert_chain(certfile='Certificador Servidor\certificate.pem', keyfile='Certificador Servidor\key.pem')
    return context


createContext()

serverName = '127.0.0.1'
serverPort = 12000
try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
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