from __future__ import annotations

from paper_pal.providers import list_available_providers
from paper_pal.chat import (
    PaperSummaryPrompt,
    ProblemStatementPrompt,
    MethodologyPrompt,
    KeyFindingsPrompt,
)

from typing import TYPE_CHECKING

import panel as pn
from pathlib import Path
from tkinter import Tk, filedialog

if TYPE_CHECKING:
    from app import Session

pn.extension()


class Header:
    """Represents the header section of the application with a title and a button for swapping panels."""

    def __init__(self) -> None:
        """Initializes the Header with a title and a swap button."""
        self._title = pn.pane.Str("PaperPal 🤝", styles={"font-size": "2em", "margin-right": "auto", "color": "White"})
        self._btn_swap_panels = pn.widgets.ButtonIcon(
            icon="transfer", active_icon="transfer", size="2em", styles={"color": "White"}
        )
        self._layout = pn.FlexBox(
            self._title,
            self._btn_swap_panels,
            align_content="center",
            align_items="center",
            styles={
                "background_color": "LightSkyBlue",
                "border-bottom": "2px solid LightSteelBlue",
                "height": "50px",
                "margin-bottom": "10px",
            },
        )

    def __call__(self) -> pn.viewable.Viewable:
        """Returns the layout for the header section.

        Returns:
            pn.viewable.Viewable: The header layout to be displayed.
        """
        return self._layout

    @property
    def btn_swap_panels(self) -> pn.widgets.ButtonIcon:
        """Gets the button for swapping panels.

        Returns:
            pn.widgets.ButtonIcon: The button widget for swapping panels.
        """
        return self._btn_swap_panels


class ChatPanel:
    """Represents the chat panel of the application, allowing interaction with the provider and managing chat history."""

    def __init__(self, session: Session) -> None:
        """Initializes the chat panel with the given session and sets up widgets for interaction.

        Args:
            session (Session): The session object that holds provider and other session-related data.
        """
        self._session = session
        self._sct_provider = pn.widgets.Select(options=list_available_providers(), sizing_mode="stretch_width")
        self._sct_model = pn.widgets.Select(
            options=session.provider.list_available_models(), sizing_mode="stretch_width"
        )
        self._chat_interface = pn.chat.ChatInterface(
            avatar="👨‍🎓",
            widgets=pn.chat.ChatAreaInput(placeholder="Press Ctrl + Enter to send", enter_sends=False),
            show_rerun=False,
            show_button_name=False,
            callback=self._response_callback,
            callback_user="PaperPal",
            callback_avatar="🤝",
            message_params={"show_reaction_icons": False},
            sizing_mode="stretch_height",
        )
        self._layout = pn.Column(pn.Row(self._sct_provider, self._sct_model), self._chat_interface)

        self._sct_provider.param.watch(self._session.update_provider, "value")
        self._sct_provider.param.watch(self._update_sct_provider, "value")
        self._sct_model.param.watch(self._session.update_model, "value")

    def __call__(self) -> pn.viewable.Viewable:
        """Returns the layout for the chat panel.

        Returns:
            pn.viewable.Viewable: The chat panel layout to be displayed.
        """
        return self._layout

    @property
    def interface(self) -> pn.chat.ChatInterface:
        """Gets the chat interface of the panel.

        Returns:
            pn.chat.ChatInterface: The chat interface widget.
        """
        return self._chat_interface

    def _response_callback(self, input_message: str, input_user: str, instance: pn.chat.ChatInterface) -> str:
        """Handles the response callback for sending messages and generating responses.

        Args:
            input_message (str): The input message from the user.
            input_user (str): The user who sent the message.
            instance (pn.chat.ChatInterface): The chat interface instance.

        Returns:
            str: The generated response to be displayed.
        """
        history = instance.serialize()
        prompt = history.pop()
        return self._session.provider.generate_response(prompt["content"], history, self._session.pdf_data)

    def _update_sct_provider(self, event) -> None:
        """Updates the model options in the provider select widget when a new provider is selected.

        Args:
            event: The event triggered by changing the provider.
        """
        self._sct_model.options = self._session.provider.list_available_models()


