import os
import altair as alt
import streamlit as st
import pandas as pd

"""
Script to visualize TARA oceans data

"""

# Path to taxonomy data
DATA_FILE = os.path.join(os.path.dirname(__file__), "data/tax-summary-adj.tsv")
# Various constants for visualization
TAX_LEVELS = ("kingdom", "clade", "phylum", "class", "subclass", "order", "family", "genus", "species")
TITLE = "TARA oceans data visualizer"
FILTER_REGIONS = ("region", "depth")


@st.cache
def load_data():
    return pd.read_csv(DATA_FILE, delimiter="\t", na_values=".", index_col=0, dtype="object")


# Create simple layout
st.title(TITLE)
st.sidebar.write(TITLE)
# Get view selection and display for user
filter_selection = st.sidebar.selectbox("Filter", FILTER_REGIONS)
st.write("Viewing by %s" % filter_selection)
# Load cached file data
data_raw = load_data()

# Generate each taxonomy plot
for col in TAX_LEVELS:
    subset = data_raw[[filter_selection, "size_fraction", col]]
    c = alt.Chart(subset.dropna()).mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3,
        width=12
    ).encode(
        x='%s:O' % col,
        y='count():O',
        color=filter_selection,
        column="size_fraction"
    ).configure_axisX(labelAngle=-45)
    st.altair_chart(c)
