"""
Quick script to pull out those specific sheets from the EDA Excel file 
and save them as CSVs for easier graphing - with automatic conversion to percentages.
"""

import pandas as pd
import numpy as np
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

# Function to identify which columns are numeric theme columns
def get_theme_columns(df):
    """Return list of columns that are likely theme percentage columns"""
    # Skip common ID/index columns
    skip_cols = ['country', 'document_type', 'architecture', 'governance',
                 'category', 'type', 'name', 'index', 'id', 'Category']
    
    numeric_cols = []
    for col in df.columns:
        # Skip if it's an ID column
        if any(skip in str(col).lower() for skip in skip_cols):
            continue
        
        # Check if column is numeric
        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_cols.append(col)
    
    return numeric_cols

# Function to standardize ID column names
def standardize_id_column(df, sheet_name):
    """Rename the first column to a consistent ID column name based on sheet type"""
    df_std = df.copy()
    first_col = df_std.columns[0]
    
    # Map sheet names to standard ID column names
    if 'Architecture' in sheet_name:
        # For architecture data, rename first column to 'governance'
        df_std = df_std.rename(columns={first_col: 'governance'})
        print(f"  Renamed '{first_col}' → 'governance'")
    elif 'National_Policy' in sheet_name:
        df_std = df_std.rename(columns={first_col: 'country_or_category'})
        print(f"  Renamed '{first_col}' → 'country_or_category'")
    elif 'UNFCCC' in sheet_name:
        df_std = df_std.rename(columns={first_col: 'country_or_category'})
        print(f"  Renamed '{first_col}' → 'country_or_category'")
    elif 'AU_Category' in sheet_name:
        df_std = df_std.rename(columns={first_col: 'document_type'})
        print(f"  Renamed '{first_col}' → 'document_type'")
    
    return df_std

# Function to convert values to percentages
def convert_to_percentage(df, theme_cols):
    """Convert numeric values to percentages (0-100 scale)"""
    df_converted = df.copy()
    
    for col in theme_cols:
        # Check the range of values to determine if conversion is needed
        max_val = df[col].max()
        min_val = df[col].min()
        
        # If values are between 0 and 1 (likely proportions), convert to percentages
        if max_val <= 1 and min_val >= 0:
            df_converted[col] = df[col] * 100
            print(f"    Converted '{col}': {min_val:.3f}-{max_val:.3f} → {df_converted[col].min():.1f}%-{df_converted[col].max():.1f}%")
        
        # If values are already percentages (0-100), leave as is
        elif max_val <= 100 and min_val >= 0:
            print(f"    '{col}' already in percentage format: {min_val:.1f}%-{max_val:.1f}%")
        
        # If values are something else (maybe counts), warn but keep as is
        else:
            print(f"    ⚠️ '{col}' has unusual range: {min_val:.2f}-{max_val:.2f} (not converted)")
    
    return df_converted

# Now grab the ones we need
for sheet_name in sheets_we_want:
    if sheet_name not in all_sheets:
        print(f"⚠️  Couldn't find '{sheet_name}' in the Excel file - skipping")
        continue
        
    try:
        print(f"\n📄 Reading '{sheet_name}'...")
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        
        # Display first few rows to see what we're working with
        print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"  Original columns: {list(df.columns)}")
        
        # Standardize the ID column name
        df = standardize_id_column(df, sheet_name)
        
        # Identify which columns are themes (numeric)
        theme_cols = get_theme_columns(df)
        print(f"  Found {len(theme_cols)} numeric theme columns")
        
        # Convert to percentages if needed
        if theme_cols:
            df_converted = convert_to_percentage(df, theme_cols)
        else:
            df_converted = df
            print("  ⚠️ No numeric theme columns found")
        
        # Clean up the filename (replace spaces with underscores)
        clean_name = sheet_name.replace(' ', '_')
        out_path = output_dir / f"{clean_name}.csv"
        
        # Save it
        df_converted.to_csv(out_path, index=False)
        
        print(f"  ✅ Saved to: {out_path}")
        print(f"  Final columns: {list(df_converted.columns)}")
        
    except Exception as e:
        print(f"❌ Something went wrong with '{sheet_name}': {e}")

# Summary
print("\n" + "="*50)
print("CONVERSION SUMMARY")
print("="*50)
print(f"All CSV files saved to: {output_dir}")
print("\nThese files now have:")
print("  • Standardized ID column names")
print("  • Theme values as percentages (0-100%)")
print("  • Ready to use with your heatmap generation script!")