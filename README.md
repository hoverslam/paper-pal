# PaperPal :handshake:

> **PaperPal** is an LLM-powered tool that helps researchers and students better understand academic papers through intelligent summaries, explanations, and contextual insights. Users can highlight text for instant clarification, ask questions about complex concepts, and extract concise takeaways from dense research articles. This streamlined approach enhances comprehension of academic literature.

<div align="center">
    <img src="./assets/example.gif" alt="Results from the Procgen paper"/>
</div>



## Features

:sparkles: **Summarization:** Provide concise summaries of sections or the entire paper, helping users grasp key points quickly.

:mag_right: **Explanation:** Clarify complex terms, theories, or concepts by breaking them down into simpler language.

:warning: **Problem Statement Extraction:** Highlight and explain the research problem the paper addresses, providing context on why the study was conducted.

:gear: **Methodology Breakdown:** Extract and simplify the research methods used in the paper, highlighting key steps and experimental design.

:bar_chart: **Key Findings & Results:** Identify and summarize the most important results and conclusions of the study.


## Upcoming Features

:crayon: **Interactive PDF Selection:** Highlight specific sections of a research paper within the PDF viewer to instantly generate summaries, explanations, or ask questions.

:wrench: **LLM Provider Selection:** Choose from different language model providers to generate responses.

:link: **Cross-Referencing:** Generate summaries of referenced papers to provide background context without requiring users to read every citation.


## Installation

1. Clone the repository:

```
git clone https://github.com/hoverslam/paper-pal
```

2. Navigate to the directory:

```
cd paper-pal
```

3. Set up a virtual environment:

```bash
python -m venv .venv
```

4. Install the dependencies:

```
pip install -r requirements.txt
```

## Usage

1. Create an .`env` file in the root directory and add your API keys in the following format:

```
GEMINI_API_KEY="<your API key here>"
```

2. Launch the web-based application by running the following command in the terminal:

```
panel serve app.py
```

3.  Open your browser and go to `http://localhost:5006/app`.


## Contribution

Have ideas to improve PaperPal? Contributions are welcome! Fork the repo, suggest features, or submit a PR.


## License

The code in this project is licensed under the [MIT License](LICENSE.txt).