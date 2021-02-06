from TARAVisualize import pd
from TARAVisualize import px
from TARAVisualize import plt
from TARAVisualize.components.selectable_component import selectable_component


def generate_repeats(repeats: pd.DataFrame):
    # Generate histogram of repeats content
    rep_subset = repeats[repeats["Total"] > 0.0]
    selectable_component(px.box(rep_subset))
    plt.clf()
