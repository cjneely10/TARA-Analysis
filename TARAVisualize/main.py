import os
import altair as alt
import streamlit as st
import pandas as pd

"""
Script to visualize TARA oceans data

"""

# Path to taxonomy data
DATA_FILE = os.path.join(os.path.dirname(__file__), "data/tax-summary.tsv")
# Various constants for visualization
TAX_LEVELS = ("kingdom", "clade", "phylum", "class", "subclass", "order", "family", "genus", "species")
TITLE = "TARA oceans data visualizer"
FILTER_BY_OPTIONS = ("size_fraction", "depth")


@st.cache
def load_data():
    return pd.read_csv(DATA_FILE, delimiter="\t", na_values=".", index_col=0, dtype="object")


# Create simple layout
st.title(TITLE)
st.sidebar.write(TITLE)
# Get view selection and display for user
filter_selection = st.sidebar.selectbox("Filter by", FILTER_BY_OPTIONS)
st.write("Viewing by %s" % filter_selection)

# Load cached file data
data_raw = load_data()

# Allow user to select which subregions to compare
regions_selection = st.sidebar.multiselect("Regions", list(set(data_raw.region)))

# Generate each taxonomy plot
for col in TAX_LEVELS:
    st.write("Level: %s" % col)
    subset = data_raw[[col, "region", filter_selection]]
    subset = subset[subset["region"].isin(regions_selection)]
    st.write(subset)
    c = alt.Chart(subset.dropna()).mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3,
        width=12
    ).encode(
        x='%s:O' % col,
        y=alt.Y('count():O', stack="normalize"),
        color=filter_selection,
        column="region"
    ).configure_axisX(labelAngle=-45)
    st.altair_chart(c)
