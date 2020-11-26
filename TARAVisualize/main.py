import altair as alt
import streamlit as st
import pandas as pd

tax_levels = ("kingdom", "clade", "phylum", "class", "subclass", "order", "family", "genus", "species")


@st.cache
def load_data():
    return pd.read_csv("/home/kmarvos/Data/Analysis/data/tax-summary-adj.tsv", delimiter="\t", na_values=".",
                       index_col=0, dtype="object")


st.title("TARA oceans data visualizer")

data_raw = load_data()

filter_selection = st.sidebar.selectbox("Filter data by:", ("region", "depth"))

for col in tax_levels:
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
