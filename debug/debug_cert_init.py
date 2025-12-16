from azure.keyvault.certificates import CertificatePolicy
import inspect

print(inspect.signature(CertificatePolicy.__init__))
