import os
from llama_parser import parse_pdf_with_llama

# Test with single file
TEST_PDF = "InputData/Exportlijst ORANGE DLS 11-07-25.pdf"

def main():
    print(f"Testing LlamaParse with premium mode on: {TEST_PDF}")
    print("=" * 60)
    
    try:
        result = parse_pdf_with_llama(TEST_PDF)
        
        print(f"\nSuccessfully parsed PDF!")
        print(f"Number of pages: {len(result.pages)}")
        
        # Display markdown content for each page
        for i, page in enumerate(result.pages, 1):
            print(f"\n--- PAGE {i} ---")
            if hasattr(page, 'md') and page.md:
                print(page.md)
            else:
                print("No markdown content available for this page")
            print("-" * 40)
        
        # Also save to file for easier review
        output_file = "OutputData/test_single_file_output.md"
        os.makedirs("OutputData", exist_ok=True)
        
        md_content = "\n\n".join([page.md for page in result.pages if hasattr(page, 'md') and page.md])
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        print(f"\nFull output saved to: {output_file}")
        
    except Exception as e:
        print(f"Error parsing PDF: {e}")

if __name__ == "__main__":
    main() 