#!/bin/bash

# Define o nome do arquivo da chave privada existente
PRIVATE_KEY="private.key"

# Verifica se o arquivo da chave privada existe
if [ ! -f "$PRIVATE_KEY" ]; then
  echo "Chave privada '$PRIVATE_KEY' não encontrada. Certifique-se de que a chave está no diretório atual."
  exit 1
fi

# Define o nome do arquivo de saída para o CSR (Certificate Signing Request)
CSR_FILE="certificate.csr"

# Define o nome do arquivo de saída para o certificado assinado
CERT_FILE="certificate.crt"

# Define a quantidade de dias que o certificado será válido
VALIDITY_DAYS=365

# Gera o CSR (Certificate Signing Request) usando a chave privada
echo "Gerando o CSR (Certificate Signing Request)..."
openssl req -new -key "$PRIVATE_KEY" -out "$CSR_FILE"

# Autoassina o certificado usando o CSR gerado e a chave privada
echo "Autoassinando o certificado..."
openssl x509 -req -days "$VALIDITY_DAYS" -in "$CSR_FILE" -signkey "$PRIVATE_KEY" -out "$CERT_FILE"

# Exibe o conteúdo do certificado gerado
echo "Certificado gerado com sucesso. Conteúdo do certificado:"
openssl x509 -in "$CERT_FILE" -text -noout

# Exibe o caminho completo do certificado gerado
echo "O certificado foi salvo em: $(pwd)/$CERT_FILE"
