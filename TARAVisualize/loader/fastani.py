from typing import Set
from TARAVisualize import pd
from TARAVisualize import px
from TARAVisualize import st
from TARAVisualize.utils.cluster import hClust_euclidean


def generate_fastani(heatmap_df: pd.DataFrame, aai_df: pd.DataFrame):
    # Generate ANI plot and table
    st.title("Average Nucleotide Identity")
    cluster = st.checkbox("Cluster?", key=1)
    if cluster:
        heatmap_df = hClust_euclidean(heatmap_df)
    st.plotly_chart(px.imshow(heatmap_df.to_numpy(), labels={"color": "ANI"},
                              x=heatmap_df.index, y=heatmap_df.columns), clear_figure=True)
    st.title("Average Amino Acid Identity")
    cluster = st.checkbox("Cluster?", key=2)
    if cluster:
        aai_df = hClust_euclidean(aai_df)
    st.plotly_chart(px.imshow(aai_df.to_numpy(), labels={"color": "AAI"},
                              x=aai_df.index, y=aai_df.columns), clear_figure=True)


def filter_fastani_aai(aa_df: pd.DataFrame, subset_ids: Set[str]) -> pd.DataFrame:
    not_present_cols = set(aa_df.index) - subset_ids
    return aa_df.drop(not_present_cols, axis=1).drop(not_present_cols, axis=0)
