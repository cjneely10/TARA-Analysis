from typing import Set

from TARAVisualize import pd
from TARAVisualize import st


def get_mags_list(metadata: pd.DataFrame) -> Set[str]:
    title = "TOPAZ data visualizer"
    tax_levels = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
    # Create simple layout
    st.sidebar.write(title)
    # Allow user to select which subregions to compare
    regions_selection = st.sidebar.multiselect("Regions", list(set(metadata.region)))
    size_fraction_selection = st.sidebar.multiselect("Size Fraction", list(set(metadata.size_fraction)))
    depth_selection = st.sidebar.multiselect("Depth", list(set(metadata.depth)))

    if len(regions_selection) + len(size_fraction_selection) + len(depth_selection) > 0:
        # Display filtered results as table
        filtered_data = metadata[metadata.region.isin(regions_selection)
                                 & metadata.size_fraction.isin(size_fraction_selection)
                                 & metadata.depth.isin(depth_selection)]
        st.sidebar.write(f"{len(filtered_data)} MAGs selected")
        # Show dataframe on menu for selection
        return set(filtered_data.index)
