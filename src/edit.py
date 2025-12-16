from .auth import get_key_client, get_secret_client, get_certificate_client
from azure.core.exceptions import HttpResponseError

def update_key_properties(name, enabled=None, key_ops=None, not_before=None, expires_on=None):
    try:
        client = get_key_client()
        print(f"Updating key '{name}'...")
        
        kwargs = {}
        if enabled is not None: kwargs['enabled'] = enabled
        if key_ops is not None: kwargs['key_operations'] = key_ops
        if not_before is not None: kwargs['not_before'] = not_before
        if expires_on is not None: kwargs['expires_on'] = expires_on

        key = client.update_key_properties(name, **kwargs)
        print(f"Key '{key.name}' updated successfully.")
    except Exception as e:
        print(f"Error updating key: {e}")

def update_key_tags(name, tags):
    try:
        client = get_key_client()
        print(f"Fetching key '{name}' to get existing tags...")
        key = client.get_key(name)
        current_tags = key.properties.tags or {}
        current_tags.update(tags)
        
        print(f"Updating key '{name}' tags...")
        updated_key = client.update_key_properties(name, tags=current_tags)
        print(f"Key '{updated_key.name}' tags updated successfully.")
    except Exception as e:
        print(f"Error updating key tags: {e}")

def update_secret_value(name, value):
    try:
        client = get_secret_client()
        print(f"Updating secret '{name}' (creating new version)...")
        secret = client.set_secret(name, value)
        print(f"Secret '{secret.name}' updated successfully.")

        # Disable older versions
        print(f"Disabling older versions of secret '{name}'...")
        versions = client.list_properties_of_secret_versions(name)
        for version in versions:
            if version.version != secret.properties.version and version.enabled:
                client.update_secret_properties(name, version=version.version, enabled=False)
                print(f"Version {version.version} disabled.")

    except Exception as e:
        print(f"Error updating secret: {e}")

def update_secret_tags(name, tags):
    try:
        client = get_secret_client()
        print(f"Fetching secret '{name}' to get existing tags...")
        secret = client.get_secret(name)
        current_tags = secret.properties.tags or {}
        current_tags.update(tags)
        
        print(f"Updating secret '{name}' tags...")
        updated_secret = client.update_secret_properties(name, tags=current_tags)
        print(f"Secret '{updated_secret.name}' tags updated successfully.")
    except Exception as e:
        print(f"Error updating secret tags: {e}")

def update_certificate_tags(name, tags):
    try:
        client = get_certificate_client()
        print(f"Fetching certificate '{name}' to get existing tags...")
        cert = client.get_certificate(certificate_name=name)
        current_tags = cert.properties.tags or {}
        current_tags.update(tags)

        print(f"Updating certificate '{name}' tags...")
        updated_cert = client.update_certificate_properties(certificate_name=name, tags=current_tags)
        print(f"Certificate '{updated_cert.name}' updated successfully.")
    except Exception as e:
        print(f"Error updating certificate: {e}")

def update_key_version_properties(name, version, enabled):
    try:
        client = get_key_client()
        print(f"Updating key '{name}' version '{version}'...")
        client.update_key_properties(name, version=version, enabled=enabled)
        print(f"Key version updated successfully.")
    except HttpResponseError as e:
        if "associated with a certificate" in str(e):
            print(f"Error: Key '{name}' is associated with a certificate. Please manage the certificate versions instead.")
        else:
            print(f"Error updating key version: {e}")
    except Exception as e:
        print(f"Error updating key version: {e}")

def update_secret_version_properties(name, version, enabled):
    try:
        client = get_secret_client()
        print(f"Updating secret '{name}' version '{version}'...")
        client.update_secret_properties(name, version=version, enabled=enabled)
        print(f"Secret version updated successfully.")
    except HttpResponseError as e:
        if "associated with a certificate" in str(e):
            print(f"Error: Secret '{name}' is associated with a certificate. Please manage the certificate versions instead.")
        else:
            print(f"Error updating secret version: {e}")
    except Exception as e:
        print(f"Error updating secret version: {e}")

def update_certificate_version_properties(name, version, enabled):
    try:
        client = get_certificate_client()
        print(f"Updating certificate '{name}' version '{version}'...")
        client.update_certificate_properties(certificate_name=name, version=version, enabled=enabled)
        print(f"Certificate version updated successfully.")
    except Exception as e:
        print(f"Error updating certificate version: {e}")

def disable_all_but_newest_key_version(name):
    try:
        client = get_key_client()
        print(f"Fetching versions for key '{name}'...")
        versions = list(client.list_properties_of_key_versions(name))
        if not versions:
            print("No versions found.")
            return

        # Sort by created_on descending
        versions.sort(key=lambda x: x.created_on, reverse=True)
        newest = versions[0]
        print(f"Newest version is {newest.version} (Created: {newest.created_on})")

        for v in versions[1:]:
            if v.enabled:
                print(f"Disabling version {v.version}...")
                client.update_key_properties(name, version=v.version, enabled=False)
        print("All other versions disabled.")
    except HttpResponseError as e:
        if "associated with a certificate" in str(e):
            print(f"Error: Key '{name}' is associated with a certificate. Please manage the certificate versions instead.")
        else:
            print(f"Error disabling old key versions: {e}")
    except Exception as e:
        print(f"Error disabling old key versions: {e}")

def disable_all_but_newest_secret_version(name):
    try:
        client = get_secret_client()
        print(f"Fetching versions for secret '{name}'...")
        versions = list(client.list_properties_of_secret_versions(name))
        if not versions:
            print("No versions found.")
            return

        # Sort by created_on descending
        versions.sort(key=lambda x: x.created_on, reverse=True)
        newest = versions[0]
        print(f"Newest version is {newest.version} (Created: {newest.created_on})")

        for v in versions[1:]:
            if v.enabled:
                print(f"Disabling version {v.version}...")
                client.update_secret_properties(name, version=v.version, enabled=False)
        print("All other versions disabled.")
    except HttpResponseError as e:
        if "associated with a certificate" in str(e):
            print(f"Error: Secret '{name}' is associated with a certificate. Please manage the certificate versions instead.")
        else:
            print(f"Error disabling old secret versions: {e}")
    except Exception as e:
        print(f"Error disabling old secret versions: {e}")

def disable_all_but_newest_certificate_version(name):
    try:
        client = get_certificate_client()
        print(f"Fetching versions for certificate '{name}'...")
        versions = list(client.list_properties_of_certificate_versions(certificate_name=name))
        if not versions:
            print("No versions found.")
            return

        # Sort by created_on descending
        versions.sort(key=lambda x: x.created_on, reverse=True)
        newest = versions[0]
        print(f"Newest version is {newest.version} (Created: {newest.created_on})")

        for v in versions[1:]:
            if v.enabled:
                print(f"Disabling version {v.version}...")
                client.update_certificate_properties(certificate_name=name, version=v.version, enabled=False)
        print("All other versions disabled.")
    except Exception as e:
        print(f"Error disabling old certificate versions: {e}")
