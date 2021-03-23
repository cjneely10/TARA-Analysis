from sklearn.decomposition import PCA
from TARAVisualize import pd
from TARAVisualize import px
from TARAVisualize import st
from TARAVisualize.utils.preprocess import fix


def generate_kegg_pca(kegg_df: pd.DataFrame):
    st.title("KEGG PCA")
    kegg_df = fix(kegg_df)
    kegg = PCA(n_components=2).fit_transform(kegg_df)
    kegg = pd.DataFrame(kegg, index=kegg_df.index).reset_index()
    st.plotly_chart(px.scatter(kegg, x=kegg.columns[1], y=kegg.columns[2], hover_name="ID"), clear_figure=True)
