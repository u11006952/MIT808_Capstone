# Generate heatmaps

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import textwrap
import numpy as np
from pathlib import Path
import sys



script_dir = Path(__file__).resolve().parent
if script_dir.name == "notebooks":
    project_root = script_dir.parent
else:
    project_root = script_dir

# Add project root to Python path so we can import config
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import themes from config
try:
    from Data_Analysis.config import THEME_LABELS, THEME_BY_LABEL
    print(f"Successfully loaded {len(THEME_LABELS)} themes from config")
except ImportError as e:
    print(f"Couldn't import from config: {e}")
    print("Using fallback theme list...")
    # Fallback theme list if config can't be found
    THEME_LABELS = [
        "Mitigation & Decarbonisation",
        "Adaptation & Resilience",
        "Climate Finance & Investment",
        "MRV, Transparency & Inventories",
        "Energy Systems & Renewables",
        "Transport Systems",
        "AFOLU, Land Use & Forestry",
        "Agriculture & Food Systems",
        "Water Resources",
        "Health & Heat Impacts",
        "Waste & Methane",
        "Industry & IPPU",
        "Coastal & Marine Systems",
        "Biodiversity & Nature-based Solutions",
        "Just Transition & Social Inclusion"
    ]



data_processed = project_root / "data" / "processed"
figures_dir = project_root / "reports" / "figures"
figures_dir.mkdir(parents=True, exist_ok=True)

print(f"\n Project root: {project_root}")
print(f"Data directory: {data_processed}")
print(f"Saving figures to: {figures_dir}\n")


plt.rcParams.update({
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "legend.title_fontsize": 9,
    "svg.fonttype": "none"  # Keep text as text in SVG, not outlines
})

sns.set_style("white")

print("Loading processed data...")

# Dataset 1: National Climate Policies
df_national = pd.read_csv(data_processed / "National_Policy_Country_Shares.csv")
print(f"National policies: {df_national.shape[0]} countries")
print(f" Columns: {list(df_national.columns)}")

# Dataset 2: Paris Agreement Submissions (UNFCCC)
df_paris = pd.read_csv(data_processed / "UNFCCC_Country_Shares.csv")
print(f"Paris Agreement: {df_paris.shape[0]} countries")
print(f" Columns: {list(df_paris.columns)}")

# Dataset 3: African Union Documents
df_au = pd.read_csv(data_processed / "AU_Category_Shares.csv")
print(f"AU documents: {df_au.shape[0]} document types")
print(f" Columns: {list(df_au.columns)}")

# Dataset 4: Architecture Theme Shares (for line plot)
df_architecture = pd.read_csv(data_processed / "Architecture_Theme_Shares.csv")
print(f"Architecture shares: {df_architecture.shape[0]} governance levels")
print(f" Columns: {list(df_architecture.columns)}\n")

#Themes

# Get the columns that are actually themes (the ones in THEME_LABELS)
def get_theme_columns(df):
    """Return list of columns that match theme labels from config"""
    return [col for col in df.columns if col in THEME_LABELS]

# Make sure we're only using the theme columns that exist in each dataframe
national_themes = get_theme_columns(df_national)
paris_themes = get_theme_columns(df_paris)
au_themes = get_theme_columns(df_au)
arch_themes = get_theme_columns(df_architecture)

print(f" Found {len(national_themes)} themes in national data")
print(f" Found {len(paris_themes)} themes in Paris data")
print(f" Found {len(au_themes)} themes in AU data")
print(f" Found {len(arch_themes)} themes in architecture data\n")


def wrap_labels(labels, width=10):
    """
    Wrap labels to specified width with better handling for long theme names
    """
    wrapped = []
    for label in labels:
        # Special handling for specific long theme names
        if "Mitigation & Decarbonisation" in str(label):
            wrapped.append("Mitigation &\nDecarbonisation")
        elif "Climate Finance & Investment" in str(label):
            wrapped.append("Climate Finance &\nInvestment")
        elif "MRV, Transparency & Inventories" in str(label):
            wrapped.append("MRV, Transparency &\nInventories")
        elif "Energy Systems & Renewables" in str(label):
            wrapped.append("Energy Systems &\nRenewables")
        elif "AFOLU, Land Use & Forestry" in str(label):
            wrapped.append("AFOLU, Land Use &\nForestry")
        elif "Agriculture & Food Systems" in str(label):
            wrapped.append("Agriculture &\nFood Systems")
        elif "Biodiversity & Nature-based Solutions" in str(label):
            wrapped.append("Biodiversity &\nNature-based Solutions")
        elif "Just Transition & Social Inclusion" in str(label):
            wrapped.append("Just Transition &\nSocial Inclusion")
        elif "Health & Heat Impacts" in str(label):
            wrapped.append("Health &\nHeat Impacts")
        elif "Coastal & Marine Systems" in str(label):
            wrapped.append("Coastal &\nMarine Systems")
        elif "Industry & IPPU" in str(label):
            wrapped.append("Industry &\nIPPU")
        elif "Transport Systems" in str(label):
            wrapped.append("Transport\nSystems")
        elif "Water Resources" in str(label):
            wrapped.append("Water\nResources")
        elif "Waste & Methane" in str(label):
            wrapped.append("Waste &\nMethane")
        else:
            # Default wrapping for any other labels
            wrapped.append('\n'.join(textwrap.wrap(str(label), width=width)))
    return wrapped

