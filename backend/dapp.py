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

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

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
certificates_file = "certificates.json"

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
        input_data = hex2str(data["payload"])
        # logger.info(f"Received input: {input_data}")

        # Parse JSON input
        parsed_data = json.loads(input_data)
        operation = parsed_data.get("operacao")
        cert_str = parsed_data.get("certificado")
        signature_b64 = parsed_data.get("assinatura")
        message = parsed_data.get("mensagem")
        flag = True
        
        if not all([operation, cert_str, signature_b64, message, flag]):
            raise ValueError("JSON data is missing required fields.")

        signature = base64.b64decode(signature_b64)
        # Trata a revogação com o certificados locais + assinatura de parametro
        if operation == "revogar_certificado":
            flag = False
            logger.info("Revoking the certificate...")
            
            # Carrega os certificados do arquivo local
            certificates = load_certificates_from_file()
            
            # Verifica se o identificador da mensagem existe nos certificados
            if message in certificates:
                certificate_data = certificates[message]
                logger.info(f"Certificate data: {certificate_data}")
                # Verifica se a chave 'cert' existe no dicionário de dados do certificado
                if 'cert' in certificate_data:
                    certificate = certificate_data['cert']
                    logger.info(f"Certificate: {certificate}")
                    # Verifica a assinatura
                    if not verify_signature(certificate, message.encode('utf-8'), signature):
                        status = "reject"
                        logger.info("Signature verification failed.")
                        logger.info("Operation rejected.")
                        return status
                    else:
                        # Atualiza o flag do certificado para false
                        certificates[message]['flag'] = flag
                        
                        # Salva a alteração no arquivo local
                        save_certificates_to_file(certificates)
                        
                        # Cria o payload com o certificado e o flag
                        payload = {"cert_str": certificate_data.get('cert_str', ''), "flag": flag}
                        
                        # Envia o payload para o servidor de rollup
                        response = requests.post(rollup_server + "/notice", json={"payload": str2hex(json.dumps(payload))})
                        
                        logger.info(f"Received notice status {response.status_code} body {response.content}")
                else:
                    logger.error(f"Certificate data missing 'cert' key for message: {message}")
            else:
                logger.info("The certificate was not found for revocation.")
        # OPERACOES POSTAR CERTIFICADO
        elif operation == "postar_certificado":
            # Carrega o certificado
            cert = load_certificate(cert_str)
            if not cert:
                raise ValueError("Failed to load certificate.")
            # Verifica a assinatura
            if not verify_signature(cert, message.encode('utf-8'), signature):
                status = "reject"
                logger.info("Signature verification failed.")
                logger.info("Operation rejected.")
                return status
                raise ValueError("Invalid signature. Operation rejected.")
            else:
                logger.info("Signature verified.")
                # Carrega certificados locais
                certificates = load_certificates_from_file()
                
                # Verifica se o identificador já existe
                if message in certificates:
                    logger.info("The certificate was already posted.")
                    status = "reject"
                    return status
                else:
                    logger.info("Posting the certificate...")
                    
                    payload = {"cert_str": cert_str, "flag": flag}
                    response = requests.post(rollup_server + "/notice", json={"payload": str2hex(json.dumps(payload))})
                    
                    logger.info(f"Received notice status {response.status_code} body {response.content}")
                    
                    # Atualiza o arquivo local com o novo certificado
                    certificates[message] = {"cert_str": cert_str, "flag": flag}
                    save_certificates_to_file(certificates)
        else:
            raise ValueError(f"Invalid operation: {operation}")
    except Exception as e:
        status = "reject"
        msg = f"Error processing data {e}"
        logger.error(msg)
        response = requests.post(rollup_server + "/report", json={"payload": str2hex(msg)})
        logger.info(f"Received report status {response.status_code} body {response.content}")

    return status

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")

    try:
        # Converte o payload hexadecimal para string
        input_data = hex2str(data["payload"])
        logger.info(f"Received input: {input_data}")

        if not input_data:
            response_message = "Error: No message provided"
            logger.error(response_message)
            # Envia o erro para o endpoint /report
            response = requests.post(rollup_server + "/report", json={"payload": str2hex(response_message)})
            logger.info(f"Received report status {response.status_code}")
            return 'reject'

        certificates = load_certificates_from_file()
        # Verifica se a message existe no dicionário de certificados
        if input_data in certificates:
            cert_info = certificates[input_data]
            if not cert_info['flag']:
                logger.info("The certificate was revoked!!")
            logger.info(f"a flag é: {cert_info['flag']}")
        else:
            logger.info("The certificate was not found!!")

        # logger.info(response_message)
        # Envia a resposta para o endpoint /report
        response = requests.post(rollup_server + "/report", json={"payload": str2hex(json.dumps(cert_info))})
        logger.info(f"Received report status {response.status_code}")
        
    except Exception as e:
        msg = f"Error processing data {e}"
        logger.error(msg)
        # Envia o erro para o endpoint /report
        response = requests.post(rollup_server + "/report", json={"payload": str2hex(msg)})
        logger.info(f"Received report status {response.status_code} body {response.content}")
    return "accept"

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received response: {response}")
    logger.info(f"Received finish status {response.status_code}")

    # Verifique o conteúdo da resposta
    logger.info(f"Response content: {response.text}")

    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        try:
            rollup_request = response.json()
            logger.info(f"Received rollup request: {rollup_request}")
            data = rollup_request["data"]
            logger.info(f"Rollup request data: {data}")
            handler = handlers[rollup_request["request_type"]]
            finish["status"] = handler(rollup_request["data"])
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            break
