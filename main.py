from paper_pal.providers import GoogleGemini
from paper_pal.prompts import KeyFindingsResultsPrompt
from paper_pal.chat import History

import configparser


config = configparser.ConfigParser()
config.read("configs/api_keys.ini")
api_key = config.get("api_keys", "GEMINI_API_KEY", fallback="")

llm = GoogleGemini(api_key)
llm.read_pdf("C:/Users/Christopher/Downloads/1809.05700v1.pdf")

prompt = KeyFindingsResultsPrompt()
response = llm.generate_response(prompt, History())
print(response)
