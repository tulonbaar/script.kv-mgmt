import unittest
from unittest.mock import MagicMock, patch
from src import edit

class TestEdit(unittest.TestCase):

    @patch('src.edit.get_key_client')
    def test_update_key_properties(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        mock_key = MagicMock()
        mock_key.name = "test-key"
        mock_client.update_key_properties.return_value = mock_key

        from datetime import datetime
        nb = datetime(2023, 1, 1)
        ops = ["encrypt", "decrypt"]

        edit.update_key_properties("test-key", enabled=True, key_ops=ops, not_before=nb)

        mock_client.update_key_properties.assert_called_once_with(
            "test-key", 
            enabled=True,
            key_operations=ops,
            not_before=nb
        )

    @patch('src.edit.get_key_client')
    def test_update_key_tags(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # Mock getting existing key
        mock_existing_key = MagicMock()
        mock_existing_key.properties.tags = {"old": "tag"}
        mock_client.get_key.return_value = mock_existing_key

        # Mock update return
        mock_updated_key = MagicMock()
        mock_updated_key.name = "test-key"
        mock_client.update_key_properties.return_value = mock_updated_key

        new_tags = {"new": "tag"}
        edit.update_key_tags("test-key", new_tags)

        # Verify get_key called
        mock_client.get_key.assert_called_once_with("test-key")
        
        # Verify update called with merged tags
        expected_tags = {"old": "tag", "new": "tag"}
        mock_client.update_key_properties.assert_called_once_with("test-key", tags=expected_tags)

    @patch('src.edit.get_secret_client')
    def test_update_secret_value(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # Mock the new secret creation
        mock_new_secret = MagicMock()
        mock_new_secret.name = "test-secret"
        mock_new_secret.properties.version = "v2"
        mock_client.set_secret.return_value = mock_new_secret

        # Mock listing versions
        mock_v1 = MagicMock()
        mock_v1.version = "v1"
        mock_v1.enabled = True
        
        mock_v2 = MagicMock()
        mock_v2.version = "v2"
        mock_v2.enabled = True # This is the new one, should not be disabled

        mock_client.list_properties_of_secret_versions.return_value = [mock_v1, mock_v2]

        edit.update_secret_value("test-secret", "new-value")

        # Check set_secret called
        mock_client.set_secret.assert_called_once_with("test-secret", "new-value")
        
        # Check list versions called
        mock_client.list_properties_of_secret_versions.assert_called_once_with("test-secret")

        # Check update_secret_properties called only for v1
        mock_client.update_secret_properties.assert_called_once_with("test-secret", version="v1", enabled=False)

    @patch('src.edit.get_secret_client')
    def test_update_secret_tags(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # Mock getting existing secret
        mock_existing_secret = MagicMock()
        mock_existing_secret.properties.tags = {"env": "dev"}
        mock_client.get_secret.return_value = mock_existing_secret

        # Mock update return
        mock_updated_secret = MagicMock()
        mock_updated_secret.name = "test-secret"
        mock_client.update_secret_properties.return_value = mock_updated_secret

        new_tags = {"env": "prod"} # Should overwrite
        edit.update_secret_tags("test-secret", new_tags)

        # Verify get_secret called
        mock_client.get_secret.assert_called_once_with("test-secret")
        
        # Verify update called with merged tags
        expected_tags = {"env": "prod"}
        mock_client.update_secret_properties.assert_called_once_with("test-secret", tags=expected_tags)

    @patch('src.edit.get_certificate_client')
    def test_update_certificate_tags(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # Mock getting existing cert
        mock_existing_cert = MagicMock()
        mock_existing_cert.properties.tags = None # No existing tags
        mock_client.get_certificate.return_value = mock_existing_cert

        mock_cert = MagicMock()
        mock_cert.name = "test-cert"
        mock_client.update_certificate_properties.return_value = mock_cert

        tags = {"env": "prod"}
        edit.update_certificate_tags("test-cert", tags)

        # Verify get_certificate called
        mock_client.get_certificate.assert_called_once_with(certificate_name="test-cert")

        # Verify update called
        mock_client.update_certificate_properties.assert_called_once_with(certificate_name="test-cert", tags=tags)

    @patch('src.edit.get_key_client')
    def test_update_key_version_properties(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        edit.update_key_version_properties("test-key", "v1", False)
        
        mock_client.update_key_properties.assert_called_once_with("test-key", version="v1", enabled=False)

    @patch('src.edit.get_secret_client')
    def test_update_secret_version_properties(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        edit.update_secret_version_properties("test-secret", "v1", False)
        
        mock_client.update_secret_properties.assert_called_once_with("test-secret", version="v1", enabled=False)

    @patch('src.edit.get_certificate_client')
    def test_update_certificate_version_properties(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        edit.update_certificate_version_properties("test-cert", "v1", False)
        
        mock_client.update_certificate_properties.assert_called_once_with(certificate_name="test-cert", version="v1", enabled=False)

if __name__ == '__main__':
    unittest.main()
