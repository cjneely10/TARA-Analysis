from TARAVisualize import pd
from TARAVisualize import px
from TARAVisualize import st


def generate_fastani(heatmap_df):
    # Generate ANI plot and table
    st.title("Average Nucleotide Identity")
    st.plotly_chart(px.imshow(heatmap_df.to_numpy(), x=heatmap_df.index, y=heatmap_df.columns), clear_figure=True)


def filter_fastani(fastani_df, subset_ids):
    not_present_cols = set(fastani_df.index) - subset_ids
    return fastani_df.drop(not_present_cols, axis=1).drop(not_present_cols, axis=0)
