import unittest
from unittest.mock import MagicMock, patch
from src import get

class TestGet(unittest.TestCase):

    @patch('src.get.get_key_client')
    def test_list_keys(self, mock_get_client):
        # Setup mock
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # Mock return values
        mock_key1 = MagicMock()
        mock_key1.name = "key1"
        mock_key1.enabled = True
        mock_key1.created_on = "2023-01-01"
        
        mock_client.list_properties_of_keys.return_value = [mock_key1]

        # Run function
        get.list_keys()

        # Assertions
        mock_client.list_properties_of_keys.assert_called_once()

    @patch('src.get.get_secret_client')
    def test_list_secrets(self, mock_get_client):
        # Setup mock
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        mock_secret1 = MagicMock()
        mock_secret1.name = "secret1"
        mock_secret1.enabled = True
        mock_secret1.created_on = "2023-01-01"
        
        mock_client.list_properties_of_secrets.return_value = [mock_secret1]

        # Run function
        get.list_secrets()

        # Assertions
        mock_client.list_properties_of_secrets.assert_called_once()

    @patch('src.get.get_certificate_client')
    def test_list_certificates(self, mock_get_client):
        # Setup mock
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        mock_cert1 = MagicMock()
        mock_cert1.name = "cert1"
        mock_cert1.enabled = True
        mock_cert1.created_on = "2023-01-01"
        
        mock_client.list_properties_of_certificates.return_value = [mock_cert1]

        # Run function
        get.list_certificates()

        # Assertions
        mock_client.list_properties_of_certificates.assert_called_once()

if __name__ == '__main__':
    unittest.main()
