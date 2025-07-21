import sys
from llama_parser import parse_pdf_with_llama

# Change this to any sample PDF in InputData/
SAMPLE_PDF = "InputData/Tomaten 11-07-2025 _ P. Solleveld Export BV.pdf"

def main():
    result = parse_pdf_with_llama(SAMPLE_PDF)
    for page in result.pages:
        print(page.text)  # or page.md, or page.structuredData

if __name__ == "__main__":
    main() 