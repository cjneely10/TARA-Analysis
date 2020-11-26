import os
import pandas as pd
import altair as alt
import streamlit as st

DATA_FILE = os.path.join(os.path.dirname(__file__), "data/tax-summary.tsv")
TAX_LEVELS = ("kingdom", "clade", "phylum", "class", "subclass", "order", "family", "genus", "species")
TITLE = "TARA oceans data visualizer"
FILTER_BY_OPTIONS = ("size_fraction", "depth")


@st.cache
def load_data():
    return pd.read_csv(DATA_FILE, delimiter="\t", na_values=".", index_col=0, dtype="object")


# Load cached file data
data_raw = load_data()
# Create simple layout
st.title(TITLE)
st.sidebar.write(TITLE)
# Get view selection and display for user
filter_selection = st.sidebar.selectbox("Filter by", FILTER_BY_OPTIONS)
# Allow user to select which subregions to compare
regions_selection = st.sidebar.multiselect("Regions", list(set(data_raw.region)))
# Allow user to select normalization
norm_selection = {}
if st.sidebar.checkbox("Normalize", value=True):
    norm_selection = {"stack": "normalize"}

# Generate each taxonomy plot
for col in TAX_LEVELS:
    subset = data_raw[[*TAX_LEVELS, "region", filter_selection]]
    subset = subset[subset["region"].isin(regions_selection)]
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
