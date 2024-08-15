#!/bin/bash

# Nome do arquivo contendo a mensagem a ser criptografada
INPUT_FILE="message.txt"

# Nome do arquivo da chave privada
PRIVATE_KEY="private.key"

# Nome do arquivo onde a mensagem criptografada será salva (em formato base64)
OUTPUT_FILE="encrypted_message_base64.txt"

# Verifica se o arquivo de entrada existe
if [ ! -f "$INPUT_FILE" ]; then
  echo "Arquivo de entrada '$INPUT_FILE' não encontrado. Certifique-se de que o arquivo está no diretório atual."
  exit 1
fi

# Verifica se o arquivo da chave privada existe
if [ ! -f "$PRIVATE_KEY" ]; then
  echo "Chave privada '$PRIVATE_KEY' não encontrada. Certifique-se de que a chave está no diretório atual."
  exit 1
fi

# Criptografa a mensagem usando a chave privada
echo "Criptografando a mensagem usando a chave privada..."
openssl rsautl -encrypt -inkey "$PRIVATE_KEY" -in "$INPUT_FILE" | base64 > "$OUTPUT_FILE"

# Exibe uma mensagem de sucesso e o caminho do arquivo criptografado
echo "Mensagem criptografada com sucesso e convertida para base64."
echo "O arquivo criptografado em base64 foi salvo em: $(pwd)/$OUTPUT_FILE"
