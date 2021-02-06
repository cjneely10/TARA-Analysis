from TARAVisualize import st
from TARAVisualize import pd
from TARAVisualize import alt


def generate_taxonomy_display(metadata: pd.DataFrame, filter_option: str):
    # Generate taxonomy table and plot
    st.title("Taxonomy")
    st.write(metadata)
    c = alt.Chart(metadata).mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3,
        width=12
    ).encode(
        x=filter_option,
        y=alt.Y('count():O'),
        column="region"
    ).configure_axisX(labelAngle=-45)
    st.altair_chart(c)
