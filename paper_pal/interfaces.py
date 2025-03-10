from __future__ import annotations

from typing import TYPE_CHECKING, Protocol
from pathlib import Path

if TYPE_CHECKING:
    from paper_pal.chat import History


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

    def generate_response(self, prompt: Prompt, history: History) -> str | None: ...

    def read_pdf(self, path: Path | str) -> None: ...
