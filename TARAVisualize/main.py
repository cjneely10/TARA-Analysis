import os

from TARAVisualize import st
from TARAVisualize.loader.fastani import generate_fastani
from TARAVisualize.loader.phylogeny import generate_phylogeny
from TARAVisualize.loader.repeats import generate_repeats
from TARAVisualize.utils.data_cacher import DataCacher
from TARAVisualize.loader.header_and_sidebar import get_region_filterby_selection
from TARAVisualize.loader.taxonomy import generate_taxonomy_display

FILE_DIR = os.path.dirname(__file__)
TAX_FILE = os.path.join(FILE_DIR, "data/tax-summary.tsv.gz")
FASTANI_FILE = os.path.join(FILE_DIR, "data/all-alex-v-alex.fastani.out.gz")
REPEATS_FILE = os.path.join(FILE_DIR, "data/repeats-summary.bylength.tsv.gz")
TREE_FILE = os.path.join(FILE_DIR, "data/COV80_TOPAZ_2021-01-25.nwk")
ID_MAPPING_FILE = os.path.join(FILE_DIR, "data/renamed-eukaryotic-mags.tsv")

cache = DataCacher(ID_MAPPING_FILE)

fastani, repeats, metadata, tree = cache.load([FASTANI_FILE, REPEATS_FILE, TAX_FILE, TREE_FILE])

filter_option, selected_mags = get_region_filterby_selection(metadata)

if selected_mags:
    metadata, repeats = cache.filter(selected_mags, [metadata, repeats])
    generate_taxonomy_display(metadata, filter_option)
    generate_fastani(fastani, selected_mags)
    generate_phylogeny(tree, selected_mags)
    generate_repeats(repeats)

else:
    st.title("Select a region")

