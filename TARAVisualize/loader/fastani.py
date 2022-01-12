from typing import Set
from TARAVisualize import pd
from TARAVisualize import px
from TARAVisualize import st


def generate_fastani(heatmap_df: pd.DataFrame, aai_df: pd.DataFrame):
    # Generate ANI plot and table
    st.title("Average Identity")
    col1, col2 = st.columns([1, 1])
    col1.plotly_chart(px.imshow(heatmap_df.to_numpy(), labels={"color": "ANI"},
                                x=heatmap_df.index, y=heatmap_df.columns), clear_figure=True)
    col2.plotly_chart(px.imshow(aai_df.to_numpy(), labels={"color": "AAI"},
                                x=aai_df.index, y=aai_df.columns), clear_figure=True)


def filter_fastani_aai(aa_df: pd.DataFrame, subset_ids: Set[str]) -> pd.DataFrame:
    not_present_cols = set(aa_df.index) - subset_ids
    return aa_df.drop(not_present_cols, axis=1).drop(not_present_cols, axis=0)
