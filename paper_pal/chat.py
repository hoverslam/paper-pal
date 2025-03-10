from paper_pal.interfaces import Prompt


class History:
    # TODO
    def __init__(self) -> None:
        pass


class UserPrompt(Prompt):
    def __init__(self, user_content: str = "") -> None:
        self._user_content = user_content

    @property
    def role(self) -> str:
        return "User"

    @property
    def content(self) -> str:
        return self._user_content


class PaperSummaryPrompt(Prompt):
    @property
    def role(self) -> str:
        return "PaperSummary"

    @property
    def content(self) -> str:
        return (
            "Please provide a concise summary of the entire academic paper attached. "
            "Focus on the key findings, arguments, and conclusions of the study. "
            "The summary should be easily understandable to someone with a general "
            "understanding of the field."
        )


class SummaryPrompt:
    def __init__(self, selection: str) -> None:
        self._selection = selection

    @property
    def role(self) -> str:
        return "Summary"

    @property
    def content(self) -> str:
        return (
            "Please provide a concise summary of the following selected text from "
            "the attached academic paper:\n\n"
            f"{self._selection}\n\n"
            "(Note: This text may be a formal section of the paper, or simply a "
            "selected portion of the text.)\n\n"
            "Ensure the summary captures the main points and arguments presented in "
            "the selected text. The summary should be easily understandable, "
            "concise, and accurately reflect the meaning of the original text."
        )


class ExplanationPrompt:
    def __init__(self, selection: str) -> None:
        self._selection = selection

    @property
    def role(self) -> str:
        return "Explanation"

    @property
    def content(self) -> str:
        return (
            f'A user has selected the term or phrase: "{self._selection}" from an academic paper because they want to '
            f'understand what it means. \n\n Provide a clear and concise explanation of what "{self._selection}" '
            "generally refers to. Break down the concept into simpler language, avoiding jargon where possible. "
            "Your explanation should be a general definition of the term, *independent* of the specific paper it was "
            "found in. The explanation should be understandable to someone with a general understanding of related "
            "concepts."
        )


class ProblemStatementExtractionPrompt:
    @property
    def role(self) -> str:
        return "ProblemStatementExtraction"

    @property
    def content(self) -> str:
        return (
            "Please identify and explain the research problem that the attached "
            "academic paper addresses. Provide context on why the study was "
            "conducted and the significance of the problem being investigated. "
            "Your explanation should be easily understandable."
        )


class MethodologyBreakdownPrompt:
    @property
    def role(self) -> str:
        return "MethodologyBreakdown"

    @property
    def content(self) -> str:
        return (
            "Please extract and simplify the research methods used in the attached "
            "academic paper. Highlight the key steps, experimental design, and "
            "data analysis techniques employed. The breakdown should be clear, "
            "concise, and easily understandable to someone with a general "
            "understanding of research methodologies."
        )


class KeyFindingsResultsPrompt:
    @property
    def role(self) -> str:
        return "KeyFindingsResults"

    @property
    def content(self) -> str:
        return (
            "Please identify and summarize the most important results and conclusions "
            "of the attached academic paper. Focus on the key findings and their "
            "implications. The summary should be clear, concise, and easily "
            "understandable, highlighting the main takeaways from the study."
        )


class QuestionPrompt:
    def __init__(self, selection: str, question: str) -> None:
        self._selection = selection
        self._question = question

    @property
    def role(self) -> str:
        return "SectionQuestion"

    @property
    def content(self) -> str:
        return (
            "Please answer the following question based *solely* on the information "
            "provided in the following section from the attached academic paper:\n\n"
            f"**Section:**\n{self._selection}\n\n"
            f"**Question:**\n{self._question}\n\n"
            "If the answer to the question cannot be found directly within the "
            "provided section, please state that the information is not explicitly "
            "mentioned in the section. Do not provide information from outside the "
            "given section."
        )
