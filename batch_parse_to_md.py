import os
from llama_parser import parse_pdf_with_llama

INPUT_DIR = "InputData"
OUTPUT_DIR = "OutputData"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

for filename in os.listdir(INPUT_DIR):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(INPUT_DIR, filename)
        print(f"Parsing: {pdf_path}")
        try:
            result = parse_pdf_with_llama(pdf_path)
            # Combine markdown from all pages
            md_content = "\n\n".join([page.md for page in result.pages if hasattr(page, 'md') and page.md])
            # Output filename
            base_name = os.path.splitext(filename)[0]
            md_filename = base_name + ".md"
            md_path = os.path.join(OUTPUT_DIR, md_filename)
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            print(f"Saved markdown to: {md_path}")
        except Exception as e:
            print(f"Failed to parse {pdf_path}: {e}") 