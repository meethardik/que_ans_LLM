import os
import logging
from azure.identity import ClientSecretCredential #DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

class GetConfiguration:
    
    logging.basicConfig(level=logging.DEBUG)

    def __init__(self, secret_name: str = "", keyvault_name: str = "") -> None:
        self.secret_name = secret_name
        self.keyvault_name = keyvault_name

    def get_openai_api_key(self) -> str:
        secret = None
        try:
            keyvault_uri = f"https://{self.keyvault_name}.vault.azure.net/"
            
            if not keyvault_uri:
                raise ValueError("Key Vault URI is not provided. Please set the KeyVault_Name environment variable.")

            tenantId = os.getenv("AZURE_TENANT_ID")
            clientId = os.getenv("AZURE_CLIENT_ID")
            clientSecret = os.getenv("AZURE_CLIENT_SECRET")

            credentials = ClientSecretCredential(
                tenant_id=tenantId,
                client_id=clientId,
                client_secret=clientSecret
            )

            client = SecretClient(vault_url=keyvault_uri, credential=credentials)
            secret = client.get_secret(self.secret_name)
            logging.debug(f"Secret '{self.secret_name}' value: {secret.value}")

            return str(secret.value)
        except Exception as e:
            logging.error(f"Error retrieving secret '{self.secret_name}' from Key Vault '{self.keyvault_name}': {e}")
            return ""