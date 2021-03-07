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
    regions_selection = st.sidebar.multiselect("Regions", sorted(list(set(metadata.region))))
    size_fraction_selection = st.sidebar.multiselect("Size Fraction",
                                                     sorted(list(set(metadata.size_fraction)),
                                                            key=lambda val: int(val.split("-")[0])))
    depth_selection = st.sidebar.multiselect("Depth", sorted(list(set(metadata.depth))))
    taxonomy_selection = st.sidebar.selectbox("Taxonomic Level", ["all", *tax_levels])
    filtered_data = metadata

    level_selected = False
    levels_selection = None
    if taxonomy_selection != "all":
        levels_selection = st.sidebar.multiselect("Select Assignment",
                                                  sorted(list(set(filtered_data[taxonomy_selection].dropna()))))
        if len(levels_selection) > 0:
            level_selected = True

    if len(regions_selection) + len(size_fraction_selection) + len(depth_selection) > 0 or level_selected:
        # Display filtered results as table
        to_filter = []
        if len(regions_selection) > 0:
            to_filter.append(("region", "regions_selection"))
        if len(size_fraction_selection) > 0:
            to_filter.append(("size_fraction", "size_fraction_selection"))
        if len(depth_selection) > 0:
            to_filter.append(("depth", "depth_selection"))
        if levels_selection is not None and len(levels_selection) > 0:
            to_filter.append((taxonomy_selection, "levels_selection"))
        filtered_data = filtered_data[eval("&".join([('filtered_data["%s"].isin(%s)' % (label, selection))
                                                    for label, selection in to_filter]))]
        st.sidebar.write(f"{len(filtered_data)} MAGs selected")
        # Show dataframe on menu for selection
        return set(filtered_data.index)
