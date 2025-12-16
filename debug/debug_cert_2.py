from azure.keyvault.certificates import CertificatePolicy

try:
    policy = CertificatePolicy.get_default()
    print(f"Original subject: {policy.subject}")
    policy.subject = "CN=newsubject"
    print(f"New subject: {policy.subject}")
except Exception as e:
    print(f"Error setting subject: {e}")

try:
    policy = CertificatePolicy.get_default()
    print(f"Original issuer_name: {policy.issuer_name}")
    policy.issuer_name = "Self" # This caused the first error
    print(f"New issuer_name: {policy.issuer_name}")
except Exception as e:
    print(f"Error setting issuer_name: {e}")
