#Correlation Analysis

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform


script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


try:
    from Data_Analysis.config import THEME_LABELS
    print(f"Loaded {len(THEME_LABELS)} themes from config")
except ImportError:
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

print(f"\n Data directory: {data_processed}")
print(f"Saving figures to: {figures_dir}\n")


df_national = pd.read_csv(data_processed / "National_Policy_Country_Shares.csv")


id_cols = ['country_or_category', 'document_type', 'governance']
theme_cols = [col for col in df_national.columns if col in THEME_LABELS]
print(f"Analyzing {len(theme_cols)} themes across {len(df_national)} countries\n")

# Calculate correlation matrix
theme_data = df_national[theme_cols]
corr_matrix = theme_data.corr()

# Create clustered heatmap
plt.figure(figsize=(14, 12))

# Generate clustering
corr_linkage = hierarchy.ward(corr_matrix)
cluster_ids = hierarchy.fcluster(corr_linkage, 1, criterion='distance')
cluster_order = np.argsort(cluster_ids)

# Reorder correlation matrix by clusters
clustered_corr = corr_matrix.iloc[cluster_order, cluster_order]

# Create mask for upper triangle
mask = np.triu(np.ones_like(clustered_corr, dtype=bool), k=1)

# Plot
sns.heatmap(clustered_corr, 
            mask=mask,
            cmap='RdBu_r', 
            center=0,
            vmin=-0.5, vmax=0.5,
            annot=True, 
            fmt='.2f',
            square=True,
            linewidths=0.5,
            cbar_kws={"label": "Correlation Coefficient"})

plt.title('Climate Theme Clusters: Which Topics Travel Together?\n(National Climate Policies)', 
          fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(figures_dir / 'theme_clusters_correlation.svg', dpi=300, bbox_inches='tight')
print(f"Saved correlation matrix to: {figures_dir / 'theme_clusters_correlation.svg'}")

# Print the clusters found
print("\n THEME CLUSTERS FOUND:")
print("="*50)
unique_clusters = np.unique(cluster_ids)
for cluster_id in unique_clusters:
    themes_in_cluster = [theme_cols[i] for i in range(len(theme_cols)) 
                        if cluster_ids[i] == cluster_id]
    print(f"\nCluster {cluster_id}:")
    for theme in themes_in_cluster:
        print(f"{theme}")

print("\n Comparing Across Governance Levels...")
print("="*50)

datasets = {
    'National': df_national,
    'Paris': pd.read_csv(data_processed / "UNFCCC_Country_Shares.csv"),
    'AU': pd.read_csv(data_processed / "AU_Category_Shares.csv")
}

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for ax, (name, df) in zip(axes, datasets.items()):
    # Get theme columns
    df_themes = [col for col in df.columns if col in THEME_LABELS]
    
    # Calculate mean theme presence
    theme_means = df[df_themes].mean().sort_values()
    
    # Plot horizontal bar chart
    theme_means.plot(kind='barh', ax=ax, color='steelblue')
    ax.set_title(f'{name} Level\nAverage Theme Focus', fontsize=12, fontweight='bold')
    ax.set_xlabel('Mean %')
    ax.set_xlim(0, 20)  # Consistent scale
    
plt.tight_layout()
plt.savefig(figures_dir / 'governance_level_comparison.svg', dpi=300, bbox_inches='tight')
print(f"Saved governance comparison to: {figures_dir / 'governance_level_comparison.svg'}")

print("\n Analysis complete!")
