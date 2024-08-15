#!/bin/bash

# Nome do arquivo contendo a mensagem a ser criptografada
INPUT_FILE="message.txt"

# Nome do arquivo da chave privada
PRIVATE_KEY="private.key"

# Nome do arquivo onde a mensagem criptografada será salva
OUTPUT_FILE="encrypted_message.bin"

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
openssl rsautl -encrypt -inkey "$PRIVATE_KEY" -in "$INPUT_FILE" -out "$OUTPUT_FILE"

# Exibe uma mensagem de sucesso e o caminho do arquivo criptografado
echo "Mensagem criptografada com sucesso."
echo "O arquivo criptografado foi salvo em: $(pwd)/$OUTPUT_FILE"
