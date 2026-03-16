"""
Quick script to pull out those specific sheets from the EDA Excel file 
and save them as CSVs for easier graphing.
"""

import pandas as pd
from pathlib import Path

# Where's our stuff?
excel_path = Path(r"C:\Users\Steven Groenewald\Dropbox\PC\Desktop\UP\MIT808\Github\Python_Repo\data\raw\EDA_Report_Summary_Tables.xlsx")
output_dir = Path(r"C:\Users\Steven Groenewald\Dropbox\PC\Desktop\UP\MIT808\Github\Python_Repo\data\processed")

# Make sure the output folder exists
output_dir.mkdir(parents=True, exist_ok=True)

# These are the sheets we want
sheets_we_want = [
    'Architecture_Theme_Shares',
    'National_Policy_Country_Shares',
    'UNFCCC_Country_Shares',
    'AU_Category_Shares'
]

print(f"Looking for Excel file at:\n{excel_path}\n")
print(f"Will save CSVs to:\n{output_dir}\n")

# Check if the Excel file exists first
if not excel_path.exists():
    print("❌ Uh oh - can't find the Excel file. Is the path right?")
    print(f"Looked for: {excel_path}")
    exit()

# Let's see what sheets we've got
print("Sheets in this Excel file:")
xlsx_file = pd.ExcelFile(excel_path)
all_sheets = xlsx_file.sheet_names
for sheet in all_sheets:
    print(f"  - {sheet}")
print()

# Now grab the ones we need
for sheet_name in sheets_we_want:
    if sheet_name not in all_sheets:
        print(f"⚠️  Couldn't find '{sheet_name}' in the Excel file - skipping")
        continue
        
    try:
        print(f"Reading '{sheet_name}'...")
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        
        # Clean up the filename (replace spaces with underscores)
        clean_name = sheet_name.replace(' ', '_')
        out_path = output_dir / f"{clean_name}.csv"
        
        # Save it
        df.to_csv(out_path, index=False)
        
        print(f"Saved to: {out_path}")
        print(f"Got {df.shape[0]} rows and {df.shape[1]} columns\n")
        
    except Exception as e:
        print(f"Something went wrong with '{sheet_name}': {e}\n")
