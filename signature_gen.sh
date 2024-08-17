#!/bin/bash

# Nome do arquivo contendo a mensagem a ser criptografada
INPUT_FILE="./INPUT/message.txt"

# Nome do arquivo da chave privada
PRIVATE_KEY="./PK/private.key"

OUTPUT_FILE="./INPUT/assinatura_base64.txt"

# Gerar a assinatura usando a chave privada
openssl dgst -sha256 -sign "$PRIVATE_KEY" -out assinatura.bin "$INPUT_FILE"

# Codificar a assinatura em base64 (opcional, para incluir em JSON ou facilitar o transporte)
base64 assinatura.bin > "$OUTPUT_FILE"

# Exibir a assinatura gerada
echo "Assinatura gerada (Base64):"
cat assinatura_base64.txt

# Limpeza dos arquivos temporários (opcional)
rm assinatura.bin
