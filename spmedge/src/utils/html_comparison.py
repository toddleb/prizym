"""
HTML to Excel Comparison Tool
-----------------------------
Extract data from HTML to validate Excel output matches the source HTML.
"""

from bs4 import BeautifulSoup
import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


def extract_tables_from_html(html_file):
    """Extract tables from HTML file and return as DataFrames."""
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = {}
    
    # Extract Plans Summary table
    summary_section = soup.find('div', class_='card')
    if summary_section:
        tables['Plans Summary'] = pd.read_html(str(summary_section.find('table')))[0]
    
    # Extract Compensation Components table
    comp_section = soup.find('div', id='Compensation')
    if comp_section:
        tables['Compensation Components'] = pd.read_html(str(comp_section.find('table')))[0]
    
    # Extract Special Provisions table
    provisions_section = soup.find('div', id='Provisions')
    if provisions_section:
        tables['Special Provisions'] = pd.read_html(str(provisions_section.find('table')))[0]
    
    # Extract Terms & Conditions (this is more complex as it's not a simple table)
    terms_section = soup.find('div', id='Terms')
    if terms_section:
        # We'll just store the raw HTML for now
        tables['Terms & Conditions'] = str(terms_section)
    
    return tables


def compare_with_excel(html_tables, excel_file):
    """Compare HTML tables with Excel file data."""
    # Read Excel file
    excel_dfs = {}
    xl = pd.ExcelFile(excel_file)
    for sheet_name in xl.sheet_names:
        excel_dfs[sheet_name] = pd.read_excel(excel_file, sheet_name=sheet_name)
    
    # Compare and report differences
    comparison_results = {}
    
    for table_name, html_df in html_tables.items():
        if table_name == 'Terms & Conditions':
            # Skip complex comparison for terms
            comparison_results[table_name] = 'Manual inspection required'
            continue
            
        if table_name in excel_dfs:
            # Basic shape comparison
            html_shape = html_df.shape
            excel_shape = excel_dfs[table_name].shape
            
            # Check if columns match
            html_cols = set(html_df.columns)
            excel_cols = set(excel_dfs[table_name].columns)
            missing_cols = html_cols - excel_cols
            extra_cols = excel_cols - html_cols
            
            # Store results
            comparison_results[table_name] = {
                'html_shape': html_shape,
                'excel_shape': excel_shape,
                'shape_match': html_shape == excel_shape,
                'missing_columns': list(missing_cols),
                'extra_columns': list(extra_cols),
                'html_sample': html_df.head(2).to_dict(),
                'excel_sample': excel_dfs[table_name].head(2).to_dict()
            }
        else:
            comparison_results[table_name] = 'Not found in Excel'
    
    return comparison_results


def generate_comparison_report(comparison_results, output_file='comparison_report.html'):
    """Generate an HTML report of the comparison results."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>HTML vs Excel Comparison Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
            h1, h2, h3 { color: #0056b3; }
            .section { margin-bottom: 30px; }
            .pass { color: green; font-weight: bold; }
            .fail { color: red; font-weight: bold; }
            .warning { color: orange; font-weight: bold; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 15px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .code { font-family: monospace; background-color: #f5f5f5; padding: 10px; border-radius: 4px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <h1>HTML to Excel Comparison Report</h1>
    """
    
    for table_name, result in comparison_results.items():
        html += f'<div class="section"><h2>{table_name}</h2>'
        
        if isinstance(result, str):
            html += f'<p class="warning">{result}</p>'
        else:
            # Shape comparison
            shape_class = 'pass' if result['shape_match'] else 'fail'
            html += f'<p>HTML table shape: {result["html_shape"]} | Excel table shape: {result["excel_shape"]} - <span class="{shape_class}">{shape_class.upper()}</span></p>'
            
            # Columns comparison
            if result['missing_columns'] or result['extra_columns']:
                html += '<p class="fail">Column mismatch:</p>'
                if result['missing_columns']:
                    html += f'<p>Missing columns in Excel: {", ".join(result["missing_columns"])}</p>'
                if result['extra_columns']:
                    html += f'<p>Extra columns in Excel: {", ".join(result["extra_columns"])}</p>'
            else:
                html += '<p class="pass">All columns match</p>'
            
            # Sample data
            html += '<h3>Sample Data Comparison</h3>'
            html += '<h4>HTML Sample:</h4>'
            html += f'<div class="code">{str(result["html_sample"])}</div>'
            html += '<h4>Excel Sample:</h4>'
            html += f'<div class="code">{str(result["excel_sample"])}</div>'
        
        html += '</div>'
    
    html += """
    </body>
    </html>
    """
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_file


def html_to_excel_compare(html_file, excel_file, output_report='comparison_report.html'):
    """Main function to compare HTML and Excel data."""
    try:
        print(f"Extracting data from HTML: {html_file}")
        html_tables = extract_tables_from_html(html_file)
        
        print(f"Comparing with Excel: {excel_file}")
        comparison = compare_with_excel(html_tables, excel_file)
        
        print(f"Generating comparison report: {output_report}")
        report_file = generate_comparison_report(comparison, output_report)
        
        print(f"Comparison complete! Report saved to: {report_file}")
        return True
    
    except Exception as e:
        print(f"Error during comparison: {str(e)}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Compare HTML and Excel data")
    parser.add_argument("html_file", help="Path to HTML file")
    parser.add_argument("excel_file", help="Path to Excel file")
    parser.add_argument("-o", "--output", default="reports/comparison_report.html", 
                        help="Output comparison report file (default: reports/comparison_report.html)")
    
    args = parser.parse_args()
    
    # Create reports directory if it doesn't exist
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    html_to_excel_compare(args.html_file, args.excel_file, args.output)