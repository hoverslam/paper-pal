from __future__ import annotations

from typing import Protocol


class Prompt(Protocol):
    @property
    def role(self) -> str: ...

    @property
    def content(self) -> str: ...


class APIProvider(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def model(self) -> str: ...

    @model.setter
    def model(self, model_name: str) -> None: ...

    @property
    def system_instructions(self) -> str | None: ...

    def list_available_models(self) -> list[str]: ...

    def generate_response(self, prompt: str, history: list[dict], pdf_content: bytes | None) -> str: ...