class ControlButtons:
    """Handles control buttons for interacting with the application, including selecting PDFs and generating summaries."""

    def __init__(self, session: Session, chat_interface: pn.chat.ChatInterface, pdf_viewer: PDFPanel) -> None:
        """Initializes the control buttons and sets up their actions.

        Args:
            session (Session): The session object that holds provider and other session-related data.
            chat_interface (pn.chat.ChatInterface): The chat interface for sending messages.
            pdf_viewer (PDFPanel): The PDF panel for displaying PDF content.
        """
        self._session = session
        self._chat_interface = chat_interface
        self._pdf_viewer = pdf_viewer

        self._btn_select_pdf = pn.widgets.Button(icon="file", description="Select PDF", button_type="success")
        self._btn_paper_summary = pn.widgets.Button(icon="sparkles", description="Summarize paper")
        self._btn_problem_statement = pn.widgets.Button(icon="info-triangle", description="Extract problem statement")
        self._btn_methodology_breakdown = pn.widgets.Button(icon="settings", description="Break down research methods")
        self._btn_key_findings = pn.widgets.Button(icon="chart-bar", description="Identify results and key findings")

        self.layout: pn.Column = pn.Column(
            self._btn_select_pdf,
            pn.Spacer(height=10),
            self._btn_paper_summary,
            self._btn_problem_statement,
            self._btn_methodology_breakdown,
            self._btn_key_findings,
            width=50,
        )

        self._btn_select_pdf.on_click(self._select_file)
        self._btn_paper_summary.on_click(self._summarize_paper)
        self._btn_problem_statement.on_click(self._extract_problem)
        self._btn_methodology_breakdown.on_click(self._break_down_methodology)
        self._btn_key_findings.on_click(self._identify_results)

    def __call__(self) -> pn.viewable.Viewable:
        """Returns the layout for the control buttons.

        Returns:
            pn.viewable.Viewable: The control buttons layout to be displayed.
        """
        return self.layout

    def _select_file(self, event) -> None:
        """Handles file selection for PDFs, loading the file into the session and the PDF viewer.

        Args:
            event: The event triggered by selecting a PDF file.
        """
        root = Tk()
        root.withdraw()
        root.call("wm", "attributes", ".", "-topmost", True)
        file_path = Path(filedialog.askopenfilename())
        self._session.pdf_data = file_path.read_bytes()
        self._session.pdf_path = file_path
        self._chat_interface.clear()
        if file_path.suffix == ".pdf":
            self._pdf_viewer.update(file_path)

    def _summarize_paper(self, event):
        """Generates a paper summary prompt and sends it to the chat interface.

        Args:
            event: The event triggered by clicking the summarize paper button.
        """
        prompt = PaperSummaryPrompt()
        message = pn.chat.ChatMessage(
            prompt.content,
            user="Summary",
            avatar="✨",
            show_reaction_icons=False,
        )
        self._chat_interface.send(message)

    def _extract_problem(self, event):
        """Generates a problem statement prompt and sends it to the chat interface.

        Args:
            event: The event triggered by clicking the extract problem statement button.
        """
        prompt = ProblemStatementPrompt()
        message = pn.chat.ChatMessage(prompt.content, user="Problem Statement", avatar="⚠️", show_reaction_icons=False)
        self._chat_interface.send(message)

    def _break_down_methodology(self, event):
        """Generates a methodology breakdown prompt and sends it to the chat interface.

        Args:
            event: The event triggered by clicking the breakdown methodology button.
        """
        prompt = MethodologyPrompt()
        message = pn.chat.ChatMessage(prompt.content, user="Methodology", avatar="⚙️", show_reaction_icons=False)
        self._chat_interface.send(message)

    def _identify_results(self, event):
        """Generates a key findings prompt and sends it to the chat interface.

        Args:
            event: The event triggered by clicking the identify key findings button.
        """
        prompt = KeyFindingsPrompt()
        message = pn.chat.ChatMessage(
            prompt.content, user="Results & Key Findings", avatar="📊", show_reaction_icons=False
        )
        self._chat_interface.send(message)


class PDFPanel:
    """Represents the panel for displaying PDFs."""

    def __init__(self) -> None:
        """Initializes the PDF viewer panel."""
        self._viewer: pn.pane.PDF = pn.pane.PDF(sizing_mode="stretch_both")

    def __call__(self) -> pn.viewable.Viewable:
        """Returns the PDF viewer panel.

        Returns:
            pn.viewable.Viewable: The PDF viewer to be displayed.
        """
        return self._viewer

    def update(self, file_path: Path) -> None:
        """Updates the PDF viewer with a new PDF file.

        Args:
            file_path (Path): The path to the PDF file to be displayed.
        """
        self._viewer.object = file_path
        self._viewer.embed = True  # type: ignore


class MainLayout:
    """The main layout of the application, combining chat, control buttons, and PDF viewer."""

    def __init__(self, session: Session) -> None:
        """Initializes the main layout with the provided session and components.

        Args:
            session (Session): The session object that holds provider and other session-related data.
        """
        self._chat_panel = ChatPanel(session)
        self._pdf_panel = PDFPanel()
        self._control_buttons = ControlButtons(session, self._chat_panel.interface, self._pdf_panel)
        self._header = Header()
        self._layout = pn.Row(
            self._chat_panel(),
            self._control_buttons(),
            self._pdf_panel(),
            styles={"height": "calc(100vh - 60px)"},
        )

        self._header.btn_swap_panels.on_click(self._swap_panels)

    def show(self) -> None:
        """Displays the layout by making the header and main layout servable."""
        self._header().servable()
        self._layout.servable()

    def _swap_panels(self, event) -> None:
        """Swaps the order of the panels in the layout when the swap button is clicked.

        Args:
            event: The event triggered by clicking the swap button.
        """
        self._layout.objects = [self._layout[2], self._layout[1], self._layout[0]]
