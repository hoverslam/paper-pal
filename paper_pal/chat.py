from paper_pal.interfaces import Prompt


class UserPrompt(Prompt):
    """A class representing a user input prompt."""

    def __init__(self, user_content: str) -> None:
        """Initializes the UserPrompt with the user's content.

        Args:
            user_content (str): The content to be used in the user prompt.
        """
        self._user_content = user_content

    @property
    def role(self) -> str:
        """Returns the role of the prompt, which is 'User'."""
        return "User"

    @property
    def content(self) -> str:
        """Returns the content provided by the user."""
        return self._user_content


class PaperSummaryPrompt(Prompt):
    """A class representing a paper summary prompt."""

    @property
    def role(self) -> str:
        """Returns the role of the prompt, which is 'PaperSummary'."""
        return "PaperSummary"

    @property
    def content(self) -> str:
        """Provides the content for summarizing an academic paper.

        Returns:
            str: A prompt for summarizing the key findings and arguments of the paper.
        """
        return (
            "Provide a concise summary of the entire academic paper attached. "
            "Focus on the key findings, arguments, and conclusions of the study. "
            "The summary should be easily understandable to someone with a general "
            "understanding of the field."
        )


class SummaryPrompt:
    """A class representing a prompt to summarize a selected portion of an academic paper."""

    def __init__(self, selection: str) -> None:
        """Initializes the SummaryPrompt with the selected portion of the paper.

        Args:
            selection (str): The selected text from the academic paper to be summarized.
        """
        self._selection = selection

    @property
    def role(self) -> str:
        """Returns the role of the prompt, which is 'Summary'."""
        return "Summary"

    @property
    def content(self) -> str:
        """Provides the content for summarizing a selected portion of an academic paper.

        Returns:
            str: A prompt asking for a summary of the selected text.
        """
        return (
            "Provide a concise summary of the following selected text from "
            "the attached academic paper:\n\n"
            f"{self._selection}\n\n"
            "(Note: This text may be a formal section of the paper, or simply a "
            "selected portion of the text.)\n\n"
            "Ensure the summary captures the main points and arguments presented in "
            "the selected text. The summary should be easily understandable, "
            "concise, and accurately reflect the meaning of the original text."
        )


class ExplanationPrompt:
    """A class representing a prompt to explain a specific term or phrase selected from an academic paper."""

    def __init__(self, selection: str) -> None:
        """Initializes the ExplanationPrompt with the selected term or phrase.

        Args:
            selection (str): The term or phrase to be explained.
        """
        self._selection = selection

    @property
    def role(self) -> str:
        """Returns the role of the prompt, which is 'Explanation'."""
        return "Explanation"

    @property
    def content(self) -> str:
        """Provides the content for explaining a selected term or phrase.

        Returns:
            str: A prompt asking for an explanation of the selected term or phrase.
        """
        return (
            f'A user has selected the term or phrase: "{self._selection}" from an academic paper because they want to '
            f'understand what it means. \n\n Provide a clear and concise explanation of what "{self._selection}" '
            "generally refers to. Break down the concept into simpler language, avoiding jargon where possible. "
            "Your explanation should be a general definition of the term, *independent* of the specific paper it was "
            "found in. The explanation should be understandable to someone with a general understanding of related "
            "concepts."
        )


class ProblemStatementPrompt:
    """A class representing a prompt to extract the problem statement from an academic paper."""

    @property
    def role(self) -> str:
        """Returns the role of the prompt, which is 'ProblemStatementExtraction'."""
        return "ProblemStatementExtraction"

    @property
    def content(self) -> str:
        """Provides the content for extracting the problem statement from the paper.

        Returns:
            str: A prompt for identifying and explaining the research problem.
        """
        return (
            "Identify and explain the research problem that the attached "
            "academic paper addresses. Provide context on why the study was "
            "conducted and the significance of the problem being investigated. "
            "Your explanation should be easily understandable."
        )


class MethodologyPrompt:
    """A class representing a prompt to extract and simplify the methodology of an academic paper."""

    @property
    def role(self) -> str:
        """Returns the role of the prompt, which is 'MethodologyBreakdown'."""
        return "MethodologyBreakdown"

    @property
    def content(self) -> str:
        """Provides the content for extracting and simplifying the research methodology.

        Returns:
            str: A prompt for explaining the methods used in the academic paper.
        """
        return (
            "Extract and simplify the research methods used in the attached "
            "academic paper. Highlight the key steps, experimental design, and "
            "data analysis techniques employed. The breakdown should be clear, "
            "concise, and easily understandable to someone with a general "
            "understanding of research methodologies."
        )


class KeyFindingsPrompt:
    """A class representing a prompt to summarize the key findings of an academic paper."""

    @property
    def role(self) -> str:
        """Returns the role of the prompt, which is 'KeyFindingsResults'."""
        return "KeyFindingsResults"

    @property
    def content(self) -> str:
        """Provides the content for summarizing the key findings of the paper.

        Returns:
            str: A prompt asking for a summary of the key findings and conclusions.
        """
        return (
            "Identify and summarize the most important results and conclusions "
            "of the attached academic paper. Focus on the key findings and their "
            "implications. The summary should be clear, concise, and easily "
            "understandable, highlighting the main takeaways from the study."
        )


class QuestionPrompt:
    """A class representing a prompt to answer a specific question based on a selected section of an academic paper."""

    def __init__(self, selection: str, question: str) -> None:
        """Initializes the QuestionPrompt with the selected section and the question.

        Args:
            selection (str): The selected section of the paper.
            question (str): The question to be answered based on the selection.
        """
        self._selection = selection
        self._question = question

    @property
    def role(self) -> str:
        """Returns the role of the prompt, which is 'SectionQuestion'."""
        return "SectionQuestion"

    @property
    def content(self) -> str:
        """Provides the content for answering a question based on a selected section of the paper.

        Returns:
            str: A prompt asking for an answer to the question based solely on the selected section.
        """
        return (
            "Answer the following question based *solely* on the information "
            "provided in the following section from the attached academic paper:\n\n"
            f"**Section:**\n{self._selection}\n\n"
            f"**Question:**\n{self._question}\n\n"
            "If the answer to the question cannot be found directly within the "
            "provided section, please state that the information is not explicitly "
            "mentioned in the section. Do not provide information from outside the "
            "given section."
        )
