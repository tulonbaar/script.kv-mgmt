import unittest
from unittest.mock import MagicMock, patch
from azure.core.exceptions import HttpResponseError
from src import edit
from datetime import datetime, timedelta

class TestEditError(unittest.TestCase):

    @patch('src.edit.get_key_client')
    def test_disable_key_version_forbidden(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Mock versions
        v1 = MagicMock()
        v1.version = "v1"
        v1.created_on = datetime.now()
        v1.enabled = True

        v2 = MagicMock()
        v2.version = "v2"
        v2.created_on = datetime.now() - timedelta(days=1)
        v2.enabled = True

        mock_client.list_properties_of_key_versions.return_value = [v1, v2]

        # Mock the exception on update
        error = HttpResponseError(message="Operation \"update\" is not allowed on this Key, since it is associated with a certificate.")
        mock_client.update_key_properties.side_effect = error

        # Capture stdout
        with patch('builtins.print') as mock_print:
            edit.disable_all_but_newest_key_version("test-key")
            
            # Verify that the specific error message was printed
            mock_print.assert_any_call("Error: Key 'test-key' is associated with a certificate. Please manage the certificate versions instead.")

    @patch('src.edit.get_secret_client')
    def test_disable_secret_version_forbidden(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Mock versions
        v1 = MagicMock()
        v1.version = "v1"
        v1.created_on = datetime.now()
        v1.enabled = True

        v2 = MagicMock()
        v2.version = "v2"
        v2.created_on = datetime.now() - timedelta(days=1)
        v2.enabled = True

        mock_client.list_properties_of_secret_versions.return_value = [v1, v2]

        # Mock the exception on update
        error = HttpResponseError(message="Operation \"update\" is not allowed on this Secret, since it is associated with a certificate.")
        mock_client.update_secret_properties.side_effect = error

        # Capture stdout
        with patch('builtins.print') as mock_print:
            edit.disable_all_but_newest_secret_version("test-secret")
            
            # Verify that the specific error message was printed
            mock_print.assert_any_call("Error: Secret 'test-secret' is associated with a certificate. Please manage the certificate versions instead.")

    @patch('src.edit.get_secret_client')
    def test_update_secret_version_forbidden(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Mock the exception on update
        error = HttpResponseError(message="Operation \"update\" is not allowed on this secret, since it is associated with a certificate.")
        mock_client.update_secret_properties.side_effect = error

        # Capture stdout
        with patch('builtins.print') as mock_print:
            edit.update_secret_version_properties("test-secret", "v1", True)
            
            # Verify that the specific error message was printed
            mock_print.assert_any_call("Error: Secret 'test-secret' is associated with a certificate. Please manage the certificate versions instead.")

if __name__ == '__main__':
    unittest.main()
