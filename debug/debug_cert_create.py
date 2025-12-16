from azure.keyvault.certificates import CertificatePolicy

try:
    policy = CertificatePolicy(issuer_name="Self", subject="CN=mysubject")
    print(f"Created policy with subject: {policy.subject}")
    print(f"Key type: {policy.key_type}")
    print(f"Key size: {policy.key_size}")
    print(f"Validity: {policy.validity_in_months}")
except Exception as e:
    print(f"Error creating policy: {e}")
