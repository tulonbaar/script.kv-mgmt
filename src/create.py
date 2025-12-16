from .auth import get_key_client, get_secret_client, get_certificate_client
from azure.keyvault.certificates import CertificatePolicy

def create_key(name, kty="RSA", size=None, curve=None, not_before=None, expires_on=None):
    try:
        client = get_key_client()
        print(f"Creating key '{name}'...")
        
        kwargs = {}
        if size: kwargs['size'] = size
        if curve: kwargs['curve'] = curve
        if not_before: kwargs['not_before'] = not_before
        if expires_on: kwargs['expires_on'] = expires_on

        key = client.create_key(name, kty, **kwargs)
        
        print(f"Key '{key.name}' created successfully.")
        print(f"  ID: {key.id}")
        print(f"  Type: {key.key_type}")
        if hasattr(key.key, 'kty') and key.key.kty == 'RSA':
             # Approximate size check if not explicitly returned in properties
             pass 
        print(f"  Enabled: {key.properties.enabled}")
        
    except Exception as e:
        print(f"Error creating key: {e}")

def create_secret(name, value):
    try:
        client = get_secret_client()
        print(f"Creating secret '{name}'...")
        secret = client.set_secret(name, value)
        print(f"Secret '{secret.name}' created successfully.")
    except Exception as e:
        print(f"Error creating secret: {e}")

def create_certificate(name, subject_name):
    try:
        client = get_certificate_client()
        print(f"Creating certificate '{name}'...")
        # Create a policy with standard defaults
        policy = CertificatePolicy(
            issuer_name="Self",
            subject=f"CN={subject_name}",
            key_type="RSA",
            key_size=2048,
            validity_in_months=12,
            content_type="application/x-pkcs12"
        )
        
        operation = client.begin_create_certificate(certificate_name=name, policy=policy)
        print(f"Certificate creation started for '{name}'. This might take a moment.")
        # operation.wait() # Optional: wait for completion
    except Exception as e:
        print(f"Error creating certificate: {e}")