def save_svg_heatmap(df, id_col, title, filename, figsize=None, 
                     bottom_margin=0.32, x_label_pad=28, tick_pad=18, annot_size=7):
    """
    Save SVG heatmap with dataset-adaptive color scaling
    """
    plot_df = df.copy()
    
    # Check if the ID column exists, if not try to find it
    if id_col not in plot_df.columns:
        possible_ids = ['country_or_category', 'country', 'document_type', 'governance', 'Category']
        for possible_id in possible_ids:
            if possible_id in plot_df.columns:
                id_col = possible_id
                print(f" Using '{id_col}' as ID column for {filename}")
                break
    
    plot_df = plot_df.set_index(id_col)
    
    # Get dimensions for dynamic sizing
    n_rows, n_cols = plot_df.shape
    
    # Calculate dataset-specific min and max for color scaling
    data_min = plot_df.min().min()
    data_max = plot_df.max().max()
    
    # Round to nearest 5 for nice tick intervals
    vmin = max(0, np.floor(data_min / 5) * 5)  # Don't go below 0
    vmax = np.ceil(data_max / 5) * 5
    
    # Generate appropriate ticks based on data range
    tick_step = 5 if vmax <= 50 else 10
    ticks = np.arange(vmin, vmax + tick_step, tick_step)
    
    print(f" Dataset range: {data_min:.1f}% to {data_max:.1f}%")
    print(f" Color scale: {vmin:.0f}% to {vmax:.0f}%")
    
    # Set default figsize based on dataset size if not provided
    if figsize is None:
        if n_cols > 12:
            figsize = (20, 14)
        elif n_cols > 8:
            figsize = (18, 12)
        else:
            figsize = (14, 8)
    
    # Add percentage labels inside cells with one decimal place
    labels = plot_df.round(1).astype(str) + "%"
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create heatmap with dataset-specific color scaling
    heatmap = sns.heatmap(
        plot_df,
        cmap="YlGnBu",
        linewidths=0.5,
        annot=labels,
        fmt="",
        annot_kws={"size": annot_size},
        cbar_kws={
            "label": "Theme Share (%)", 
            "shrink": 0.8,
            "ticks": ticks,
            "orientation": "vertical",
            "pad": 0.02
        },
        vmin=vmin, vmax=vmax,  # Dataset-specific color scale
        ax=ax
    )
    
    # Make sure the colorbar label is visible and properly formatted
    cbar = heatmap.collections[0].colorbar
    cbar.set_label("Theme Share (%)", fontsize=10, fontweight="normal", labelpad=15)
    cbar.ax.tick_params(labelsize=9)
    
    # Format x-axis labels with wrapping
    wrapped_labels = wrap_labels(plot_df.columns, 10)
    ax.set_xticklabels(wrapped_labels, rotation=45, ha="right", fontsize=9)
    
    # Add padding to tick labels
    ax.tick_params(axis='x', pad=tick_pad)
    
    # Format y-axis labels
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=8)
    
    # Titles and labels with custom padding
    ax.set_title(title, fontsize=14, fontweight="bold", pad=30)
    ax.set_xlabel("Climate Themes", fontsize=11, fontweight="bold", labelpad=x_label_pad)
    ax.set_ylabel(id_col.replace("_", " ").title(), fontsize=11, fontweight="bold", labelpad=15)
    
    # Adjust layout with custom bottom margin
    plt.tight_layout()
    plt.subplots_adjust(bottom=bottom_margin)
    
    # Save as SVG in the figures directory
    full_path = figures_dir / filename
    plt.savefig(full_path, dpi=300, bbox_inches="tight", facecolor="white", format="svg")
    print(f"Saved: {full_path}")
    plt.close()

