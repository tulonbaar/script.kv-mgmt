import os
from azure.identity import DefaultAzureCredential, DeviceCodeCredential, ChainedTokenCredential, UsernamePasswordCredential, CredentialUnavailableError
from azure.keyvault.keys import KeyClient
from azure.keyvault.secrets import SecretClient
from azure.keyvault.certificates import CertificateClient
from dotenv import load_dotenv

load_dotenv()

def device_code_prompt(verification_uri, user_code, **kwargs):
    print(f"\nTo sign in, use a web browser to open the page {verification_uri} and enter the code {user_code} to authenticate.\n")

class SafeDefaultAzureCredential(DefaultAzureCredential):
    def get_token(self, *scopes, **kwargs):
        try:
            return super().get_token(*scopes, **kwargs)
        except Exception as e:
            # print(f"DEBUG: SafeDefaultAzureCredential caught {type(e).__name__}: {e}")
            # Ensure we allow the chain to continue by raising CredentialUnavailableError
            # even if DefaultAzureCredential raised something else (like ClientAuthenticationError)
            if not isinstance(e, CredentialUnavailableError):
                pass
            raise CredentialUnavailableError(message="DefaultAzureCredential failed", from_exception=e)

def get_credentials():
    # print("DEBUG: get_credentials called")
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    username = os.getenv("AZURE_USERNAME")
    password = os.getenv("AZURE_PASSWORD")

    # Filter out placeholder or empty
    if tenant_id and "your-tenant-id" in tenant_id:
        tenant_id = None

    credentials = []

    # 1. Username/Password (if defined in .env)
    # Note: This requires 'Allow public client flows' to be enabled on the App Registration
    # and MFA to be disabled for the user.
    if username and password and client_id:
        credentials.append(UsernamePasswordCredential(
            client_id=client_id, 
            username=username, 
            password=password, 
            tenant_id=tenant_id
        ))

    # 2. DefaultAzureCredential (SP, Managed Identity, CLI, etc.)
    # We exclude interactive browser here to avoid errors in headless environments.
    credentials.append(SafeDefaultAzureCredential(exclude_interactive_browser_credential=True))

    # 3. Device Code (Fallback)
    dc_cred = DeviceCodeCredential(tenant_id=tenant_id, prompt_callback=device_code_prompt)
    credentials.append(dc_cred)

    return ChainedTokenCredential(*credentials)

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

def validate_connection():
    """
    Attempts to connect to the Key Vault to verify credentials.
    Returns True if successful, raises an exception otherwise.
    """
    try:
        client = get_secret_client()
        # Try to list secrets (limit 1) to verify access
        # We use an iterator but don't need to consume it fully, just creating it might be enough 
        # or trying to fetch the first page.
        # A simple property access might not trigger a network call.
        # list_properties_of_secrets returns an ItemPaged, iterating it triggers the call.
        secrets = client.list_properties_of_secrets()
        next(secrets, None) # Try to get one item, or None if empty. 
                            # If auth fails, this will raise an exception.
        print("Successfully connected to Key Vault.")
        return True
    except Exception as e:
        print(f"Failed to connect to Key Vault: {e}")
        raise
