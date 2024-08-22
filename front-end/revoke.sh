#!/bin/bash

# Verificar se o número de argumentos está correto
if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <mensagem> <private.key>"
    exit 1
fi

# Atribuir parâmetros a variáveis
MENSAGEM="$1"

OUTPUT_FILE="./files"
OUTPUT_FILE_FROM_MESSAGE="$OUTPUT_FILE/$MENSAGEM"

#Define o caminho dos arquivos para leitura
CERT_FILE="$OUTPUT_FILE_FROM_MESSAGE/certificate.crt"
SIGN_FILE="$OUTPUT_FILE_FROM_MESSAGE/assinatura_base64.txt"

CERTIFICATE=$(cat "$CERT_FILE")
SIGNATURE=$(cat "$SIGN_FILE")
#MENSAGEM JA É $MENSAGEM
OPERATION_TYPE="revogar_certificado"
DAPP_ADDRESS="0xab7528bb862fb57e8a2bcd567a2e929a0be56a5e"
CHAIN_ID="31337" # Exemplo: Foundry
RPC_URL="http://127.0.0.1:8545"
MNEMONIC="test test test test test test test test test test test junk"

# Envia o comando Cartesi
INPUT_STRING=$(jq -n \
    --arg operacao "$OPERATION_TYPE" \
    --arg certificado "$CERTIFICATE" \
    --arg mensagem "$MENSAGEM" \
    --arg assinatura "$SIGNATURE" \
    '{
    operacao: $operacao,
    certificado: $certificado,
    mensagem: $mensagem,
    assinatura: $assinatura
    }')

echo "Revoke Input JSON: $INPUT_STRING"

# Envia o comando Cartesi
cartesi send generic \
    --dapp "$DAPP_ADDRESS" \
    -c "$CHAIN_ID" \
    -r "$RPC_URL" \
    --mnemonic-passphrase "$MNEMONIC" \
    --input-encoding "string" \
    --input "$INPUT_STRING"