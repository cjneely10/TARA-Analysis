from TARAVisualize import pd
from TARAVisualize import px
from TARAVisualize import st


def generate_quality(quality: pd.DataFrame):
    quality = quality.reset_index()
    st.title("Quality metrics")
    col1, col2 = st.beta_columns([2, 5])
    col1.plotly_chart(px.box(quality[["n50", "ID"]], points="all", width=250, hover_name="ID"))
    col2.plotly_chart(px.box(quality.drop("n50", axis=1), points="all", hover_name="ID"))
