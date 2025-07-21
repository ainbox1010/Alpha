import os
from dotenv import load_dotenv
from llama_cloud_services import LlamaParse

load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")

if not LLAMA_API_KEY:
    raise ValueError("LLAMA_CLOUD_API_KEY not set in .env")

parser = LlamaParse(
    api_key=LLAMA_API_KEY,
    base_url="https://api.cloud.eu.llamaindex.ai",  # <-- protocol included!
    verbose=True,
    language="en",
)

def parse_pdf_with_llama(pdf_path):
    result = parser.parse(pdf_path)
    # You can access result.pages, result.get_text_documents(), etc.
    return result 