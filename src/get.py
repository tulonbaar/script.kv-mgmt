from .auth import get_key_client, get_secret_client, get_certificate_client

def get_key(name):
    try:
        client = get_key_client()
        return client.get_key(name)
    except Exception as e:
        print(f"Error getting key: {e}")
        return None

def get_all_keys():
    try:
        client = get_key_client()
        return list(client.list_properties_of_keys())
    except Exception as e:
        print(f"Error fetching keys: {e}")
        return []

def get_all_secrets():
    try:
        client = get_secret_client()
        return list(client.list_properties_of_secrets())
    except Exception as e:
        print(f"Error fetching secrets: {e}")
        return []

def get_all_certificates():
    try:
        client = get_certificate_client()
        return list(client.list_properties_of_certificates())
    except Exception as e:
        print(f"Error fetching certificates: {e}")
        return []

def list_keys():
    try:
        print("\n--- Keys ---")
        keys = get_all_keys()
        count = 0
        for key in keys:
            print(f"Name: {key.name} | Enabled: {key.enabled} | Created: {key.created_on}")
            count += 1
        if count == 0:
            print("No keys found.")
    except Exception as e:
        print(f"Error listing keys: {e}")

def list_secrets():
    try:
        print("\n--- Secrets ---")
        secrets = get_all_secrets()
        count = 0
        for secret in secrets:
            print(f"Name: {secret.name} | Enabled: {secret.enabled} | Created: {secret.created_on}")
            count += 1
        if count == 0:
            print("No secrets found.")
    except Exception as e:
        print(f"Error listing secrets: {e}")

def list_certificates():
    try:
        print("\n--- Certificates ---")
        certs = get_all_certificates()
        count = 0
        for cert in certs:
            print(f"Name: {cert.name} | Enabled: {cert.enabled} | Created: {cert.created_on}")
            count += 1
        if count == 0:
            print("No certificates found.")
    except Exception as e:
        print(f"Error listing certificates: {e}")

def list_key_versions(name):
    try:
        client = get_key_client()
        print(f"\n--- Versions for Key: {name} ---")
        versions = client.list_properties_of_key_versions(name)
        version_list = []
        for v in versions:
            version_list.append(v)
            print(f"[{len(version_list)}] Version: {v.version} | Enabled: {v.enabled} | Created: {v.created_on}")
        if not version_list:
            print("No versions found.")
        return version_list
    except Exception as e:
        print(f"Error listing key versions: {e}")
        return []

def list_secret_versions(name):
    try:
        client = get_secret_client()
        print(f"\n--- Versions for Secret: {name} ---")
        versions = client.list_properties_of_secret_versions(name)
        version_list = []
        for v in versions:
            version_list.append(v)
            print(f"[{len(version_list)}] Version: {v.version} | Enabled: {v.enabled} | Created: {v.created_on}")
        if not version_list:
            print("No versions found.")
        return version_list
    except Exception as e:
        print(f"Error listing secret versions: {e}")
        return []

def list_certificate_versions(name):
    try:
        client = get_certificate_client()
        print(f"\n--- Versions for Certificate: {name} ---")
        versions = client.list_properties_of_certificate_versions(name)
        version_list = []
        for v in versions:
            version_list.append(v)
            print(f"[{len(version_list)}] Version: {v.version} | Enabled: {v.enabled} | Created: {v.created_on}")
        if not version_list:
            print("No versions found.")
        return version_list
    except Exception as e:
        print(f"Error listing certificate versions: {e}")
        return []
