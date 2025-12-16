from azure.keyvault.keys import KeyClient
import inspect

print(inspect.signature(KeyClient.update_key_properties))
