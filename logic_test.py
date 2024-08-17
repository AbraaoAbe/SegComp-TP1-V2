from os import environ
import os
import traceback
import logging
import requests
import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

# rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
# logger.info(f"HTTP rollup_server url is {rollup_server}")

def hex2str(hex):
    """
    Decodes a hex string into a regular string
    """
    return bytes.fromhex(hex[2:]).decode("utf-8")

def str2hex(str):
    """
    Encodes a string as a hex string
    """
    return "0x" + str.encode("utf-8").hex()

def load_certificate(cert_str):
    try:
        # Carrega a chave pública a partir do certificado PEM
        cert_str = cert_str.replace("-----BEGIN CERTIFICATE-----", "").replace("-----END CERTIFICATE-----", "").replace("\n", "")
        cert_der = base64.b64decode(cert_str)
        cert = RSA.import_key(cert_der)
        return cert
    except Exception as e:
        logger.error(f"Erro ao carregar o certificado: {e}")
        return None

def verify_signature(cert, message, signature):
    try:
        # Verifica a assinatura usando a chave pública do certificado
        h = SHA256.new(message)
        pkcs1_15.new(cert).verify(h, signature)
        return True
    except (ValueError, TypeError) as e:
        logger.error(f"Erro ao verificar a assinatura: {e}")
        return False

# Define o caminho do arquivo onde os certificados serão armazenados
certificates_file = "./calculator/certificates.json"

