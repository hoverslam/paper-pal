from typing import Protocol
from pathlib import Path


class Prompt(Protocol):
    @property
    def role(self) -> str: ...

    @property
    def content(self) -> str: ...


class APIProvider(Protocol):
    api_key: str

    @property
    def name(self) -> str: ...

    @property
    def model(self) -> str: ...

    @model.setter
    def model(self, model_name: str) -> None: ...

    @property
    def system_instructions(self) -> str | None: ...

    def list_available_models(self) -> list[str]: ...

    def generate_response(self, prompt: Prompt, history) -> str | None: ...

    def read_pdf(self, path: Path | str) -> None: ...
