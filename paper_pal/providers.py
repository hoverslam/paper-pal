from __future__ import annotations

from paper_pal.interfaces import APIProvider

import os
from pathlib import Path
from abc import ABC
from dotenv import load_dotenv

from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv(dotenv_path=Path(".env"))


def get_api_keys() -> dict:
    """Retrieve the API keys from environment variables.

    Returns:
        dict: A dictionary with API provider names as keys and corresponding API keys as values.
    """
    api_keys = {
        "Google Gemini": os.getenv("GEMINI_API_KEY"),
    }

    return {key: value for key, value in api_keys.items() if value is not None}


def list_available_providers() -> list:
    """List available API providers based on the API keys present in the environment variables.

    Returns:
        list: A list of available providers with valid API keys.
    """
    providers = ["Google Gemini"]

    return list(set(providers) & set(get_api_keys()))


def load_provider(name: str) -> APIProvider:
    """Load the specified API provider class based on the provided name.

    Args:
        name (str): The name of the API provider to load.

    Returns:
        APIProvider: An instance of the specified API provider.

    Raises:
        KeyError: If the provider name is not found in the available providers.
    """
    providers = {
        "Google Gemini": GoogleGemini,
    }

    api_key = get_api_keys()[name]
    provider = providers[name](api_key)

    return provider


class BaseProvider(ABC, APIProvider):
    """Base class for API providers, implementing common functionality for interacting with APIs."""

    def __init__(self, api_key: str) -> None:
        """Initialize the base provider with an API key and load necessary configurations.

        Args:
            api_key (str): The API key for authenticating with the provider.
        """
        self._api_key = api_key
        self._model = self.list_available_models()[0]
        self._system_instructions = self._load_system_instructions("./configs/system_instructions.txt")
        self._pdf_content = None

    @property
    def model(self) -> str:
        """Get the current model name.

        Returns:
            str: The current model name.
        """
        return self._model

    @model.setter
    def model(self, model_name: str) -> None:
        """Set the model name. Raises an error if the model is invalid.

        Args:
            model_name (str): The name of the model to set.

        Raises:
            ValueError: If the provided model name is not available.
        """
        if model_name not in self.list_available_models():
            raise ValueError(f"Invalid model name: {model_name}")
        self._model = model_name

    @property
    def system_instructions(self) -> str | None:
        """Get the system instructions used for generating responses.

        Returns:
            str | None: The system instructions, or None if not set.
        """
        return self._system_instructions

    def _load_system_instructions(self, path: Path | str) -> str:
        """Load system instructions from a file.

        Args:
            path (Path | str): The file path of the system instructions.

        Returns:
            str: The content of the system instructions file.

        Raises:
            FileNotFoundError: If the instructions file is not found.
        """
        path = Path(path)
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: System prompt file not found at {path}")

        return text

    @property
    def name(self) -> str:
        """Get the name of the API provider.

        This method must be implemented by subclasses.

        Returns:
            str: The name of the API provider.

        Raises:
            NotImplementedError: If not implemented in the subclass.
        """
        raise NotImplementedError

    def generate_response(self, prompt: str, history: list[dict], pdf_content: bytes | None) -> str:
        """Generate a response based on the provided prompt and history.

        Args:
            prompt (str): The prompt for which to generate a response.
            history (list[dict]): The conversation history.
            pdf_content (bytes | None): Optional PDF content to include in the request.

        Returns:
            str: The generated response from the API provider.

        Raises:
            NotImplementedError: If not implemented in the subclass.
        """
        raise NotImplementedError

    def list_available_models(self) -> list[str]:
        """List the models available for the API provider.

        Returns:
            list[str]: A list of available model names.

        Raises:
            NotImplementedError: If not implemented in the subclass.
        """
        raise NotImplementedError


class GoogleGemini(BaseProvider):
    """Implementation of the Google Gemini API provider."""

    def __init__(self, api_key: str) -> None:
        """Initialize the Google Gemini provider with the provided API key.

        Args:
            api_key (str): The API key for authenticating with the Google Gemini API.
        """
        super().__init__(api_key)
        self._client = genai.Client(api_key=self._api_key)

    @property
    def name(self) -> str:
        """Get the name of the Google Gemini provider, including the model name.

        Returns:
            str: The name of the provider, including the current model.
        """
        return f"Google Gemini | {self.model}"

    def list_available_models(self) -> list[str]:
        """List available models for the Google Gemini provider.

        Returns:
            list[str]: A list of available model names for Google Gemini.
        """
        return [
            "gemini-2.0-flash-exp",
            "gemini-2.0-pro-exp-02-05",
            "gemini-2.0-flash-thinking-exp-01-21",
        ]

    def generate_response(self, prompt: str, history: list[dict], pdf_content: bytes | None) -> str:
        """Generate a response based on the provided prompt, history, and optional PDF content.

        Args:
            prompt (str): The prompt for which to generate a response.
            history (list[dict]): The conversation history.
            pdf_content (bytes | None): Optional PDF content to include in the request.

        Returns:
            str: The generated response from the Google Gemini API.
        """
        content = f"<START | history>{history}<END | history>\n" + prompt
        if pdf_content is not None:
            contents = [
                types.Part.from_bytes(
                    data=pdf_content,
                    mime_type="application/pdf",
                ),
                content,
            ]
        else:
            contents = content

        response = self._client.models.generate_content(
            model=self._model,
            config=types.GenerateContentConfig(system_instruction=self._system_instructions),
            contents=contents,
        )

        return response.text if response.text else "No response from the model."
