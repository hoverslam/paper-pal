from paper_pal.providers import list_available_providers, load_provider
from paper_pal.interfaces import APIProvider
from paper_pal.chat import (
    PaperSummaryPrompt,
    ProblemStatementPrompt,
    MethodologyPrompt,
    KeyFindingsPrompt,
)

from pathlib import Path
from tkinter import Tk, filedialog
from dataclasses import dataclass

import panel as pn


pn.extension()


@dataclass
class CurrentProvider:
    obj: APIProvider

    def update_provider(self, event) -> None:
        self.obj = load_provider(event.new)

    def update_model(self, event) -> None:
        self.obj.model = event.new


@dataclass
class CurrentPDF:
    obj: bytes | None = None


providers = list_available_providers()
current_provider = CurrentProvider(load_provider(providers[0]))
current_pdf = CurrentPDF()

# Header
title = pn.pane.Str("PaperPal 🤝", styles={"font-size": "2em", "margin-right": "auto", "color": "White"})
btn_transfer = pn.widgets.ButtonIcon(icon="transfer", active_icon="transfer", size="2em", styles={"color": "White"})
btn_help = pn.widgets.ButtonIcon(icon="help", active_icon="help", size="2em", styles={"color": "White"})
header_section = pn.FlexBox(
    title,
    btn_transfer,
    align_content="center",
    align_items="center",
    styles={
        "background_color": "LightSkyBlue",
        "border-bottom": "2px solid LightSteelBlue",
        "height": "50px",
        "margin-bottom": "10px",
    },
)
header_section.servable()


# Chat modul
def response_callback(input_message: str, input_user: str, instance: pn.chat.ChatInterface) -> str:
    history = instance.serialize()
    prompt = history.pop()  # The last item of the history is the current prompt.
    response_message = current_provider.obj.generate_response(prompt["content"], history, current_pdf.obj)

    return response_message


sct_provider = pn.widgets.Select(options=providers, sizing_mode="stretch_width")
sct_model = pn.widgets.Select(options=current_provider.obj.list_available_models(), sizing_mode="stretch_width")
chat_interface = pn.chat.ChatInterface(
    avatar="👨‍🎓",
    widgets=pn.chat.ChatAreaInput(placeholder="Press Ctrl + Enter to send", enter_sends=False),
    show_rerun=False,
    show_button_name=False,
    callback=response_callback,
    callback_user="PaperPal",
    callback_avatar="🤝",
    message_params={"show_reaction_icons": False},
    sizing_mode="stretch_height",
)
chat_modul = pn.Column(pn.Row(sct_provider, sct_model), chat_interface)

# Control buttons
btn_select_pdf = pn.widgets.Button(
    icon="file",
    icon_size="0.9em",
    description="Select PDF",
    button_type="success",
)
btn_paper_summary = pn.widgets.Button(
    icon="sparkles",
    icon_size="0.9em",
    description="Summarize paper",
)
btn_problem_statement = pn.widgets.Button(
    icon="info-triangle",
    icon_size="0.9em",
    description="Extract problem statement",
)
btn_methodology_breakdown = pn.widgets.Button(
    icon="settings",
    icon_size="0.9em",
    description="Break down research methods",
)
btn_key_findings = pn.widgets.Button(
    icon="chart-bar",
    icon_size="0.9em",
    description="Identify results and key findings",
)
contol_buttons = pn.Column(
    btn_select_pdf,
    pn.Spacer(height=10),
    btn_paper_summary,
    btn_problem_statement,
    btn_methodology_breakdown,
    btn_key_findings,
    width=50,
)

# PDF Viewer
pdf_viewer = pn.pane.PDF(sizing_mode="stretch_both")

# Main layout
main_section = pn.Row(
    chat_modul,
    contol_buttons,
    pdf_viewer,
    styles={"height": "calc(100vh - 60px)"},
)
main_section.servable()


# Action functions
def swap_panels(event) -> None:
    main_section.objects = [main_section[2], main_section[1], main_section[0]]
    print(current_provider.obj.name)


def select_file(event) -> None:
    root = Tk()
    root.withdraw()
    root.call("wm", "attributes", ".", "-topmost", True)
    file_path = Path(filedialog.askopenfilename())
    current_pdf.obj = file_path.read_bytes()
    chat_interface.clear()

    if file_path.suffix == ".pdf":
        for i, obj in enumerate(main_section):
            if isinstance(obj, pn.pane.PDF):
                main_section[i] = pn.pane.PDF(file_path, embed=True, sizing_mode="stretch_both")  # type: ignore


def update_sct_provider(event) -> None:
    sct_model.options = current_provider.obj.list_available_models()


def summarize_paper(event) -> None:
    prompt = PaperSummaryPrompt()
    message = pn.chat.ChatMessage(
        prompt.content,
        user="Summary",
        avatar="✨",
        show_reaction_icons=False,
    )
    chat_interface.send(message)


def extract_problem(event) -> None:
    prompt = ProblemStatementPrompt()
    message = pn.chat.ChatMessage(prompt.content, user="Problem Statement", avatar="⚠️", show_reaction_icons=False)
    chat_interface.send(message)


def break_down_methodology(event) -> None:
    prompt = MethodologyPrompt()
    message = pn.chat.ChatMessage(prompt.content, user="Methodology", avatar="⚙️", show_reaction_icons=False)
    chat_interface.send(message)


def identify_results(event) -> None:
    prompt = KeyFindingsPrompt()
    message = pn.chat.ChatMessage(prompt.content, user="Results & Key Findings", avatar="📊", show_reaction_icons=False)
    chat_interface.send(message)


# Actions
btn_transfer.on_click(swap_panels)
btn_select_pdf.on_click(select_file)
btn_paper_summary.on_click(summarize_paper)
btn_problem_statement.on_click(extract_problem)
btn_methodology_breakdown.on_click(break_down_methodology)
btn_key_findings.on_click(identify_results)
sct_provider.param.watch(current_provider.update_provider, "value")
sct_provider.param.watch(update_sct_provider, "value")
sct_model.param.watch(current_provider.update_model, "value")
