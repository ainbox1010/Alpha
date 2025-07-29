import os
from html_to_markdown_converter import convert_llamaparse_output

def convert_llamaparse_file(input_file, output_file):
    """Convert a LlamaParse output file to consistent markdown format"""
    
    print(f"Converting {input_file} to consistent markdown format...")
    
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert HTML tables to markdown
        converted_content = convert_llamaparse_output(content)
        
        # Write the converted content
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(converted_content)
        
        print(f"✅ Successfully converted to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error converting file: {e}")

def main():
    # Convert the test file we created earlier
    input_file = "OutputData/test_single_file_output.md"
    output_file = "OutputData/test_single_file_converted.md"
    
    if os.path.exists(input_file):
        convert_llamaparse_file(input_file, output_file)
        
        print(f"\n📋 Summary:")
        print(f"Original file: {input_file}")
        print(f"Converted file: {output_file}")
        print(f"Check the converted file to see consistent markdown tables!")
        
    else:
        print(f"❌ Input file not found: {input_file}")
        print("Please run test_single_file.py first to generate the input file.")

if __name__ == "__main__":
    main() 