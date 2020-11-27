import os
import numpy as np
import pandas as pd
import altair as alt
import seaborn as sns
import streamlit as st
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt

FILE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(FILE_DIR, "data/tax-summary.tsv")
FASTANI_A = os.path.join(FILE_DIR, "data/all-alex-v-alex.fastani.out")
FASTANI_B = os.path.join(FILE_DIR, "data/all-alex-v-delmont.fastani.out")
TAX_LEVELS = ("kingdom", "clade", "phylum", "class", "subclass", "order", "family", "genus", "species")
TITLE = "TARA oceans data visualizer"
FILTER_BY_OPTIONS = ("size_fraction", "depth")


@st.cache
def load_taxonomy() -> pd.DataFrame:
    return pd.read_csv(DATA_FILE, delimiter="\t", na_values=".", index_col=0, dtype="object")


@st.cache
def load_fastani(file_name: str, header_ids: List[str]) -> pd.DataFrame:
    return pd.read_csv(file_name, delimiter="\t", header=0, names=header_ids, dtype="object")


def create_heatmap(file_names: List[str], as_dict: Dict[Tuple[str, str], str]) -> pd.DataFrame:
    out = np.full((len(file_names), len(file_names)), 70.0, dtype="float32")
    for i, f1_name in enumerate(file_names):
        for j, f2_name in enumerate(file_names):
            if (f1_name, f2_name) in as_dict.keys():
                out[i, j] = float(as_dict[(f1_name, f2_name)])
    return pd.DataFrame(out, index=file_names, columns=file_names)


# Load cached file data
data_raw = load_taxonomy()
fastani_a = load_fastani(FASTANI_A, ["alexander1", "alexander2", "pid", "r1", "r2"])
fastani_a_dict = {(k1, k2): p for k1, k2, p in zip(fastani_a.alexander1, fastani_a.alexander2, fastani_a.pid)}
fastani_b = load_fastani(FASTANI_B, ["alexander1", "delmont", "pid", "r1", "r2"])
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
    subset = subset[[col, "region", filter_selection]].dropna()
    c = alt.Chart(subset).mark_bar(
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
    ax = sns.heatmap(create_heatmap(subset.index, fastani_a_dict), square=True,  cmap="mako")
    st.pyplot(plt)
    plt.clf()
