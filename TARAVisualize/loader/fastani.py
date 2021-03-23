from typing import Set

from scipy.cluster.hierarchy import linkage, dendrogram

from TARAVisualize import pd
from TARAVisualize import px
from TARAVisualize import st


def hClust_euclidean(genome_df):
    linkage_matrix = linkage(genome_df, method='average', metric='euclidean')
    names = genome_df.index.tolist()
    clust = dendrogram(linkage_matrix, no_plot=True, labels=names, get_leaves=True)
    return genome_df.reindex(list(clust['ivl']))


def generate_fastani(heatmap_df: pd.DataFrame):
    # Generate ANI plot and table
    st.title("Average Nucleotide Identity")
    cluster = st.checkbox("Cluster?")
    if cluster:
        heatmap_df = hClust_euclidean(heatmap_df)
    st.plotly_chart(px.imshow(heatmap_df.to_numpy(), labels={"color": "ANI"},
                              x=heatmap_df.index, y=heatmap_df.columns), clear_figure=True)


def filter_fastani(fastani_df: pd.DataFrame, subset_ids: Set[str]) -> pd.DataFrame:
    not_present_cols = set(fastani_df.index) - subset_ids
    return fastani_df.drop(not_present_cols, axis=1).drop(not_present_cols, axis=0)
