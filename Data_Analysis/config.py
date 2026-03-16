from pathlib import Path
from typing import Dict, List, Any

from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file if it exists
load_dotenv()

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")

DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

MODELS_DIR = PROJ_ROOT / "models"

REPORTS_DIR = PROJ_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass

# =============================================================================
# THEME CONFIGURATION
# =============================================================================
# Stable mapping of climate policy themes to IDs, labels, and base keywords
# These 15 themes are used consistently across all datasets for graphing and analysis

THEMES: List[Dict[str, Any]] = [
    {
        "id": "mitigation",
        "label": "Mitigation & Decarbonisation",
        "base_keywords": [
            "emissions reduction",
            "decarbonisation",
            "low carbon development",
            "carbon pricing",
            "methane abatement",
            "energy efficiency",
            "net zero"
        ]
    },
    {
        "id": "adaptation",
        "label": "Adaptation & Resilience",
        "base_keywords": [
            "resilience building",
            "vulnerability reduction",
            "disaster risk management",
            "early warning systems",
            "drought and flood response",
            "loss and damage"
        ]
    },
    {
        "id": "finance",
        "label": "Climate Finance & Investment",
        "base_keywords": [
            "climate finance needs",
            "investment mobilisation",
            "grants and concessional finance",
            "green bonds",
            "private sector finance"
        ]
    },
    {
        "id": "mrv",
        "label": "MRV, Transparency & Inventories",
        "base_keywords": [
            "measurement",
            "reporting and verification",
            "transparency",
            "greenhouse gas inventories",
            "monitoring",
            "tracking progress"
        ]
    },
    {
        "id": "energy",
        "label": "Energy Systems & Renewables",
        "base_keywords": [
            "renewable energy",
            "solar",
            "wind",
            "hydropower",
            "grid and electricity systems",
            "clean cooking",
            "electrification"
        ]
    },
    {
        "id": "transport",
        "label": "Transport Systems",
        "base_keywords": [
            "transport sector emissions",
            "vehicles",
            "electric mobility",
            "public transport",
            "aviation",
            "shipping",
            "rail"
        ]
    },
    {
        "id": "afolu",
        "label": "AFOLU, Land Use & Forestry",
        "base_keywords": [
            "land use",
            "forestry",
            "reforestation",
            "agroforestry",
            "sequestration",
            "lulucf",
            "afolu measures"
        ]
    },
    {
        "id": "agriculture",
        "label": "Agriculture & Food Systems",
        "base_keywords": [
            "climate-smart agriculture",
            "food security",
            "livestock and crops",
            "irrigation",
            "soil health",
            "sustainable farming"
        ]
    },
    {
        "id": "water",
        "label": "Water Resources",
        "base_keywords": [
            "water security",
            "catchment management",
            "groundwater",
            "river basins",
            "irrigation water",
            "drought management"
        ]
    },
    {
        "id": "health",
        "label": "Health & Heat Impacts",
        "base_keywords": [
            "climate-related health impacts",
            "malaria and disease",
            "heat stress",
            "public health resilience"
        ]
    },
    {
        "id": "waste",
        "label": "Waste & Methane",
        "base_keywords": [
            "solid waste and wastewater management",
            "landfill gas",
            "recycling",
            "methane reduction"
        ]
    },
    {
        "id": "industry",
        "label": "Industry & IPPU",
        "base_keywords": [
            "industrial processes and product use",
            "cement and manufacturing",
            "mining",
            "refrigerants and hfcs",
            "ippu measures"
        ]
    },
    {
        "id": "coastal",
        "label": "Coastal & Marine Systems",
        "base_keywords": [
            "coastal adaptation",
            "sea level rise",
            "marine ecosystems",
            "fisheries",
            "coral reefs",
            "seagrass",
            "blue economy"
        ]
    },
    {
        "id": "biodiversity",
        "label": "Biodiversity & Nature-based Solutions",
        "base_keywords": [
            "biodiversity protection",
            "ecosystems",
            "nature-based solutions",
            "protected areas",
            "ecological restoration"
        ]
    },
    {
        "id": "just_transition",
        "label": "Just Transition & Social Inclusion",
        "base_keywords": [
            "social inclusion",
            "jobs and livelihoods",
            "affected workers and communities",
            "gender and youth",
            "equity"
        ]
    }
]

# Color mapping for consistent graphing across visualizations
# Using a colorblind-friendly palette
THEME_COLORS: Dict[str, str] = {
    "mitigation": "#1f77b4",      # blue
    "adaptation": "#ff7f0e",      # orange
    "finance": "#2ca02c",          # green
    "mrv": "#d62728",              # red
    "energy": "#9467bd",           # purple
    "transport": "#8c564b",        # brown
    "afolu": "#e377c2",            # pink
    "agriculture": "#7f7f7f",      # gray
    "water": "#bcbd22",            # olive
    "health": "#17becf",           # cyan
    "waste": "#aec7e8",            # light blue
    "industry": "#ffbb78",          # light orange
    "coastal": "#98df8a",          # light green
    "biodiversity": "#ff9896",      # light red
    "just_transition": "#c5b0d5"   # light purple
}

# Helper dictionaries for quick lookups
THEME_BY_ID: Dict[str, Dict[str, Any]] = {theme["id"]: theme for theme in THEMES}
THEME_BY_LABEL: Dict[str, Dict[str, Any]] = {theme["label"]: theme for theme in THEMES}

# List of theme labels for easy reference
THEME_LABELS: List[str] = [theme["label"] for theme in THEMES]

# List of theme IDs for easy reference
THEME_IDS: List[str] = [theme["id"] for theme in THEMES]

# Metadata
THEME_CONFIG_VERSION: str = "1.0"
THEME_CONFIG_DESCRIPTION: str = "Climate policy themes from National Climate Change Policy analysis"
THEME_CONFIG_DATE_CREATED: str = "2024-01-15"
THEME_CONFIG_SOURCE: str = "National_Climate_Policies_Guided_Paragraph_Themes_COMBINED.xlsx"
THEME_CONFIG_NOTES: str = "Base keywords derived from Theme_Definitions sheet. Expanded variants stored in raw data only."