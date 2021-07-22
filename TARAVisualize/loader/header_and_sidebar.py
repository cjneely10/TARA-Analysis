from typing import Set

from TARAVisualize import pd
from TARAVisualize import st
from TARAVisualize.utils.tax_levels import tax_levels


def get_mags_list(metadata: pd.DataFrame) -> Set[str]:
    title = "TOPAviZ"
    # Create simple layout
    st.sidebar.write(title)
    st.sidebar.write("Filter by")
    # Allow user to select which subregions to compare
    taxonomy_selection = st.sidebar.selectbox("Taxonomic Level", ["all", *tax_levels])
    filtered_data = metadata

    to_filter = []
    filter_used = False

    if len(to_filter) > 0:
        filtered_data = filtered_data[eval("&".join([('filtered_data["%s"].isin(%s)' % (label, selection))
                                                     for label, selection in to_filter]))]
        filter_used = True

    if taxonomy_selection != "all":
        levels_selection = st.sidebar.multiselect("Select Assignment",
                                                  sorted(list(set(filtered_data[taxonomy_selection].dropna()))))
        filtered_data = filtered_data[filtered_data[taxonomy_selection].isin(levels_selection)]
        filter_used = True
        # Show dataframe on menu for selection
    regions_selection = st.sidebar.multiselect("Regions", sorted(list(set(metadata.region))))
    size_fraction_selection = st.sidebar.multiselect("Size Fraction",
                                                     sorted(list(set(metadata.size_fraction)),
                                                            key=lambda val: int(val.split("-")[0])))
    depth_selection = st.sidebar.multiselect("Depth", sorted(list(set(metadata.depth))))
    if len(regions_selection) + len(size_fraction_selection) + len(depth_selection) > 0:
        # Display filtered results as table
        if len(regions_selection) > 0:
            to_filter.append(("region", "regions_selection"))
        if len(size_fraction_selection) > 0:
            to_filter.append(("size_fraction", "size_fraction_selection"))
        if len(depth_selection) > 0:
            to_filter.append(("depth", "depth_selection"))
    st.sidebar.write(f"{len(filtered_data)} MAGs selected")
    if filter_used:
        return set(filtered_data.index)
