"""
Compensation Plan Analyzer
This utility processes compensation plan JSON files from a specified directory
and generates a readable HTML report with visualizations.
"""

import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
import re
import numpy as np


def load_json_files(directory):
    """Load all JSON files from the specified directory that contain comp plan data"""
    plans = []
    
    # Verify directory exists
    if not os.path.isdir(directory):
        print(f"❌ Directory not found: {directory}")
        return plans
    
    # Get all JSON files in the directory
    file_paths = [
        os.path.join(directory, f) 
        for f in os.listdir(directory) 
        if f.endswith('.json') and 'FY' in f
    ]
    
    if not file_paths:
        print(f"⚠️ No JSON files with 'FY' in the name found in {directory}")
        return plans
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as f:
                plan_data = json.load(f)
                
                # Verify this is a comp plan by checking for key fields
                if 'plan_info' in plan_data and 'compensation_components' in plan_data:
                    plans.append(plan_data)
                    print(f"✅ Loaded: {os.path.basename(file_path)}")
                else:
                    print(f"⚠️ Skipped (not a comp plan): {os.path.basename(file_path)}")
        except Exception as e:
            print(f"❌ Error loading {file_path}: {str(e)}")
    
    return plans


def create_summary_table(plans):
    """Create a summary table with key information from all plans"""
    summary_data = []
    
    for plan in plans:
        plan_info = plan.get('plan_info', {})
        effective = plan.get('effective_dates', {})
        
        summary_data.append({
            'Role': plan_info.get('role', 'N/A'),
            'Business Unit': plan_info.get('business_unit', 'N/A'),
            'Plan ID': plan_info.get('plan_id', 'N/A'),
            'Plan Year': plan_info.get('plan_year', 'N/A'),
            'Start Date': effective.get('start_date', 'N/A'),
            'End Date': effective.get('end_date', 'N/A'),
            'Region': plan_info.get('region', 'N/A')
        })
    
    return pd.DataFrame(summary_data)


def create_compensation_table(plans):
    """Create a detailed table of all compensation components across plans"""
    comp_data = []
    
    for plan in plans:
        plan_info = plan.get('plan_info', {})
        role = plan_info.get('role', 'Unknown')
        
        for comp in plan.get('compensation_components', []):
            comp_data.append({
                'Role': role,
                'Component Name': comp.get('name', 'N/A'),
                'Type': comp.get('type', 'N/A'),
                'Category': comp.get('category', 'N/A'),
                'Frequency': comp.get('frequency', 'N/A'),
                'Target Amount': comp.get('target_amount', 'N/A'),
                'Structure': comp.get('structure', 'N/A')
            })
    
    return pd.DataFrame(comp_data)


def extract_numeric_value(value_str):
    """Extract numeric value from strings like '$40,000' or '$20,000 - $50,000'"""
    if not isinstance(value_str, str):
        return None
    
    # Check for range format
    if '-' in value_str:
        parts = value_str.split('-')
        if len(parts) == 2:
            # Get the average of the range
            try:
                val1 = float(re.sub(r'[^\d.]', '', parts[0].strip()))
                val2 = float(re.sub(r'[^\d.]', '', parts[1].strip()))
                return (val1 + val2) / 2
            except:
                return None
    
    # Single value format
    try:
        return float(re.sub(r'[^\d.]', '', value_str))
    except:
        return None


