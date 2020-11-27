import os
import pandas as pd
import altair as alt
import streamlit as st
from typing import Dict

FILE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(FILE_DIR, "data/tax-summary.tsv")
FASTANI_A = os.path.join(FILE_DIR, "data/all-alex-v-alex.fastani.out")
FASTANI_B = os.path.join(FILE_DIR, "data/all-del-v-alex.fastani.out")
TAX_LEVELS = ("kingdom", "clade", "phylum", "class", "subclass", "order", "family", "genus", "species")
TITLE = "TARA oceans data visualizer"
FILTER_BY_OPTIONS = ("size_fraction", "depth")


@st.cache
def load_taxonomy() -> pd.DataFrame:
    return pd.read_csv(DATA_FILE, delimiter="\t", na_values=".", index_col=0, dtype="object")


@st.cache
def load_fastani(file_name: str) -> pd.DataFrame:
    pass


# Load cached file data
data_raw = load_taxonomy()
# Create simple layout
st.title(TITLE)
st.sidebar.write(TITLE)
# Get view selection and display for user
filter_selection = st.sidebar.selectbox("Filter by", FILTER_BY_OPTIONS)
# Allow user to select which subregions to compare
regions_selection = st.sidebar.multiselect("Regions", list(set(data_raw.region)))
# Allow user to select which taxa to visualize
tax_selection = st.sidebar.multiselect("Taxonomic levels", TAX_LEVELS)
# Allow user to select normalization
norm_selection: Dict[str, str] = {}
if st.sidebar.checkbox("Normalize", value=True):
    norm_selection = {"stack": "normalize"}

# Generate each taxonomy plot
for col in tax_selection:
    subset = data_raw[data_raw["region"].isin(regions_selection)]
    if len(subset) == 0:
        continue
    st.write("Level: %s" % col)
    st.write(subset)
    c = alt.Chart(subset[[col, "region", filter_selection]].dropna()).mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3,
        width=12
    ).encode(
        x='%s:O' % col,
        y=alt.Y('count():O', **norm_selection),
        color=filter_selection,
        column="region"
    ).configure_axisX(labelAngle=-45)
    st.altair_chart(c)
