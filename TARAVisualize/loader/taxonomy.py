from TARAVisualize import pd
from TARAVisualize import px
from TARAVisualize import st
from TARAVisualize.utils.tax_levels import tax_levels as levels


def get_taxonomy(metadata: pd.DataFrame):
    st.title("Taxonomy")
    st.write(metadata[levels])
    col1, col2 = st.columns([1, 1])
    for i in range(0, 8, 2):
        col1.plotly_chart(px.pie(metadata[levels[i]].dropna(), names=levels[i], title=levels[i]),
                          use_container_width=True)
        col2.plotly_chart(px.pie(metadata[levels[i + 1]].dropna(), names=levels[i + 1], title=levels[i + 1]),
                          use_container_width=True)
