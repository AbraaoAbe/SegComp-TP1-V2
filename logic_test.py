import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def parse_json_input(json_string):
    try:
        # Faz o parsing do JSON string para um dicionário Python
        data = json.loads(json_string)
        return data
    except json.JSONDecodeError:
        print("Erro ao decodificar o JSON.")
        return None

def load_certificate(cert_str):
    try:
        # Carrega a chave pública a partir do certificado PEM
        cert_str = cert_str.replace("-----BEGIN CERTIFICATE-----", "").replace("-----END CERTIFICATE-----", "").replace("\n", "")
        cert_der = base64.b64decode(cert_str)
        cert = RSA.import_key(cert_der)
        return cert
    except Exception as e:
        print(f"Erro ao carregar o certificado: {e}")
        return None

def verify_signature(cert, message, signature):
    try:
        # Verifica a assinatura usando a chave pública do certificado
        h = SHA256.new(message)
        pkcs1_15.new(cert).verify(h, signature)
        return True
    except (ValueError, TypeError) as e:
        print(f"Erro ao verificar a assinatura: {e}")
        return False

def main(json_string):
    # Passo 1: Parse do JSON string
    data = parse_json_input(json_string)
    if not data:
        return
    
    # Passo 2: Extrair os componentes do JSON
    cert_str = data.get("certificado")
    signature_b64 = data.get("assinatura")
    message = data.get("mensagem")
    status = data.get("status", False)

    # Passo 3: Carregar o certificado
    cert = load_certificate(cert_str)
    if not cert:
        return

    # Passo 4: Decodificar a assinatura de base64
    signature = base64.b64decode(signature_b64)

    # Passo 5: Tentar verificar a assinatura com o certificado
    if verify_signature(cert, message.encode('utf-8'), signature):
        print("Usuário é quem diz ser.")
    else:
        print("Usuário NÃO é quem diz ser.")


json_string = '''{
    "certificado": "-----BEGIN CERTIFICATE-----\\nMIIC7zCCAdcCFBRNImnDM7e7IlIPf7HjMy2ESFT+MA0GCSqGSIb3DQEBCwUAMDQx\\nDzANBgNVBAMMBmFiZXppbjEhMB8GCSqGSIb3DQEJARYSdW1lbWFpbEBob3Rkb2cu\\nY29tMB4XDTI0MDgxNTE0MTgwM1oXDTI1MDgxNTE0MTgwM1owNDEPMA0GA1UEAwwG\\nYWJlemluMSEwHwYJKoZIhvcNAQkBFhJ1bWVtYWlsQGhvdGRvZy5jb20wggEiMA0G\\nCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDeYqr7bZoLBj2TR4TuH7BPOVlhAkJx\\nKKTFeldh7SlBi2s1lNTlWbUX8G3ggcHccojNmWtRY4VoKfSEGe/rKF4TWKw2PJXk\\ntf9F0awG1ZXUdXpfYc3W0VH0lykqJp8CTX362590UwUVb8sGyadc2qjupPITf6hy\\nwbu782LEExHsfTY2oXw5k4zEGYVhXWeIVDPlUbp1HLXKcwwJvlN8ieRhC73ir/oj\\nQYs3q8eOdg8MZzL12hb00DbEQ2pOclm5JhdzLJeykYA/5kawNSjfh8D8S9ENj533\\nABr72p2g5qj0TViiTF8NX8pp1NpnpWpfSTBI1fUcFpZe+ezhCAVvYwZJAgMBAAEw\\nDQYJKoZIhvcNAQELBQADggEBANpDw2MKxiqdJLTB4ycp6SREE231gM1Ot9axYmZx\\nKZZu4SLTPaGtbfQZFmDBWtGPgsRTkgq61z7/pqdJb0XIBfEjhmm9PRLcyj0CHqJo\\nDr/py86tpIOLlfZrGCeDxRTJtVaHwRCS4MDNBst7bUB3wI5erxCQCmIkHmjRt75I\\nRZd4PFaZzpwnVacZOHKsR7f74GnWCW3S858DehRJFbb3mYryJntrLK7c0VCEvHbL\\nvzZ5C5szLpeAvrbiCMvs77FwB1s6vZYTD8Vn6NdgXxhY1M3DB0WAbI58ocKV7eBf\\nuYDsn5q2OeL8yZth/kerxEJWMc+SbZ0VpLUquKWIOr4gSNE=\\n-----END CERTIFICATE-----",
    "mensagem": "Comi quem leu!",
    "assinatura": "BcqBptw3BmOwJmlf3NkzlpX/uB+LL2Lqd3ur12fKBLiYEpiUFQiyaUruhHcRh0tPAtNQdkGfN9DC\\n7d+JldUGRgohADhklM6Pi/YhanJLD5DO/fpfHWC/PlBHDr4T3Ttwjf40UV1//4E6h4iruaO9jUAb\\nJkpTxXFgVdRGAbA4sTWQx0/Bj/7x3kS7t2CL3ROIog1+0ZJQAJuJsUHjV1b1S8ox4I84NCO3Oz/y\\n1lFztNFvoK3cLpee+NkV2k2f9kcxV8Qi1MPN+PJW+g1a55uL8iVKvTGtjhXGdGl9d0NfEeCmnWXE\\nAyBxwViB9ty8OQX5ha/EEIYRpewZtjiwC+S+aw==",
    "status": true
}'''

main(json_string)
