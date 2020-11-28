import os
import numpy as np
import pandas as pd
import altair as alt
import seaborn as sns
import streamlit as st
from typing import Dict, List
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
def load_fastani_file(file_name: str, header_ids: List[str]) -> pd.DataFrame:
    return pd.read_csv(file_name, delimiter="\t", header=0, names=header_ids, dtype="object")


@st.cache
def load_fastani_data(fastani_df: pd.DataFrame) -> pd.DataFrame:
    fastani_a = load_fastani_file(FASTANI_A, ["alexander1", "alexander2", "pid", "r1", "r2"])
    as_dict = {(k1, k2): p for k1, k2, p in zip(fastani_a.alexander1, fastani_a.alexander2, fastani_a.pid)}
    out = np.full((len(fastani_df.index), len(fastani_df.index)), 70.0, dtype="float32")
    dict_keys = as_dict.keys()
    for i, f1_name in enumerate(fastani_df.index):
        for j, f2_name in enumerate(fastani_df.index):
            if (f1_name, f2_name) in dict_keys:
                out[i, j] = float(as_dict[(f1_name, f2_name)])
    out_df = pd.DataFrame(out, index=fastani_df.index, columns=fastani_df.index)
    return out_df


# Load cached file data
data_raw = load_taxonomy()
fastani_a_df = load_fastani_data(data_raw)

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

# Generate each plot
for col in tax_selection:
    subset = data_raw[data_raw["region"].isin(regions_selection) & data_raw[col]]
    if len(subset) == 0:
        continue
    # Generate taxonomy table and plot
    regions_str = "%s" % ", ".join(regions_selection)
    st.write("Taxonomy of regions by %s (n=%s)" % (col, str(len(subset))))
    st.write(regions_str)
    st.write(subset)
    # Filter na sections for better display on chart
    subset = subset[[col, "region", filter_selection]]
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
    # Generate ANI plot and table
    st.write("Average Nucleotide Identity by %s (n=%s)" % (col, str(len(subset))))
    st.write(regions_str)
    not_present_cols = set(fastani_a_df.index) - set(subset.index)
    heatmap_df = fastani_a_df.drop(not_present_cols, axis=1).drop(not_present_cols, axis=0)
    if norm_selection != {}:
        heatmap_df /= heatmap_df.max()
    sns.heatmap(heatmap_df, square=True, cmap="mako")
    col1, col2 = st.beta_columns([5, 5])
    col1.pyplot(plt)
    col2.write(heatmap_df)
    # Clear before moving to next request
    plt.clf()
