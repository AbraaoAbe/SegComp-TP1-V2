#!/bin/bash

# Verificar se o número de argumentos está correto
if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <mensagem> <private.key>"
    exit 1
fi

# Atribuir parâmetros a variáveis
MENSAGEM="$1"
CHAVE="$2"

OUTPUT_FILE="./files"
OUTPUT_FILE_FROM_MESSAGE="$OUTPUT_FILE/$MENSAGEM"
KEY_PATH_FILE="$OUTPUT_FILE_FROM_MESSAGE/$CHAVE"
MESSAGE_FILE="$OUTPUT_FILE_FROM_MESSAGE/message.txt"

# Criar o arquivo de mensagem
echo "$MENSAGEM" > "$MESSAGE_FILE"

# Exibir os parâmetros (para depuração)
echo "Mensagem recebida: $MENSAGEM"
echo "Arquivo da mensagem: $MESSAGE_FILE"
echo "Caminho para o arquivo de chave: $KEY_PATH_FILE"
echo "Arquivo de saida: $OUTPUT_FILE_FROM_MESSAGE"

###################### GERACAO DO CERTIFICADO ASSINADO ######################

VALIDITY_DAYS=365
# Define o nome do arquivo de saída para o CSR (Certificate Signing Request)
CSR_FILE="$OUTPUT_FILE_FROM_MESSAGE/certificate.csr"
# Define o nome do arquivo de saída para o certificado assinado
CERT_FILE="$OUTPUT_FILE_FROM_MESSAGE/certificate.crt"
# Define o arquivo de configuração do certificado
CONFIG_FILE="./config/openssl.cnf"

# Gera o CSR (Certificate Signing Request) usando a chave privada
echo "Gerando o CSR (Certificate Signing Request)..."
openssl req -new -key "$KEY_PATH_FILE" -out "$CSR_FILE" -config "$CONFIG_FILE"

# Autoassina o certificado usando o CSR gerado e a chave privada
echo "Autoassinando o certificado..."
openssl x509 -req -days "$VALIDITY_DAYS" -in "$CSR_FILE" -signkey "$KEY_PATH_FILE" -out "$CERT_FILE"

# Exibe o conteúdo do certificado gerado
echo "Certificado gerado com sucesso. Conteúdo do certificado:"
openssl x509 -in "$CERT_FILE" -text -noout

# Exibe o caminho completo do certificado gerado
echo "O certificado foi salvo em: $(pwd)/$CERT_FILE"

# Limpeza dos arquivos temporários (opcional)
rm "$CSR_FILE"

###################### GERACAO DA ASSINATURA ######################

SIGN_FILE="$OUTPUT_FILE_FROM_MESSAGE/assinatura_base64.txt"
INTERMEDIARY_FILE="$OUTPUT_FILE_FROM_MESSAGE/assinatura.bin"

# Gerar a assinatura usando a chave privada
openssl dgst -sha256 -sign "$KEY_PATH_FILE" -out $INTERMEDIARY_FILE "$MESSAGE_FILE"
echo "Assinatura gerada utilizando o arquivo: $MESSAGE_FILE"

# Codificar a assinatura em base64 (opcional, para incluir em JSON ou facilitar o transporte)
base64 $INTERMEDIARY_FILE > "$SIGN_FILE"

# Exibir a assinatura gerada
echo "Assinatura gerada com sucesso (Base64):"
cat $SIGN_FILE

# Limpeza dos arquivos temporários (opcional)
rm $INTERMEDIARY_FILE

#Por fim remove a chave privada
rm $KEY_PATH_FILE