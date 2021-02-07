from typing import Tuple, Set

from TARAVisualize import st
from TARAVisualize import pd


def get_region_filterby_selection(metadata: pd.DataFrame) -> Set[str]:
    title = "TOPAZ data visualizer"
    # Create simple layout
    st.sidebar.write(title)
    # Allow user to select which subregions to compare
    regions_selection = st.sidebar.multiselect("Regions", list(set(metadata.region)))

    if regions_selection:
        # Display filtered results as table
        filtered_data = metadata[metadata.region.isin(regions_selection)]
        if len(regions_selection) == 1:
            st.sidebar.write(f"{len(filtered_data)} MAGs in region {regions_selection[0]}")
        else:
            st.sidebar.write(f"{len(filtered_data)} MAGs in regions {', '.join(regions_selection)}")
        # Show dataframe on menu for selection
        return set(filtered_data.index)
