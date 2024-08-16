from os import environ
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

def handle_advance(data):
    logger.info(f"Received advance request data {data}")

    status = "accept"
    try:
        input_data = hex2str(data["payload"])
        logger.info(f"Received input: {input_data}")

        # Parse JSON input
        parsed_data = json.loads(input_data)
        operation = parsed_data.get("operacao")
        cert_str = parsed_data.get("certificado")
        signature_b64 = parsed_data.get("assinatura")
        message = parsed_data.get("mensagem")

        if not all([operation, cert_str, signature_b64, message]):
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

        # Executa a operação com base no tipo
        if operation == "postar_certificado":
            logger.info("Postando certificado na blockchain...")
            # Implementar lógica para postar o certificado na blockchain
            response = requests.post(rollup_server + "/notice", json={"payload": str2hex(f"Certificado postado: {cert_str}")})
            logger.info(f"Received notice status {response.status_code} body {response.content}")

        elif operation == "revogar_certificado":
            logger.info("Revogando certificado na blockchain...")
            # Implementar lógica para revogar o certificado na blockchain
            response = requests.post(rollup_server + "/notice", json={"payload": str2hex(f"Certificado revogado: {cert_str}")})
            logger.info(f"Received notice status {response.status_code} body {response.content}")

        else:
            raise ValueError(f"Operação desconhecida: {operation}")

    except Exception as e:
        status = "reject"
        msg = f"Error processing data {data}\n{traceback.format_exc()}"
        logger.error(msg)
        response = requests.post(rollup_server + "/report", json={"payload": str2hex(msg)})
        logger.info(f"Received report status {response.status_code} body {response.content}")

    return status

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    logger.info("Adding report")
    response = requests.post(rollup_server + "/report", json={"payload": data["payload"]})
    logger.info(f"Received report status {response.status_code}")
    return "accept"

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]

        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
