from TARAVisualize import pd
from TARAVisualize import px
from TARAVisualize import st


def generate_quality(quality: pd.DataFrame):
    quality = quality.reset_index()
    st.title("Quality metrics")
    col1, col2 = st.columns([2, 5])
    col1.plotly_chart(px.box(quality[["n50", "ID"]], points="all", hover_name="ID"), use_container_width=True)
    col2.plotly_chart(px.box(quality.drop("n50", axis=1), points="all", hover_name="ID"), use_container_width=True)
