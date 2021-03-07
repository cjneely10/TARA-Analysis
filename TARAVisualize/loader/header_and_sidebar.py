from typing import Set

from TARAVisualize import pd
from TARAVisualize import st
from TARAVisualize.utils.tax_levels import tax_levels


def get_mags_list(metadata: pd.DataFrame) -> Set[str]:
    title = "TOPAZ data visualizer"
    # Create simple layout
    st.sidebar.write(title)
    st.sidebar.write("Filter by")
    # Allow user to select which subregions to compare
    regions_selection = st.sidebar.multiselect("Regions", list(set(metadata.region)))
    size_fraction_selection = st.sidebar.multiselect("Size Fraction", list(set(metadata.size_fraction)))
    depth_selection = st.sidebar.multiselect("Depth", list(set(metadata.depth)))
    taxonomy_selection = st.sidebar.selectbox("Taxonomic Level", ["all", *tax_levels])
    filtered_data = metadata

    level_selected = False
    if taxonomy_selection != "all":
        levels_selection = st.sidebar.multiselect("Select Assignment",
                                                  list(set(filtered_data[taxonomy_selection])))
        if len(levels_selection) > 0:
            level_selected = True
            filtered_data = filtered_data[filtered_data[taxonomy_selection].isin(levels_selection)]

    if len(regions_selection) + len(size_fraction_selection) + len(depth_selection) > 0 or level_selected:
        # Display filtered results as table
        if len(regions_selection) > 0:
            filtered_data = filtered_data[filtered_data.region.isin(regions_selection)]
        if len(size_fraction_selection) > 0:
            filtered_data = filtered_data[filtered_data.size_fraction.isin(size_fraction_selection)]
        if len(depth_selection) > 0:
            filtered_data = filtered_data[filtered_data.depth.isin(depth_selection)]
        st.sidebar.write(f"{len(filtered_data)} MAGs selected")
        # Show dataframe on menu for selection
        return set(filtered_data.index)
