from TARAVisualize import np
from TARAVisualize import pd
from TARAVisualize import plt
from TARAVisualize import px
from TARAVisualize import st
from TARAVisualize.components.selectable_component import selectable_component


def generate_repeats(repeats: pd.DataFrame, original_repeats: pd.DataFrame):
    # Generate histogram of repeats content
    st.title("DNA Repeats")
    fig = px.scatter(repeats)
    selected_ids = selectable_component(fig)
    if selected_ids is not None:
        display_df = original_repeats[original_repeats.index.isin([selected_id["x"] for selected_id in selected_ids])]
    else:
        display_df = original_repeats
    display_df = display_df.loc[:, (display_df != 0.0).any(axis=0)].replace(np.nan, 0.0)
    st.write(display_df)
    plt.clf()


def repeats_filter(repeats: pd.DataFrame) -> pd.DataFrame:
    display_columns = ("LINEs", "SINEs", "LTR", "Small", "DNA", "Satellites", "Simple", "Unclassified")
    rep_subset = repeats[repeats["Total"] > 0.0]
    return rep_subset.replace(0.0, np.nan).filter(display_columns).rename(
        columns={"Small": "Small RNA", "DNA": "DNA repeats"}, copy=False)
