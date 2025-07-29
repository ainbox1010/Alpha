import re
from bs4 import BeautifulSoup
import html

def detect_html_tables(text):
    """Detect if text contains HTML tables"""
    # Look for common HTML table patterns
    html_table_patterns = [
        r'<table[^>]*>.*?</table>',
        r'<tr[^>]*>.*?</tr>',
        r'<td[^>]*>.*?</td>',
        r'<th[^>]*>.*?</th>'
    ]
    
    for pattern in html_table_patterns:
        if re.search(pattern, text, re.DOTALL | re.IGNORECASE):
            return True
    return False

def html_table_to_markdown(html_content):
    """Convert HTML table to markdown table format"""
    try:
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all tables
        tables = soup.find_all('table')
        markdown_tables = []
        
        for table in tables:
            markdown_table = []
            
            # Process each row
            rows = table.find_all('tr')
            for i, row in enumerate(rows):
                # Get all cells (th and td)
                cells = row.find_all(['th', 'td'])
                
                if not cells:
                    continue
                
                # Convert cells to markdown format
                row_content = []
                for cell in cells:
                    # Get cell text and clean it
                    cell_text = cell.get_text(strip=True)
                    # Handle empty cells
                    if not cell_text:
                        cell_text = ""
                    row_content.append(cell_text)
                
                # Join cells with | separator
                markdown_row = "| " + " | ".join(row_content) + " |"
                markdown_table.append(markdown_row)
                
                # Add separator row after header (first row)
                if i == 0:
                    separator = "| " + " | ".join(["---"] * len(cells)) + " |"
                    markdown_table.append(separator)
            
            if markdown_table:
                markdown_tables.append("\n".join(markdown_table))
        
        return markdown_tables
        
    except Exception as e:
        print(f"Error converting HTML table: {e}")
        return []

def convert_llamaparse_output(input_text):
    """Convert LlamaParse output to consistent markdown format"""
    lines = input_text.split('\n')
    converted_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this line starts an HTML table
        if line.strip().startswith('<table'):
            # Collect all HTML table content
            html_content = []
            while i < len(lines) and not lines[i].strip().startswith('</table>'):
                html_content.append(lines[i])
                i += 1
            if i < len(lines):
                html_content.append(lines[i])  # Add closing </table>
            
            html_text = '\n'.join(html_content)
            
            # Convert HTML table to markdown
            markdown_tables = html_table_to_markdown(html_text)
            
            # Add converted markdown tables
            for table in markdown_tables:
                converted_lines.append(table)
                converted_lines.append("")  # Add empty line after table
            
        else:
            # Keep non-table content as is
            converted_lines.append(line)
        
        i += 1
    
    return '\n'.join(converted_lines)

def test_conversion():
    """Test the HTML to markdown conversion"""
    # Sample HTML table (similar to what LlamaParse might output)
    sample_html = """
Some text before the table.

<table>
  <thead>
    <tr>
      <th>Product</th>
      <th>Origin</th>
      <th>Content</th>
      <th>Pack</th>
      <th>Box p/p</th>
      <th>Size & Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Star Ruby</td>
      <td>RSA</td>
      <td>15 kg</td>
      <td>OT/Crt</td>
      <td>65</td>
      <td>14,50</td>
    </tr>
    <tr>
      <td>White</td>
      <td>RSA</td>
      <td>15 kg</td>
      <td>OT/Crt</td>
      <td>65</td>
      <td></td>
    </tr>
  </tbody>
</table>

Some text after the table.
"""
    
    print("Original HTML:")
    print(sample_html)
    print("\n" + "="*50 + "\n")
    
    print("Converted to Markdown:")
    converted = convert_llamaparse_output(sample_html)
    print(converted)

if __name__ == "__main__":
    test_conversion() 