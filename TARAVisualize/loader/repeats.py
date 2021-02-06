import plotly.express as px
from TARAVisualize import pd
from TARAVisualize import st
from TARAVisualize import plt
from TARAVisualize.components.selectable_component import selectable_component


def generate_repeats(repeats: pd.DataFrame):
    # Generate histogram of repeats content
    rep_subset = repeats[repeats["Total"] > 0.0]
    columns = list(rep_subset.columns)
    columns_drop_null = [c.replace(":", "") if rep_subset[c].mean() > 0.0 else "" for c in columns]
    fig, ax = plt.subplots()
    boxplot = rep_subset.boxplot(column=columns, ax=ax)
    plt.xticks([i + 1 for i in range(len(columns))], columns_drop_null, rotation="vertical")
    plt.xlabel("Type of repeat")
    plt.ylabel("Total length of repetitive content")
    st.title("DNA Repeats")
    selectable_component(px.box(repeats))
    plt.clf()
