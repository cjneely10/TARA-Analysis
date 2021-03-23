from collections import Counter

from sklearn import preprocessing

from TARAVisualize import pd
from TARAVisualize import px
from TARAVisualize import st
from sklearn.decomposition import PCA


def generate_kegg_plot(kegg_df: pd.DataFrame, kegg_ids):
    st.title("Top KEGG terms")
    generate_kegg_pca(kegg_df)
    counted = Counter(kegg_df.astype(bool).sum(axis=0).to_dict())
    out = {}
    for value, count in counted.most_common():
        if count == 0:
            break
        out[value] = [count, kegg_ids[value]]
    st.dataframe(pd.DataFrame.from_dict(out, orient="index", columns=["Count", "Description"]))


def generate_kegg_pca(kegg_df: pd.DataFrame):
    kegg = PCA(n_components=2).fit_transform(scale(kegg_df.loc[:, (kegg_df != 0).any(axis=0)]))
    st.plotly_chart(px.scatter(kegg[:, 0], kegg[:, 1]), clear_figure=True)


def scale(df):
    x = df.values  # returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    return pd.DataFrame(x_scaled, columns=df.columns, index=df.index)
