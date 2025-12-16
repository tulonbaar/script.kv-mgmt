import unittest
from unittest.mock import MagicMock, patch
from azure.core.exceptions import HttpResponseError
from src import delete

class TestDeleteError(unittest.TestCase):

    @patch('src.delete.get_secret_client')
    def test_delete_secret_forbidden(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Mock the exception
        error = HttpResponseError(message="Operation \"delete\" is not allowed on this secret, since it is associated with a certificate.")
        mock_client.begin_delete_secret.side_effect = error

        # Capture stdout to verify the message
        with patch('builtins.print') as mock_print:
            delete.delete_secret("test-secret")
            
            # Verify that the specific error message was printed
            mock_print.assert_any_call("Error: Secret 'test-secret' is associated with a certificate. Please delete the certificate instead.")

if __name__ == '__main__':
    unittest.main()
