import os
from azure.identity import ClientSecretCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.secrets import SecretClient
from azure.keyvault.certificates import CertificateClient
from dotenv import load_dotenv

load_dotenv()

def get_credentials():
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")
    
    if not all([tenant_id, client_id, client_secret]):
        # Fallback or let the caller handle it, but for this script explicit check is good
        # However, DefaultAzureCredential could also be used if we wanted to be more flexible.
        # Given the user explicitly mentioned .env with these values, ClientSecretCredential is direct.
        pass

    return ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

def get_key_client():
    vault_url = os.getenv("KEY_VAULT_URL")
    if not vault_url:
        raise ValueError("Missing KEY_VAULT_URL in .env file")
    return KeyClient(vault_url=vault_url, credential=get_credentials())

def get_secret_client():
    vault_url = os.getenv("KEY_VAULT_URL")
    if not vault_url:
        raise ValueError("Missing KEY_VAULT_URL in .env file")
    return SecretClient(vault_url=vault_url, credential=get_credentials())

def get_certificate_client():
    vault_url = os.getenv("KEY_VAULT_URL")
    if not vault_url:
        raise ValueError("Missing KEY_VAULT_URL in .env file")
    return CertificateClient(vault_url=vault_url, credential=get_credentials())
