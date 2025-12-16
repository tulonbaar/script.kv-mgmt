import unittest
from unittest.mock import MagicMock, patch
from src import delete

class TestDelete(unittest.TestCase):

    @patch('src.delete.get_key_client')
    def test_delete_key(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        mock_poller = MagicMock()
        mock_deleted_key = MagicMock()
        mock_deleted_key.name = "test-key"
        mock_poller.result.return_value = mock_deleted_key
        mock_client.begin_delete_key.return_value = mock_poller

        delete.delete_key("test-key")

        mock_client.begin_delete_key.assert_called_once_with("test-key")
        mock_poller.result.assert_called_once()

    @patch('src.delete.get_secret_client')
    def test_delete_secret(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        mock_poller = MagicMock()
        mock_deleted_secret = MagicMock()
        mock_deleted_secret.name = "test-secret"
        mock_poller.result.return_value = mock_deleted_secret
        mock_client.begin_delete_secret.return_value = mock_poller

        delete.delete_secret("test-secret")

        mock_client.begin_delete_secret.assert_called_once_with("test-secret")
        mock_poller.result.assert_called_once()

    @patch('src.delete.get_certificate_client')
    def test_delete_certificate(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        mock_poller = MagicMock()
        mock_deleted_cert = MagicMock()
        mock_deleted_cert.name = "test-cert"
        mock_poller.result.return_value = mock_deleted_cert
        mock_client.begin_delete_certificate.return_value = mock_poller

        delete.delete_certificate("test-cert")

        mock_client.begin_delete_certificate.assert_called_once_with("test-cert")
        mock_poller.result.assert_called_once()

if __name__ == '__main__':
    unittest.main()
