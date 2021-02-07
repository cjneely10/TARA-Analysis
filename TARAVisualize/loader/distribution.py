from TARAVisualize import st
from TARAVisualize import pd
from TARAVisualize import alt


def distribution(metadata: pd.DataFrame):
    st.title("Distribution")
    c1 = alt.Chart(metadata).mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3,
        width=12
    ).encode(
        x="size_fraction",
        y=alt.Y('count():O'),
        column="region"
    ).configure_axisX(labelAngle=-45)
    c2 = alt.Chart(metadata).mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3,
        width=12
    ).encode(
        x="depth",
        y=alt.Y('count():O'),
        column="region"
    ).configure_axisX(labelAngle=-45)
    col1, col2 = st.beta_columns([5, 5])
    col1.altair_chart(c1)
    col2.altair_chart(c2)
