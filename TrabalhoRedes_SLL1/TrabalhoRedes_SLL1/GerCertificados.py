from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
import datetime

#Gerando a chave

key = rsa.generate_private_key(public_exponent = 65537, key_size = 2048)

#Salvando a chave em disco

with open('Certificador Servidor/key.pem', 'wb') as file:
    file.write(key.private_bytes(encoding = serialization.Encoding.PEM, 
    format = serialization.PrivateFormat.TraditionalOpenSSL, 
    encryption_algorithm = serialization.BestAvailableEncryption(b"passphrase"),
    ))
 
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"BR"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Rio de Janeiro"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Rio de Janeiro"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"LBR Studies"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"lbrlearning.com"),
])

cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(

    # Validade do certificado gerado de 365 dias
    datetime.datetime.utcnow() + datetime.timedelta(days=365)
).add_extension(
    x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
    critical=False,
# Assinando nosso certificado com a chave privada
).sign(key, hashes.SHA256())

# Escrevendo nosso certificado em disco
with open("Certificador Servidor/certificate.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))