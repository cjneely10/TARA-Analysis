from typing import Tuple, Set

from TARAVisualize import st
from TARAVisualize import pd


def get_region_filterby_selection(metadata: pd.DataFrame) -> Tuple[str, Set[str]]:
    title = "TOPAZ data visualizer"
    # Create simple layout
    st.sidebar.write(title)

    # Get view selection and display for user
    filter_selection = st.sidebar.selectbox("Filter by", ("size_fraction", "depth"))
    # Allow user to select which subregions to compare
    regions_selection = st.sidebar.multiselect("Regions", list(set(metadata.region)))
    # Display filtered results as table
    filtered_data = metadata[metadata.region.isin(regions_selection)]
    # Show dataframe on menu for selection
    selected_ids = set(st.sidebar.multiselect(f"MAGs (n = {len(filtered_data.index)})", filtered_data.index))
    if len(selected_ids) == 0:
        selected_ids = set(filtered_data.index)
    return filter_selection, selected_ids
