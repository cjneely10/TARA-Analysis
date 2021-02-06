import os
import numpy as np
import pandas as pd
import altair as alt
import seaborn as sns
import streamlit as st
from typing import Dict
import matplotlib.pyplot as plt

FILE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(FILE_DIR, "data/tax-summary.tsv.gz")
FASTANI_A = os.path.join(FILE_DIR, "data/all-alex-v-alex.fastani.out.gz")
REPEATS_FILE = os.path.join(FILE_DIR, "data/repeats-summary.bylength.tsv.gz")
REPEAT_BY_PERC = os.path.join(FILE_DIR, "data/repeats-summary.tsv.gz")
TAX_LEVELS = ("kingdom", "clade", "phylum", "class", "subclass", "order", "family", "genus", "species")
TITLE = "TARA oceans data visualizer"
FILTER_BY_OPTIONS = ("size_fraction", "depth")


# Load cached file data
data_raw = load_taxonomy()
fastani_a_df = load_fastani_data(data_raw)
repeats_df = load_repeats_data(REPEATS_FILE)
repeats_perc_df = load_repeats_data(REPEAT_BY_PERC)

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
st.sidebar.write("Options")
norm_selection: Dict[str, str] = {}
if st.sidebar.checkbox("Normalize", value=False):
    norm_selection = {"stack": "normalize"}
nan_selection = st.sidebar.checkbox("Filter nan", value=True)
by_percent = st.sidebar.checkbox("Repeat content by percent", value=True)

# Generate each plot
for col in tax_selection:
    if nan_selection:
        subset = data_raw[data_raw["region"].isin(regions_selection) & data_raw[col]]
    else:
        subset = data_raw[data_raw["region"].isin(regions_selection)]
    if len(subset) == 0:
        continue
    # Generate taxonomy table and plot
    regions_str = "%s" % ", ".join(regions_selection)
    st.write("Preliminary taxonomy of regions by %s (n=%s)" % (col, str(len(subset))))
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

    # Generate histogram of repeats content
    if not by_percent:
        rep_subset = repeats_df[repeats_df.index.isin(subset.index)].astype("float32")
    else:
        rep_subset = repeats_perc_df[repeats_perc_df.index.isin(subset.index)].astype("float32")
    rep_subset = rep_subset[rep_subset["Total"] > 0.0]
    columns = list(rep_subset.columns)
    columns_drop_null = [c.replace(":", "") if rep_subset[c].mean() > 0.0 else "" for c in columns]
    fig, ax = plt.subplots()
    boxplot = rep_subset.boxplot(column=columns, ax=ax)
    plt.xticks([i + 1 for i in range(len(columns))], columns_drop_null, rotation="vertical")
    plt.xlabel("Type of repeat")
    if by_percent:
        plt.ylabel("Percent repetitive content")
    else:
        plt.ylabel("Total length of repetitive content")
    st.write("Repetitive content by %s (n=%s)" % (col, str(len(subset))))
    st.pyplot(plt, clear_figure=True)
    st.write(rep_subset)
