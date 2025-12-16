from azure.keyvault.certificates import CertificatePolicy

try:
    policy = CertificatePolicy.get_default()
    print(f"Policy type: {type(policy)}")
    print(f"Dir policy: {dir(policy)}")
    if hasattr(policy, 'x509_certificate_properties'):
        print(f"x509_certificate_properties: {policy.x509_certificate_properties}")
    else:
        print("No x509_certificate_properties attribute")
except Exception as e:
    print(f"Error: {e}")