def save_line_plot(df, id_col, title, filename, figsize=(12, 6)):
    """
    Create a line plot showing theme distribution across governance levels
    """
    plot_df = df.copy()
    
    # Check what the ID column actually is
    print(f" Line plot - using ID column: {id_col}")
    print(f" Available columns: {list(plot_df.columns)}")
    
    # If the specified id_col isn't found, try to find the most likely one
    if id_col not in plot_df.columns:
        possible_ids = ['governance', 'Governance', 'architecture', 'Architecture', 
                       'country', 'document_type', 'category', 'country_or_category']
        for possible_id in possible_ids:
            if possible_id in plot_df.columns:
                id_col = possible_id
                print(f" Using '{id_col}' as ID column instead")
                break
    
    plot_df = plot_df.set_index(id_col)
    
    # Transpose so themes become rows, governance levels become columns
    plot_df = plot_df.T
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot each governance level as a line
    for column in plot_df.columns:
        ax.plot(plot_df.index, plot_df[column], marker='o', linewidth=2, markersize=6, label=column)
    
    # Wrap x-axis labels
    wrapped_labels = wrap_labels(plot_df.index, 10)
    ax.set_xticks(range(len(plot_df.index)))
    ax.set_xticklabels(wrapped_labels, rotation=45, ha="right", fontsize=9)
    
    # Add labels and title
    ax.set_title(title, fontsize=14, fontweight="bold", pad=20)
    ax.set_xlabel("Climate Themes", fontsize=11, fontweight="bold", labelpad=15)
    ax.set_ylabel("Theme Share (%)", fontsize=11, fontweight="bold", labelpad=10)
    
    # Add legend
    ax.legend(title="Governance Level", bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Add grid for readability
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Adjust layout to make room for legend
    plt.tight_layout()
    plt.subplots_adjust(right=0.85)
    
    # Save as SVG
    full_path = figures_dir / filename
    plt.savefig(full_path, dpi=300, bbox_inches="tight", facecolor="white", format="svg")
    print(f"Saved line plot: {full_path}")
    plt.close()

#Heatmaps

print("\n" + "="*80)
print("GENERATING SVG HEATMAPS")
print("="*80)

# 1. National Climate Policies SVG Heatmap
print("\n National Climate Policies")
save_svg_heatmap(
    df_national,
    id_col="country_or_category",
    title="National Climate Policies: Theme Shares by Country",
    filename="national_policies_heatmap.svg",
    figsize=(16, 10),
    bottom_margin=0.32,
    x_label_pad=28,
    tick_pad=18,
    annot_size=7
)

# 2. Paris Agreement Submissions SVG Heatmap
print("\n Paris Agreement Submissions")
save_svg_heatmap(
    df_paris,
    id_col="country_or_category",
    title="Paris Agreement Submissions: Theme Shares by Country",
    filename="paris_agreement_heatmap.svg",
    figsize=(18, 12),
    bottom_margin=0.32,
    x_label_pad=28,
    tick_pad=18,
    annot_size=7
)

# 3. AU Documents SVG Heatmap
print("\n African Union Documents")
save_svg_heatmap(
    df_au,
    id_col="document_type",
    title="African Union Documents: Climate Theme Distribution by Document Type",
    filename="au_documents_heatmap.svg",
    figsize=(14, 6),
    bottom_margin=0.32,
    x_label_pad=25,
    tick_pad=15,
    annot_size=9
)

# 4. Architecture Theme Shares - Line Plot
print("\n  Governance Architecture Comparison")
save_line_plot(
    df_architecture,
    id_col="governance",  # Changed from "architecture" to "governance"
    title="Climate Theme Distribution Across Governance Levels",
    filename="architecture_comparison_lineplot.svg",
    figsize=(14, 7)
)


print("\n" + "="*80)
print("ALL FIGURES GENERATED SUCCESSFULLY!")
print("="*80)

print(f"\n📊 Files saved to: {figures_dir}")
print("-" * 40)
print(f" {figures_dir / 'national_policies_heatmap.svg'}")
print(f" {figures_dir / 'paris_agreement_heatmap.svg'}")
print(f" {figures_dir / 'au_documents_heatmap.svg'}")
print(f" {figures_dir / 'architecture_comparison_lineplot.svg'}")

print(f"You can find these in: {figures_dir}")
