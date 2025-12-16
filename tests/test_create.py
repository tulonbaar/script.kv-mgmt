import unittest
from unittest.mock import MagicMock, patch, ANY
from src import create

class TestCreate(unittest.TestCase):

    @patch('src.create.get_key_client')
    def test_create_key(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        mock_key = MagicMock()
        mock_key.name = "test-key"
        mock_key.id = "https://kv.vault.azure.net/keys/test-key/version"
        mock_key.key_type = "RSA"
        mock_key.properties.enabled = True
        mock_client.create_key.return_value = mock_key

        create.create_key("test-key")

        mock_client.create_key.assert_called_once_with("test-key", "RSA")

    @patch('src.create.get_key_client')
    def test_create_key_advanced(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        mock_key = MagicMock()
        mock_key.name = "test-key-adv"
        mock_key.id = "https://kv.vault.azure.net/keys/test-key-adv/version"
        mock_key.key_type = "RSA"
        mock_key.properties.enabled = True
        mock_client.create_key.return_value = mock_key

        from datetime import datetime
        nb = datetime(2023, 1, 1)
        exp = datetime(2024, 1, 1)

        create.create_key("test-key-adv", kty="RSA", size=4096, not_before=nb, expires_on=exp)

        mock_client.create_key.assert_called_once_with(
            "test-key-adv", 
            "RSA", 
            size=4096, 
            not_before=nb, 
            expires_on=exp
        )

    @patch('src.create.get_secret_client')
    def test_create_secret(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        mock_secret = MagicMock()
        mock_secret.name = "test-secret"
        mock_client.set_secret.return_value = mock_secret

        create.create_secret("test-secret", "value")

        mock_client.set_secret.assert_called_once_with("test-secret", "value")

    @patch('src.create.get_certificate_client')
    def test_create_certificate(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # Mock the poller
        mock_poller = MagicMock()
        mock_client.begin_create_certificate.return_value = mock_poller

        create.create_certificate("test-cert", "mysubject")

        # Verify begin_create_certificate was called with correct name and a policy
        mock_client.begin_create_certificate.assert_called_once()
        args, kwargs = mock_client.begin_create_certificate.call_args
        self.assertEqual(kwargs['certificate_name'], "test-cert")
        self.assertIsNotNone(kwargs['policy'])
        self.assertEqual(kwargs['policy'].subject, "CN=mysubject")

if __name__ == '__main__':
    unittest.main()
