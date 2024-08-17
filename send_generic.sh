#!/bin/bash

# Defina suas variáveis
INPUT_PATH_FILES="./INPUT"
DAPP_ADDRESS="0xab7528bb862fb57e8a2bcd567a2e929a0be56a5e"
CHAIN_ID="31337" # Exemplo: Foundry
RPC_URL="http://127.0.0.1:8545"
MNEMONIC="test test test test test test test test test test test junk"

# Recebe a entrada do usuário
echo "Escolha a operação (1 para postar_certificado, 2 para revogar_certificado):"
read OPERATION

# Verifica a escolha do usuário
if [ "$OPERATION" -eq 1 ]; then
  OPERATION_TYPE="postar_certificado"

elif [ "$OPERATION" -eq 2 ]; then
  OPERATION_TYPE="revogar_certificado"
else
  echo "Opção inválida. Saindo..."
  exit 1
fi

# Carrega os dados dos arquivos
CERTIFICATE=$(cat ${INPUT_PATH_FILES}/certificate.crt) 
MESSAGE=$(cat ${INPUT_PATH_FILES}/message.txt)          
SIGNATURE=$(cat ${INPUT_PATH_FILES}/assinatura_base64.txt) 

# Exibe os dados carregados
# echo "Certificate: $CERTIFICATE"
# echo "Message: $MESSAGE"
# echo "Signature: $SIGNATURE"

# Cria a string de entrada JSON
INPUT_STRING=$(jq -n \
  --arg operacao "$OPERATION_TYPE" \
  --arg certificado "$CERTIFICATE" \
  --arg mensagem "$MESSAGE" \
  --arg assinatura "$SIGNATURE" \
  '{
    operacao: $operacao,
    certificado: $certificado,
    mensagem: $mensagem,
    assinatura: $assinatura
  }')

# Exibe a string JSON criada (para debug)
# echo "Input JSON: $INPUT_STRING"

# Envia o comando Cartesi
cartesi send generic \
  --dapp "$DAPP_ADDRESS" \
  -c "$CHAIN_ID" \
  -r "$RPC_URL" \
  --mnemonic-passphrase "$MNEMONIC" \
  --input-encoding "string" \
  --input "$INPUT_STRING"
