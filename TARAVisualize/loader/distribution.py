from TARAVisualize import alt
from TARAVisualize import pd
from TARAVisualize import st


def distribution(metadata: pd.DataFrame):
    st.title("Distribution")
    col1, col2 = st.beta_columns([5, 5])
    col1.altair_chart(alt.Chart(metadata).mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3,
        width=12
    ).encode(
        x="size_fraction",
        y=alt.Y('count():O'),
        column="region"
    ).configure_axisX(labelAngle=-45))
    col2.altair_chart(alt.Chart(metadata).mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3,
        width=12
    ).encode(
        x="depth",
        y=alt.Y('count():O'),
        column="region"
    ).configure_axisX(labelAngle=-45))
