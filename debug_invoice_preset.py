import os
from llama_parser import parse_pdf_with_llama
from llama_cloud_services import LlamaParse
from dotenv import load_dotenv

load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")

TEST_PDF = "InputData/Exportlijst ORANGE DLS 11-07-25.pdf"

def test_different_presets():
    print("Testing different LlamaParse configurations...")
    print("=" * 60)
    
    working_modes = []
    
    # Test 1: Default (Balanced) mode
    print("\n1. Testing DEFAULT (Balanced) mode:")
    try:
        parser_default = LlamaParse(
            api_key=LLAMA_API_KEY,
            base_url="https://api.cloud.eu.llamaindex.ai",
            verbose=True,
            language="en",
        )
        result = parser_default.parse(TEST_PDF)
        print("✅ DEFAULT mode works!")
        working_modes.append("default")
    except Exception as e:
        print(f"❌ DEFAULT mode failed: {e}")
    
    # Test 2: Premium mode
    print("\n2. Testing PREMIUM mode:")
    try:
        parser_premium = LlamaParse(
            api_key=LLAMA_API_KEY,
            base_url="https://api.cloud.eu.llamaindex.ai",
            verbose=True,
            language="en",
            premium_mode=True,
        )
        result = parser_premium.parse(TEST_PDF)
        print("✅ PREMIUM mode works!")
        working_modes.append("premium")
    except Exception as e:
        print(f"❌ PREMIUM mode failed: {e}")
    
    # Test 3: Invoice preset
    print("\n3. Testing INVOICE preset:")
    try:
        parser_invoice = LlamaParse(
            api_key=LLAMA_API_KEY,
            base_url="https://api.cloud.eu.llamaindex.ai",
            verbose=True,
            language="en",
            preset="invoice",
        )
        result = parser_invoice.parse(TEST_PDF)
        print("✅ INVOICE preset works!")
        working_modes.append("invoice")
    except Exception as e:
        print(f"❌ INVOICE preset failed: {e}")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {str(e)}")
    
    # Test 4: Fast mode
    print("\n4. Testing FAST mode:")
    try:
        parser_fast = LlamaParse(
            api_key=LLAMA_API_KEY,
            base_url="https://api.cloud.eu.llamaindex.ai",
            verbose=True,
            language="en",
            fast_mode=True,
        )
        result = parser_fast.parse(TEST_PDF)
        print("✅ FAST mode works!")
        working_modes.append("fast")
    except Exception as e:
        print(f"❌ FAST mode failed: {e}")
    
    return working_modes

def main():
    print(f"Debugging LlamaParse with file: {TEST_PDF}")
    print(f"File exists: {os.path.exists(TEST_PDF)}")
    print(f"File size: {os.path.getsize(TEST_PDF)} bytes")
    
    working_modes = test_different_presets()
    
    if working_modes:
        print(f"\n🎉 Working modes found: {', '.join(working_modes)}")
        if "invoice" in working_modes:
            print("✅ INVOICE preset works! Use this for best table structure.")
        elif "premium" in working_modes:
            print("✅ PREMIUM mode works! Use this as alternative for table structure.")
        else:
            print("⚠️  Only basic modes work. Invoice preset failed.")
    else:
        print("\n❌ All modes failed. There might be an issue with:")
        print("- The PDF file itself")
        print("- API key or permissions")
        print("- Network connectivity")
        print("- LlamaParse service status")

if __name__ == "__main__":
    main() 