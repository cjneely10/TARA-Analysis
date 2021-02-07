import os

import concurrent.futures
from TARAVisualize import st
from TARAVisualize.loader.fastani import generate_fastani, filter_fastani
from TARAVisualize.loader.phylogeny import generate_phylogeny
from TARAVisualize.loader.repeats import generate_repeats, repeats_filter
from TARAVisualize.utils.data_cacher import DataCacher
from TARAVisualize.loader.header_and_sidebar import get_region_filterby_selection
from TARAVisualize.loader.distribution import distribution

# Paths to data files
FILE_DIR = os.path.dirname(__file__)
TAX_FILE = os.path.join(FILE_DIR, "data/tax-summary.tsv.gz")
FASTANI_FILE = os.path.join(FILE_DIR, "data/all-alex-v-alex.fastani.out.gz")
REPEATS_FILE = os.path.join(FILE_DIR, "data/repeats-summary.bylength.tsv.gz")
TREE_FILE = os.path.join(FILE_DIR, "data/COV80_TOPAZ_2021-01-25.nwk")
ID_MAPPING_FILE = os.path.join(FILE_DIR, "data/renamed-eukaryotic-mags.tsv")

# Instantiate parallelized data cacher
cache = DataCacher()

# Load all data into full dataframes
fastani, repeats, metadata, tree = cache.load([FASTANI_FILE, REPEATS_FILE, TAX_FILE, TREE_FILE])

# Get user filter selections
selected_mags = get_region_filterby_selection(metadata)

if selected_mags:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(tree.prune, selected_mags),
                   executor.submit(lambda: metadata[metadata.index.isin(selected_mags)]),
                   executor.submit(repeats_filter, repeats[repeats.index.isin(selected_mags)]),
                   executor.submit(filter_fastani, fastani, selected_mags)]
        # Load application components
        concurrent.futures.wait(futures)
        tree_path, metadata, filtered_repeats, fastani = (future.result() for future in futures)
        distribution(metadata)
        generate_fastani(fastani)
        generate_phylogeny(tree, tree_path)
        generate_repeats(filtered_repeats, repeats)

else:
    st.title("Select a region")
    generate_phylogeny(tree, tree.render(True), False)
