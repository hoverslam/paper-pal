import unittest
from unittest.mock import patch, MagicMock
from paper_pal.providers import get_api_keys, list_available_providers, load_provider


class TestApiFunctions(unittest.TestCase):
    @patch("os.getenv")
    def test_get_api_keys(self, mock_getenv):
        # Test for API key retrieval when the key is set in the environment variable
        mock_getenv.return_value = "test_api_key"
        api_keys = get_api_keys()
        self.assertEqual(api_keys, {"Google Gemini": "test_api_key"})

        # Test for API key retrieval when the key is not set in the environment variable
        mock_getenv.return_value = None
        api_keys = get_api_keys()
        self.assertEqual(api_keys, {})

    @patch("paper_pal.providers.get_api_keys")
    def test_list_available_providers(self, mock_get_api_keys):
        # Mock the get_api_keys() function to return a valid API key
        mock_get_api_keys.return_value = {"Google Gemini": "test_api_key"}

        # Test the available providers list when the API key is set
        available_providers = list_available_providers()
        self.assertEqual(available_providers, ["Google Gemini"])

        # Test the available providers list when the API key is not set
        mock_get_api_keys.return_value = {}
        available_providers = list_available_providers()
        self.assertEqual(available_providers, [])

    @patch("paper_pal.providers.get_api_keys")
    @patch("paper_pal.providers.GoogleGemini")
    def test_load_provider(self, mock_GoogleGemini, mock_get_api_keys):
        # Mock the get_api_keys() to return a valid API key
        mock_get_api_keys.return_value = {"Google Gemini": "test_api_key"}

        # Mock GoogleGemini constructor
        mock_provider_instance = MagicMock()
        mock_GoogleGemini.return_value = mock_provider_instance

        # Test loading a provider
        provider = load_provider("Google Gemini")
        mock_GoogleGemini.assert_called_with("test_api_key")
        self.assertEqual(provider, mock_provider_instance)

        # Test if loading a provider with an invalid name raises an exception
        with self.assertRaises(KeyError):
            load_provider("Invalid Provider")


if __name__ == "__main__":
    unittest.main()
