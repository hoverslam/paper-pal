from paper_pal.providers import load_provider
from paper_pal.chat import History, KeyFindingsResultsPrompt


llm = load_provider("Google Gemini")
llm.read_pdf("C:/Users/Christopher/Downloads/1809.05700v1.pdf")

prompt = KeyFindingsResultsPrompt()
response = llm.generate_response(prompt, History())
print(response)