def generate_visualizations(plans, output_dir):
    """Generate visualizations for comp plans and save to specified directory"""
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Extract compensation components for visualization
    comp_data = []
    
    for plan in plans:
        plan_info = plan.get('plan_info', {})
        role = plan_info.get('role', 'Unknown')
        business_unit = plan_info.get('business_unit', 'Unknown')
        
        for comp in plan.get('compensation_components', []):
            target_amount = comp.get('target_amount', 'N/A')
            numeric_value = extract_numeric_value(target_amount)
            
            comp_data.append({
                'Role': role,
                'Business Unit': business_unit,
                'Component Name': comp.get('name', 'N/A'),
                'Type': comp.get('type', 'N/A'), 
                'Category': comp.get('category', 'N/A'),
                'Frequency': comp.get('frequency', 'N/A'),
                'Target Amount': target_amount,
                'Numeric Value': numeric_value
            })
    
    comp_df = pd.DataFrame(comp_data)
    
    # Save paths for each visualization
    viz_paths = {}
    
    # Visualization 1: Component Types by Role
    plt.figure(figsize=(10, 6))
    role_type_counts = comp_df.groupby(['Role', 'Type']).size().unstack(fill_value=0)
    role_type_counts.plot(kind='bar', stacked=True)
    plt.title('Compensation Component Types by Role')
    plt.xlabel('Role')
    plt.ylabel('Count')
    plt.tight_layout()
    
    viz_path = os.path.join(output_dir, 'comp_types_by_role.png')
    plt.savefig(viz_path)
    viz_paths['comp_types'] = viz_path
    plt.close()
    
    # Visualization 2: Target Amount by Component (where numeric values are available)
    plt.figure(figsize=(12, 6))
    comp_values = comp_df[comp_df['Numeric Value'].notna()]
    if not comp_values.empty:
        comp_values.plot(kind='bar', x='Component Name', y='Numeric Value', color='skyblue')
        plt.title('Target Amount by Compensation Component')
        plt.xlabel('Component')
        plt.ylabel('Target Amount ($)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        viz_path = os.path.join(output_dir, 'target_amount_by_component.png')
        plt.savefig(viz_path)
        viz_paths['target_amounts'] = viz_path
    plt.close()
    
    # Visualization 3: Frequency Distribution
    plt.figure(figsize=(8, 8))
    freq_counts = comp_df['Frequency'].value_counts()
    plt.pie(freq_counts, labels=freq_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('Compensation Component Payment Frequency')
    plt.axis('equal')
    plt.tight_layout()
    
    viz_path = os.path.join(output_dir, 'payment_frequency.png')
    plt.savefig(viz_path)
    viz_paths['payment_frequency'] = viz_path
    plt.close()
    
    # Visualization 4: Business Unit Distribution
    plt.figure(figsize=(10, 6))
    bu_counts = comp_df['Business Unit'].value_counts()
    bu_counts.plot(kind='bar', color='lightgreen')
    plt.title('Compensation Components by Business Unit')
    plt.xlabel('Business Unit')
    plt.ylabel('Number of Components')
    plt.tight_layout()
    
    viz_path = os.path.join(output_dir, 'components_by_bu.png')
    plt.savefig(viz_path)
    viz_paths['business_units'] = viz_path
    plt.close()
    
    return viz_paths


def generate_html_report(plans, visualizations, output_file):
    """Generate an HTML report with all tables and visualizations"""
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Create tables
    summary_df = create_summary_table(plans)
    comp_df = create_compensation_table(plans)
    
    # Get special provisions
    provisions_data = []
    for plan in plans:
        plan_info = plan.get('plan_info', {})
        role = plan_info.get('role', 'Unknown')
        
        for provision in plan.get('special_provisions', []):
            provisions_data.append({
                'Role': role,
                'Provision Name': provision.get('name', 'N/A'),
                'Description': provision.get('description', 'N/A'),
                'Conditions': provision.get('conditions', 'N/A'),
                'SPM Component': provision.get('spm_mapping', {}).get('spm_component', 'N/A')
            })
    
    provisions_df = pd.DataFrame(provisions_data) if provisions_data else pd.DataFrame()
    
    # Start building HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Compensation Plans Analysis</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 20px;
                color: #333;
                background-color: #f8f9fa;
            }}
            h1, h2, h3 {{
                color: #0056b3;
            }}
            .dashboard-header {{
                background: linear-gradient(to right, #0056b3, #00a8e8);
                color: white;
                padding: 20px;
                border-radius: 5px;
                margin-bottom: 20px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .card {{
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 20px;
                background-color: white;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 20px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            .tab {{
                overflow: hidden;
                border: 1px solid #ccc;
                background-color: #f1f1f1;
                border-radius: 5px 5px 0 0;
            }}
            .tab button {{
                background-color: inherit;
                float: left;
                border: none;
                outline: none;
                cursor: pointer;
                padding: 14px 16px;
                transition: 0.3s;
                font-size: 17px;
            }}
            .tab button:hover {{
                background-color: #ddd;
            }}
            .tab button.active {{
                background-color: #0056b3;
                color: white;
            }}
            .tabcontent {{
                display: none;
                padding: 20px;
                border: 1px solid #ccc;
                border-top: none;
                border-radius: 0 0 5px 5px;
                animation: fadeEffect 1s;
                background-color: white;
            }}
            @keyframes fadeEffect {{
                from {{opacity: 0;}}
                to {{opacity: 1;}}
            }}
            .visualization-grid {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
                margin-top: 20px;
            }}
            .viz-card {{
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
                background-color: white;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .viz-card img {{
                width: 100%;
                height: auto;
                border-radius: 3px;
            }}
            @media (max-width: 768px) {{
                .visualization-grid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="dashboard-header">
            <h1>Medtronic Sales Incentive Plans Analysis</h1>
            <p>Generated on {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
        
        <div class="card">
            <h2>Plans Summary</h2>
            {summary_df.to_html(index=False, classes='dataframe')}
        </div>
        
        <div class="tab">
            <button class="tablinks" onclick="openTab(event, 'Compensation')" id="defaultOpen">Compensation Components</button>
            <button class="tablinks" onclick="openTab(event, 'Provisions')">Special Provisions</button>
            <button class="tablinks" onclick="openTab(event, 'Terms')">Terms & Conditions</button>
            <button class="tablinks" onclick="openTab(event, 'Visualizations')">Visualizations</button>
        </div>
        
        <div id="Compensation" class="tabcontent">
            <h2>Compensation Components</h2>
            {comp_df.to_html(index=False, classes='dataframe')}
        </div>
        
        <div id="Provisions" class="tabcontent">
            <h2>Special Provisions</h2>
            {provisions_df.to_html(index=False, classes='dataframe') if not provisions_df.empty else "<p>No special provisions found in the plans.</p>"}
        </div>
        
        <div id="Terms" class="tabcontent">
            <h2>Terms & Conditions</h2>
    """
    
    # Add terms and conditions content
    for plan in plans:
        plan_info = plan.get('plan_info', {})
        role = plan_info.get('role', 'Unknown')
        
        html += f"<h3>{role}</h3>"
        
        terms = plan.get('terms_and_conditions', [])
        if terms:
            html += "<ul>"
            for term in terms:
                html += f"<li><strong>{term.get('component_type', 'Term')}:</strong> {term.get('description', 'N/A')}</li>"
            html += "</ul>"
        else:
            html += "<p>No terms and conditions found for this role.</p>"
    
    # Add visualizations tab
    html += """
        </div>
        
        <div id="Visualizations" class="tabcontent">
            <h2>Compensation Plan Visualizations</h2>
            <div class="visualization-grid">
    """
    
    # Add each visualization if available
    if 'comp_types' in visualizations:
        rel_path = os.path.relpath(visualizations['comp_types'], os.path.dirname(output_file))
        html += f"""
                <div class="viz-card">
                    <h3>Component Types by Role</h3>
                    <img src="{rel_path}" alt="Component Types by Role">
                </div>
        """
    
    if 'target_amounts' in visualizations:
        rel_path = os.path.relpath(visualizations['target_amounts'], os.path.dirname(output_file))
        html += f"""
                <div class="viz-card">
                    <h3>Target Amount by Component</h3>
                    <img src="{rel_path}" alt="Target Amount by Component">
                </div>
        """
    
    if 'payment_frequency' in visualizations:
        rel_path = os.path.relpath(visualizations['payment_frequency'], os.path.dirname(output_file))
        html += f"""
                <div class="viz-card">
                    <h3>Payment Frequency Distribution</h3>
                    <img src="{rel_path}" alt="Payment Frequency">
                </div>
        """
    
    if 'business_units' in visualizations:
        rel_path = os.path.relpath(visualizations['business_units'], os.path.dirname(output_file))
        html += f"""
                <div class="viz-card">
                    <h3>Components by Business Unit</h3>
                    <img src="{rel_path}" alt="Components by Business Unit">
                </div>
        """
    
    # Finish HTML
    html += """
            </div>
        </div>
        
        <script>
        function openTab(evt, tabName) {
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tabcontent");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
            }
            tablinks = document.getElementsByClassName("tablinks");
            for (i = 0; i < tablinks.length; i++) {
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " active";
        }
        
        // Get the element with id="defaultOpen" and click on it
        document.getElementById("defaultOpen").click();
        </script>
    </body>
    </html>
    """
    
    with open(output_file, 'w') as f:
        f.write(html)
    
    return output_file


def analyze_comp_plans(input_dir, output_dir):
    """Main function to process compensation plans and generate report"""
    print(f"🚀 Starting Compensation Plan Analysis from directory: {input_dir}")
    
    # Load plans from the input directory
    plans = load_json_files(input_dir)
    
    if not plans:
        print("❌ No compensation plans found. Please check the input directory.")
        return None
    
    print(f"✅ Found {len(plans)} compensation plans")
    
    # Generate visualizations
    print("📊 Generating visualizations...")
    vis_output_dir = os.path.join(output_dir, 'visualizations')
    visualizations = generate_visualizations(plans, vis_output_dir)
    
    # Generate HTML report
    print("📝 Generating HTML report...")
    report_path = os.path.join(output_dir, 'comp_plans_report.html')
    report_file = generate_html_report(plans, visualizations, report_path)
    
    print(f"✨ Analysis complete! Report generated at: {report_file}")
    
    return {
        "plans_processed": len(plans),
        "visualizations": visualizations,
        "report_file": report_file
    }


if __name__ == "__main__":
    # When run directly, use defaults
    analyze_comp_plans('data/stage_process', 'output')