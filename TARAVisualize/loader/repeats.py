from TARAVisualize import np
from TARAVisualize import pd
from TARAVisualize import px
from TARAVisualize import plt
from TARAVisualize.components.selectable_component import selectable_component


def generate_repeats(repeats: pd.DataFrame):
    # Generate histogram of repeats content
    display_columns = ("LINEs", "SINEs", "LTR", "Small", "DNA", "Satellites", "Simple" "Unclassified")
    rep_subset = repeats[repeats["Total"] > 0.0]
    rep_subset = rep_subset.replace(0.0, np.nan)
    rep_subset = rep_subset.filter(display_columns)
    rep_subset.rename(columns={"Small": "Small RNA", "DNA": "DNA repeats"}, copy=False)
    fig = px.scatter(rep_subset)
    selected_ids = selectable_component(fig)
    if selected_ids is not None:
        pass
    plt.clf()
