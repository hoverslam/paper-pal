from __future__ import annotations

from paper_pal.interfaces import APIProvider

import os
from pathlib import Path
from abc import ABC
from dotenv import load_dotenv

from google import genai
from google.genai import types


load_dotenv(dotenv_path=Path(".env"))


def get_api_keys() -> dict:
    api_keys = {
        "Google Gemini": os.getenv("GEMINI_API_KEY"),
    }

    return {key: value for key, value in api_keys.items() if value is not None}


def list_available_providers() -> list:
    providers = ["Google Gemini"]

    return list(set(providers) & set(get_api_keys()))


def load_provider(name: str) -> APIProvider:
    providers = {
        "Google Gemini": GoogleGemini,
    }

    api_key = get_api_keys()[name]
    provider = providers[name](api_key)

    return provider


class BaseProvider(ABC, APIProvider):
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self._model = self.list_available_models()[0]
        self._system_instructions = self._load_system_instructions("./configs/system_instructions.txt")
        self._pdf_content = None

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, model_name: str) -> None:
        if model_name not in self.list_available_models():
            raise ValueError(f"Invalid model name: {model_name}")
        self._model = model_name

    @property
    def system_instructions(self) -> str | None:
        self._system_instructions

    def _load_system_instructions(self, path: Path | str) -> str:
        path = Path(path)
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: System prompt file not found at {path}")

        return text

    @property
    def name(self) -> str:
        raise NotImplementedError

    def generate_response(self, prompt: str, history: list[dict], pdf_content: bytes | None) -> str:
        raise NotImplementedError

    def list_available_models(self) -> list[str]:
        raise NotImplementedError


class GoogleGemini(BaseProvider):
    def __init__(self, api_key: str) -> None:
        super().__init__(api_key)
        self._client = genai.Client(api_key=self._api_key)

    @property
    def name(self) -> str:
        return f"Google Gemini | {self.model}"

    def list_available_models(self) -> list[str]:
        return [
            "gemini-2.0-flash-exp",
            "gemini-2.0-pro-exp-02-05",
            "gemini-2.0-flash-thinking-exp-01-21",
        ]

    def generate_response(self, prompt: str, history: list[dict], pdf_content: bytes | None) -> str:
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
