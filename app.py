from paper_pal.providers import list_available_providers, load_provider
from paper_pal.interfaces import APIProvider
from paper_pal.ui import MainLayout

from pathlib import Path


class Session:
    def __init__(self, provider: APIProvider, pdf_data: bytes | None = None, pdf_path: Path | None = None) -> None:
        self.provider = provider
        self.pdf_data = pdf_data
        self.pdf_path = pdf_path

    def update_provider(self, event) -> None:
        self.provider = load_provider(event.new)

    def update_model(self, event) -> None:
        self.provider.model = event.new


session = Session(load_provider(list_available_providers()[0]))
MainLayout(session).show()
