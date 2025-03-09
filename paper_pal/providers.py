from paper_pal.interfaces import APIProvider, Prompt
from paper_pal.chat import History

from pathlib import Path

from google import genai
from google.genai import types


class GoogleGemini(APIProvider):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self._client = genai.Client(api_key=self.api_key)
        self._model = self.list_available_models()[0]
        self._pdf_content = None
        self._system_instructions = self._load_system_instructions("./configs/system_instructions.txt")

    @property
    def name(self) -> str:
        return "Google Gemini"

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

    def list_available_models(self) -> list[str]:
        return [
            "gemini-2.0-flash-exp",
            "gemini-2.0-pro-exp-02-05",
            "gemini-2.0-flash-thinking-exp-01-21",
        ]

    def generate_response(self, prompt: Prompt, history: History) -> str | None:
        # TODO: Add history
        if self._pdf_content is not None:
            contents = [
                types.Part.from_bytes(
                    data=self._pdf_content,
                    mime_type="application/pdf",
                ),
                prompt.content,
            ]
        else:
            contents = prompt.content

        response = self._client.models.generate_content(
            model=self._model,
            config=types.GenerateContentConfig(system_instruction=self._system_instructions),
            contents=contents,
        )

        return response.text

    def read_pdf(self, path: Path | str) -> None:
        path = Path(path)
        try:
            self._pdf_content = path.read_bytes()
        except FileNotFoundError:
            print(f"Error: PDF not found at {path}")

    def _load_system_instructions(self, path: Path | str) -> str:
        path = Path(path)
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: System prompt file not found at {path}")

        return text
