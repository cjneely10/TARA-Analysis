from TARAVisualize import pd
from TARAVisualize import px
from TARAVisualize import st


def get_taxonomy(metadata: pd.DataFrame):
    levels = ["clade", "kingdom", "phylum", "class", "order", "family", "genus", "species"]
    st.title("Taxonomy")
    col1, col2 = st.beta_columns([1, 1])
    i = 0
    for _ in range(4):
        data = metadata[levels[i]].dropna()
        col1.plotly_chart(px.pie(data, names=levels[i], title=levels[i]))
        i += 1
        data = metadata[levels[i]].dropna()
        col2.plotly_chart(px.pie(data, names=levels[i], title=levels[i]))
        i += 1
