from TARAVisualize import pd
from TARAVisualize import st
from TARAVisualize import plt
from TARAVisualize import sns


def generate_fastani(fastani_df: pd.DataFrame, subset_ids):
    # Generate ANI plot and table
    st.title("Average Nucleotide Identity")
    not_present_cols = set(fastani_df.index) - subset_ids
    heatmap_df = fastani_df.drop(not_present_cols, axis=1).drop(not_present_cols, axis=0)
    sns.heatmap(heatmap_df, square=True, cmap="mako")
    st.pyplot(plt, clear_figure=True)
