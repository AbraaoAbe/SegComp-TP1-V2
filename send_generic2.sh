#!/bin/bash

# Defina suas variáveis
DAPP_ADDRESS="0xab7528bb862fb57e8a2bcd567a2e929a0be56a5e"
CHAIN_ID="31337" # Exemplo: Foundry
RPC_URL="http://127.0.0.1:8545"
MNEMONIC="test test test test test test test test test test test junk"

# JSON input as a string
INPUT_STRING='{
    "operacao": "postar_certificado",
    "certificado": "-----BEGIN CERTIFICATE-----\nMIIC7zCCAdcCFBRNImnDM7e7IlIPf7HjMy2ESFT+MA0GCSqGSIb3DQEBCwUAMDQx\nDzANBgNVBAMMBmFiZXppbjEhMB8GCSqGSIb3DQEJARYSdW1lbWFpbEBob3Rkb2cu\nY29tMB4XDTI0MDgxNTE0MTgwM1oXDTI1MDgxNTE0MTgwM1owNDEPMA0GA1UEAwwG\nYWJlemluMSEwHwYJKoZIhvcNAQkBFhJ1bWVtYWlsQGhvdGRvZy5jb20wggEiMA0G\nCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDeYqr7bZoLBj2TR4TuH7BPOVlhAkJx\nKKTFeldh7SlBi2s1lNTlWbUX8G3ggcHccojNmWtRY4VoKfSEGe/rKF4TWKw2PJXk\ntf9F0awG1ZXUdXpfYc3W0VH0lykqJp8CTX362590UwUVb8sGyadc2qjupPITf6hy\nwbu782LEExHsfTY2oXw5k4zEGYVhXWeIVDPlUbp1HLXKcwwJvlN8ieRhC73ir/oj\nQYs3q8eOdg8MZzL12hb00DbEQ2pOclm5JhdzLJeykYA/5kawNSjfh8D8S9ENj533\nABr72p2g5qj0TViiTF8NX8pp1NpnpWpfSTBI1fUcFpZe+ezhCAVvYwZJAgMBAAEw\nDQYJKoZIhvcNAQELBQADggEBANpDw2MKxiqdJLTB4ycp6SREE231gM1Ot9axYmZx\nKZZu4SLTPaGtbfQZFmDBWtGPgsRTkgq61z7/pqdJb0XIBfEjhmm9PRLcyj0CHqJo\nDr/py86tpIOLlfZrGCeDxRTJtVaHwRCS4MDNBst7bUB3wI5erxCQCmIkHmjRt75I\nRZd4PFaZzpwnVacZOHKsR7f74GnWCW3S858DehRJFbb3mYryJntrLK7c0VCEvHbL\nvzZ5C5szLpeAvrbiCMvs77FwB1s6vZYTD8Vn6NdgXxhY1M3DB0WAbI58ocKV7eBf\nuYDsn5q2OeL8yZth/kerxEJWMc+SbZ0VpLUquKWIOr4gSNE=\n-----END CERTIFICATE-----",
    "mensagem": "Comi quem leu!",
    "assinatura": "BcqBptw3BmOwJmlf3NkzlpX/uB+LL2Lqd3ur12fKBLiYEpiUFQiyaUruhHcRh0tPAtNQdkGfN9DC\n7d+JldUGRgohADhklM6Pi/YhanJLD5DO/fpfHWC/PlBHDr4T3Ttwjf40UV1//4E6h4iruaO9jUAb\nJkpTxXFgVdRGAbA4sTWQx0/Bj/7x3kS7t2CL3ROIog1+0ZJQAJuJsUHjV1b1S8ox4I84NCO3Oz/y\n1lFztNFvoK3cLpee+NkV2k2f9kcxV8Qi1MPN+PJW+g1a55uL8iVKvTGtjhXGdGl9d0NfEeCmnWXE\nAyBxwViB9ty8OQX5ha/EEIYRpewZtjiwC+S+aw==",
    "status": true
}'

cartesi send generic \
  --dapp "$DAPP_ADDRESS" \
  -c "$CHAIN_ID" \
  -r "$RPC_URL" \
  --mnemonic-passphrase "$MNEMONIC" \
  --input-encoding "string" \
  --input "$INPUT_STRING"
