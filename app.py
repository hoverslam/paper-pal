from paper_pal.providers import list_available_providers, load_provider
from paper_pal.interfaces import APIProvider
from paper_pal.chat import (
    UserPrompt,
    PaperSummaryPrompt,
    ProblemStatementPrompt,
    MethodologyPrompt,
    KeyFindingsPrompt,
)

from pathlib import Path
from tkinter import Tk, filedialog

import panel as pn


pn.extension()


class Session:
    def __init__(self, provider: APIProvider, pdf_data: bytes | None = None, pdf_path: Path | None = None) -> None:
        self.provider = provider
        self.pdf_data = pdf_data
        self.pdf_path = pdf_path

    def update_provider(self, event) -> None:
        self.provider = load_provider(event.new)

    def update_model(self, event) -> None:
        self.provider.model = event.new


providers = list_available_providers()
session = Session(load_provider(providers[0]))

# Header
title = pn.pane.Str("PaperPal 🤝", styles={"font-size": "2em", "margin-right": "auto", "color": "White"})
btn_transfer = pn.widgets.ButtonIcon(icon="transfer", active_icon="transfer", size="2em", styles={"color": "White"})
btn_help = pn.widgets.ButtonIcon(icon="help", active_icon="help", size="2em", styles={"color": "White"})
header = pn.FlexBox(
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
header.servable()


# Chat panel
def response_callback(input_message: str, input_user: str, instance: pn.chat.ChatInterface) -> str:
    history = instance.serialize()
    prompt = history.pop()  # The last item of the history is the current prompt.
    response_message = session.provider.generate_response(prompt["content"], history, session.pdf_data)

    return response_message


sct_provider = pn.widgets.Select(options=providers, sizing_mode="stretch_width")
sct_model = pn.widgets.Select(options=session.provider.list_available_models(), sizing_mode="stretch_width")
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
chat_panel = pn.Column(pn.Row(sct_provider, sct_model), chat_interface)

# Control panel
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
control_panel = pn.Column(
    btn_select_pdf,
    pn.Spacer(height=10),
    btn_paper_summary,
    btn_problem_statement,
    btn_methodology_breakdown,
    btn_key_findings,
    width=50,
)

# PDF Panel
pdf_panel = pn.pane.PDF(sizing_mode="stretch_both")

# Main layout
main_layout = pn.Row(
    chat_panel,
    control_panel,
    pdf_panel,
    styles={"height": "calc(100vh - 60px)"},
)
main_layout.servable()

# Introduction to user
prompt = UserPrompt(
    "Give a short introduction of yourself to the user, explaining how you can assist them."
    "Make it clear - in a humorous way - that you're just a highly sophisticated next-token predictor."
)
response = session.provider.generate_response(prompt.content, chat_interface.serialize(), None)
message = pn.chat.ChatMessage(response, user="PaperPal", avatar="🤝", show_reaction_icons=False)
chat_interface.send(message, respond=False)


# Action functions
def swap_panels(event) -> None:
    main_layout.objects = [main_layout[2], main_layout[1], main_layout[0]]


def select_file(event) -> None:
    root = Tk()
    root.withdraw()
    root.call("wm", "attributes", ".", "-topmost", True)
    file_path = Path(filedialog.askopenfilename())
    session.pdf_data = file_path.read_bytes()
    session.pdf_path = file_path
    chat_interface.clear()

    if file_path.suffix == ".pdf":
        for i, obj in enumerate(main_layout):
            if isinstance(obj, pn.pane.PDF):
                main_layout[i] = pn.pane.PDF(file_path, embed=True, sizing_mode="stretch_both")  # type: ignore


def update_sct_provider(event) -> None:
    sct_model.options = session.provider.list_available_models()


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
sct_provider.param.watch(session.update_provider, "value")
sct_provider.param.watch(update_sct_provider, "value")
sct_model.param.watch(session.update_model, "value")
