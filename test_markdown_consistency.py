import os
from llama_cloud_services import LlamaParse
from dotenv import load_dotenv

load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")

TEST_PDF = "InputData/Exportlijst ORANGE DLS 11-07-25.pdf"

def test_markdown_consistency():
    print("Testing LlamaParse for consistent markdown table output...")
    print("=" * 60)
    
    # Test 1: Premium mode with markdown result type
    print("\n1. Testing PREMIUM mode with markdown result type:")
    try:
        parser_premium_md = LlamaParse(
            api_key=LLAMA_API_KEY,
            base_url="https://api.cloud.eu.llamaindex.ai",
            verbose=True,
            language="en",
            premium_mode=True,
            result_type="markdown",  # Force markdown output
        )
        result = parser_premium_md.parse(TEST_PDF)
        
        # Get markdown documents
        md_docs = result.get_markdown_documents(split_by_page=True)
        
        output_file = "OutputData/test_premium_markdown.md"
        os.makedirs("OutputData", exist_ok=True)
        
        with open(output_file, "w", encoding="utf-8") as f:
            for i, doc in enumerate(md_docs, 1):
                f.write(f"# Page {i}\n\n")
                f.write(doc.text)
                f.write("\n\n---\n\n")
        
        print(f"✅ PREMIUM with markdown result type works!")
        print(f"Saved to: {output_file}")
        return "premium_markdown"
        
    except Exception as e:
        print(f"❌ PREMIUM with markdown failed: {e}")
    
    # Test 2: Default mode with markdown result type
    print("\n2. Testing DEFAULT mode with markdown result type:")
    try:
        parser_default_md = LlamaParse(
            api_key=LLAMA_API_KEY,
            base_url="https://api.cloud.eu.llamaindex.ai",
            verbose=True,
            language="en",
            result_type="markdown",  # Force markdown output
        )
        result = parser_default_md.parse(TEST_PDF)
        
        # Get markdown documents
        md_docs = result.get_markdown_documents(split_by_page=True)
        
        output_file = "OutputData/test_default_markdown.md"
        os.makedirs("OutputData", exist_ok=True)
        
        with open(output_file, "w", encoding="utf-8") as f:
            for i, doc in enumerate(md_docs, 1):
                f.write(f"# Page {i}\n\n")
                f.write(doc.text)
                f.write("\n\n---\n\n")
        
        print(f"✅ DEFAULT with markdown result type works!")
        print(f"Saved to: {output_file}")
        return "default_markdown"
        
    except Exception as e:
        print(f"❌ DEFAULT with markdown failed: {e}")
    
    return None

def main():
    print(f"Testing markdown consistency with file: {TEST_PDF}")
    
    working_mode = test_markdown_consistency()
    
    if working_mode:
        print(f"\n🎉 Found working markdown mode: {working_mode}")
        print("Check the output files to see if tables are in consistent markdown format")
    else:
        print("\n❌ No markdown modes worked")

if __name__ == "__main__":
    main() 