# Função para carregar certificados existentes
def load_certificates_from_file():
    if os.path.exists(certificates_file) and os.path.getsize(certificates_file) > 0:
        with open(certificates_file, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError as e:
                logger.error(f"Erro ao decodificar JSON: {e}")
                return {}
    else:
        # Retorna um dicionário vazio se o arquivo não existir ou estiver vazio
        return {}

# Função para salvar certificados
def save_certificates_to_file(certificates):
    with open(certificates_file, "w") as file:
        json.dump(certificates, file, indent=4)

def handle_advance(data):
    logger.info(f"Received advance request data {data}")

    status = "accept"
    try:
        # input_data = hex2str(data["payload"])
        # logger.info(f"Received input: {input_data}")

        # Parse JSON input
        parsed_data = json.loads(data)
        operation = parsed_data.get("operacao")
        cert_str = parsed_data.get("certificado")
        signature_b64 = parsed_data.get("assinatura")
        message = parsed_data.get("mensagem")
        status = parsed_data.get("status")

        if not all([operation, cert_str, signature_b64, message, status]):
            raise ValueError("JSON data is missing required fields.")

        # Carrega o certificado
        cert = load_certificate(cert_str)
        if not cert:
            raise ValueError("Failed to load certificate.")

        # Decodifica a assinatura de base64
        signature = base64.b64decode(signature_b64)

        # Verifica a assinatura
        if not verify_signature(cert, message.encode('utf-8'), signature):
            raise ValueError("Invalid signature. Operation rejected.")
        else:
            logger.info("Signature verified.")

        # Executa a operação com base no tipo
        if operation == "postar_certificado":
            logger.info("Verifing if the certificate was already posted...")
            
            # Carrega certificados existentes
            certificates = load_certificates_from_file()
            
            # Verifica se o identificador já existe
            if message in certificates:
                logger.info("The certificate was already posted.")
            else:
                logger.info("Posting the certificate...")
                
                # # Estrutura JSON para enviar para a blockchain
                # payload = {"message": message, "cert_str": cert_str, "status": status}
                # response = requests.post(rollup_server + "/notice", json={"payload": str2hex(json.dumps(payload))})
                
                # logger.info(f"Received notice status {response.status_code} body {response.content}")
                
                # Atualiza o arquivo local com o novo certificado
                logger.info(f"Updating certificates file:{certificates}")
                certificates[message] = {"cert_str": cert_str, "status": status}
                logger.info(f"Certificates file updated:{certificates}")
                save_certificates_to_file(certificates)

        elif operation == "revogar_certificado":
            logger.info("Revoking the certificate...")
            # Carrega certificados existentes
            certificates = load_certificates_from_file()
            
            # Verifica se o identificador existe
            if message in certificates:
                # Atualiza o status do certificado para false
                certificates[message]['status'] = False
                
                # Salva a alteração no arquivo local
                save_certificates_to_file(certificates)
                
                # Estrutura JSON para enviar para a blockchain
                payload = {"message": message, "cert_str": certificates[message]['cert_str'], "status": False}
                # response = requests.post(rollup_server + "/notice", json={"payload": str2hex(json.dumps(payload))})
                
                # logger.info(f"Received notice status {response.status_code} body {response.content}")
            else:
                logger.info("Certificado não encontrado para revogação.")

        else:
            raise ValueError(f"Operação desconhecida: {operation}")

    except Exception as e:
        status = "reject"
        msg = f"Error processing data {data}\n{traceback.format_exc()}"
        logger.error(msg)
        # response = requests.post(rollup_server + "/report", json={"payload": str2hex(msg)})
        # logger.info(f"Received report status {response.status_code} body {response.content}")

    return status

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    logger.info("Adding report")
    # response = requests.post(rollup_server + "/report", json={"payload": data["payload"]})
    # logger.info(f"Received report status {response.status_code}")
    return "accept"


json_string = '''{
    "operacao": "postar_certificado",
    "certificado": "-----BEGIN CERTIFICATE-----\\nMIIC7zCCAdcCFBRNImnDM7e7IlIPf7HjMy2ESFT+MA0GCSqGSIb3DQEBCwUAMDQx\\nDzANBgNVBAMMBmFiZXppbjEhMB8GCSqGSIb3DQEJARYSdW1lbWFpbEBob3Rkb2cu\\nY29tMB4XDTI0MDgxNTE0MTgwM1oXDTI1MDgxNTE0MTgwM1owNDEPMA0GA1UEAwwG\\nYWJlemluMSEwHwYJKoZIhvcNAQkBFhJ1bWVtYWlsQGhvdGRvZy5jb20wggEiMA0G\\nCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDeYqr7bZoLBj2TR4TuH7BPOVlhAkJx\\nKKTFeldh7SlBi2s1lNTlWbUX8G3ggcHccojNmWtRY4VoKfSEGe/rKF4TWKw2PJXk\\ntf9F0awG1ZXUdXpfYc3W0VH0lykqJp8CTX362590UwUVb8sGyadc2qjupPITf6hy\\nwbu782LEExHsfTY2oXw5k4zEGYVhXWeIVDPlUbp1HLXKcwwJvlN8ieRhC73ir/oj\\nQYs3q8eOdg8MZzL12hb00DbEQ2pOclm5JhdzLJeykYA/5kawNSjfh8D8S9ENj533\\nABr72p2g5qj0TViiTF8NX8pp1NpnpWpfSTBI1fUcFpZe+ezhCAVvYwZJAgMBAAEw\\nDQYJKoZIhvcNAQELBQADggEBANpDw2MKxiqdJLTB4ycp6SREE231gM1Ot9axYmZx\\nKZZu4SLTPaGtbfQZFmDBWtGPgsRTkgq61z7/pqdJb0XIBfEjhmm9PRLcyj0CHqJo\\nDr/py86tpIOLlfZrGCeDxRTJtVaHwRCS4MDNBst7bUB3wI5erxCQCmIkHmjRt75I\\nRZd4PFaZzpwnVacZOHKsR7f74GnWCW3S858DehRJFbb3mYryJntrLK7c0VCEvHbL\\nvzZ5C5szLpeAvrbiCMvs77FwB1s6vZYTD8Vn6NdgXxhY1M3DB0WAbI58ocKV7eBf\\nuYDsn5q2OeL8yZth/kerxEJWMc+SbZ0VpLUquKWIOr4gSNE=\\n-----END CERTIFICATE-----",
    "mensagem": "Comi quem leu!",
    "assinatura": "BcqBptw3BmOwJmlf3NkzlpX/uB+LL2Lqd3ur12fKBLiYEpiUFQiyaUruhHcRh0tPAtNQdkGfN9DC\\n7d+JldUGRgohADhklM6Pi/YhanJLD5DO/fpfHWC/PlBHDr4T3Ttwjf40UV1//4E6h4iruaO9jUAb\\nJkpTxXFgVdRGAbA4sTWQx0/Bj/7x3kS7t2CL3ROIog1+0ZJQAJuJsUHjV1b1S8ox4I84NCO3Oz/y\\n1lFztNFvoK3cLpee+NkV2k2f9kcxV8Qi1MPN+PJW+g1a55uL8iVKvTGtjhXGdGl9d0NfEeCmnWXE\\nAyBxwViB9ty8OQX5ha/EEIYRpewZtjiwC+S+aw==",
    "status": true
}'''

handle_advance(json_string)
