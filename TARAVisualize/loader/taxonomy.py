from TARAVisualize import st
from TARAVisualize import pd
from TARAVisualize import alt


def generate_taxonomy_display(metadata: pd.DataFrame, filter_option: str):
    st.title("Distribution by %s" % filter_option)
    c = alt.Chart(metadata).mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3,
        width=12
    ).encode(
        x=("size_fraction" if filter_option[0] == "S" else "depth"),
        y=alt.Y('count():O'),
        column="region"
    ).configure_axisX(labelAngle=-45)
    st.altair_chart(c)
