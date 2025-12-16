import unittest
from unittest.mock import MagicMock, patch
from src import edit
from datetime import datetime, timedelta

class TestVersionManagement(unittest.TestCase):

    @patch('src.edit.get_secret_client')
    def test_disable_all_but_newest_secret_version(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Create mock versions
        v1 = MagicMock()
        v1.version = "v1"
        v1.created_on = datetime.now() - timedelta(days=10)
        v1.enabled = True

        v2 = MagicMock()
        v2.version = "v2"
        v2.created_on = datetime.now() - timedelta(days=5)
        v2.enabled = True

        v3 = MagicMock()
        v3.version = "v3"
        v3.created_on = datetime.now() # Newest
        v3.enabled = True

        # Return them in mixed order
        mock_client.list_properties_of_secret_versions.return_value = [v1, v3, v2]

        edit.disable_all_but_newest_secret_version("test-secret")

        # Verify v3 is NOT disabled (it's the newest)
        # Verify v1 and v2 ARE disabled
        
        # Check calls to update_secret_properties
        # Should be called for v1 and v2 with enabled=False
        
        calls = mock_client.update_secret_properties.call_args_list
        self.assertEqual(len(calls), 2)
        
        # Extract args from calls
        disabled_versions = [call[1]['version'] for call in calls]
        self.assertIn('v1', disabled_versions)
        self.assertIn('v2', disabled_versions)
        self.assertNotIn('v3', disabled_versions)

    @patch('src.edit.get_key_client')
    def test_disable_all_but_newest_key_version(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        v1 = MagicMock()
        v1.version = "v1"
        v1.created_on = datetime.now()
        v1.enabled = True

        v2 = MagicMock()
        v2.version = "v2"
        v2.created_on = datetime.now() - timedelta(days=1)
        v2.enabled = True

        mock_client.list_properties_of_key_versions.return_value = [v1, v2]

        edit.disable_all_but_newest_key_version("test-key")

        # v1 is newest, v2 should be disabled
        mock_client.update_key_properties.assert_called_once_with("test-key", version="v2", enabled=False)

if __name__ == '__main__':
    unittest.main()
