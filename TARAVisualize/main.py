import os

from TARAVisualize import st
from TARAVisualize.utils.data_cacher import DataCacher
from TARAVisualize.components.header_and_sidebar import get_region_filterby_selection
from TARAVisualize.components.taxonomy import generate_taxonomy_display

st.set_option('deprecation.showPyplotGlobalUse', False)

FILE_DIR = os.path.dirname(__file__)
TAX_FILE = os.path.join(FILE_DIR, "data/tax-summary.tsv.gz")
FASTANI_FILE = os.path.join(FILE_DIR, "data/all-alex-v-alex.fastani.out.gz")
REPEATS_FILE = os.path.join(FILE_DIR, "data/repeats-summary.bylength.tsv.gz")
TREE_FILE = os.path.join(FILE_DIR, "data/COV80_TOPAZ_2021-01-25.nwk")

cache = DataCacher()

fastani, repeats, metadata, tree = cache.load([FASTANI_FILE, REPEATS_FILE, TAX_FILE, TREE_FILE])

filter_option, selected_mags_df = get_region_filterby_selection(metadata)

if selected_mags_df:
    metadata, = cache.filter(selected_mags_df, [metadata])
    generate_taxonomy_display(metadata, filter_option)

