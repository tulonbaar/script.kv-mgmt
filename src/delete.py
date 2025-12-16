from .auth import get_key_client, get_secret_client, get_certificate_client
from azure.core.exceptions import HttpResponseError

def delete_key(name):
    try:
        client = get_key_client()
        print(f"Deleting key '{name}'...")
        poller = client.begin_delete_key(name)
        deleted_key = poller.result()
        print(f"Key '{deleted_key.name}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting key: {e}")

def delete_secret(name):
    try:
        client = get_secret_client()
        print(f"Deleting secret '{name}'...")
        poller = client.begin_delete_secret(name)
        deleted_secret = poller.result()
        print(f"Secret '{deleted_secret.name}' deleted successfully.")
    except HttpResponseError as e:
        if "associated with a certificate" in str(e):
            print(f"Error: Secret '{name}' is associated with a certificate. Please delete the certificate instead.")
        else:
            print(f"Error deleting secret: {e}")
    except Exception as e:
        print(f"Error deleting secret: {e}")

def delete_certificate(name):
    try:
        client = get_certificate_client()
        print(f"Deleting certificate '{name}'...")
        poller = client.begin_delete_certificate(name)
        deleted_cert = poller.result()
        print(f"Certificate '{deleted_cert.name}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting certificate: {e}")
