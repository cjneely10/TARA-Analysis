from collections import Counter

from TARAVisualize import pd
from TARAVisualize import st


def generate_kegg_plot(kegg_df: pd.DataFrame, kegg_ids):
    st.title("Top KEGG terms")
    counted = Counter(kegg_df.astype(bool).sum(axis=0).to_dict())
    out = {}
    for value, count in counted.most_common():
        if count == 0:
            break
        out[value] = [count, kegg_ids[value]]
    st.dataframe(pd.DataFrame.from_dict(out, orient="index", columns=["Count", "Description"]))
