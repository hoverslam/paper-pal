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
    def __init__(self) -> None:
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
        return self._layout

    @property
    def btn_swap_panels(self) -> pn.widgets.ButtonIcon:
        return self._btn_swap_panels


class ChatPanel:
    def __init__(self, session: Session) -> None:
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
        return self._layout

    @property
    def interface(self) -> pn.chat.ChatInterface:
        return self._chat_interface

    def _response_callback(self, input_message: str, input_user: str, instance: pn.chat.ChatInterface) -> str:
        history = instance.serialize()
        prompt = history.pop()
        return self._session.provider.generate_response(prompt["content"], history, self._session.pdf_data)

    def _update_sct_provider(self, event) -> None:
        self._sct_model.options = self._session.provider.list_available_models()


class ControlButtons:
    def __init__(self, session: Session, chat_interface: pn.chat.ChatInterface, pdf_viewer: PDFPanel) -> None:
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
        return self.layout

    def _select_file(self, event) -> None:
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
        prompt = PaperSummaryPrompt()
        message = pn.chat.ChatMessage(
            prompt.content,
            user="Summary",
            avatar="✨",
            show_reaction_icons=False,
        )
        self._chat_interface.send(message)

    def _extract_problem(self, event):
        prompt = ProblemStatementPrompt()
        message = pn.chat.ChatMessage(prompt.content, user="Problem Statement", avatar="⚠️", show_reaction_icons=False)
        self._chat_interface.send(message)

    def _break_down_methodology(self, event):
        prompt = MethodologyPrompt()
        message = pn.chat.ChatMessage(prompt.content, user="Methodology", avatar="⚙️", show_reaction_icons=False)
        self._chat_interface.send(message)

    def _identify_results(self, event):
        prompt = KeyFindingsPrompt()
        message = pn.chat.ChatMessage(
            prompt.content, user="Results & Key Findings", avatar="📊", show_reaction_icons=False
        )
        self._chat_interface.send(message)


class PDFPanel:
    def __init__(self) -> None:
        self._viewer: pn.pane.PDF = pn.pane.PDF(sizing_mode="stretch_both")

    def __call__(self) -> pn.viewable.Viewable:
        return self._viewer

    def update(self, file_path: Path) -> None:
        self._viewer.object = file_path
        self._viewer.embed = True  # type: ignore


class MainLayout:
    def __init__(self, session: Session) -> None:
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
        self._header().servable()
        self._layout.servable()

    def _swap_panels(self, event) -> None:
        self._layout.objects = [self._layout[2], self._layout[1], self._layout[0]]
