import os

from Bio import Phylo

from TARAVisualize import st
from TARAVisualize.utils.data_cacher import DataCacher

st.set_option('deprecation.showPyplotGlobalUse', False)

FILE_DIR = os.path.dirname(__file__)
TAX_FILE = os.path.join(FILE_DIR, "data/tax-summary.tsv.gz")
FASTANI_FILE = os.path.join(FILE_DIR, "data/all-alex-v-alex.fastani.out.gz")
REPEATS_FILE = os.path.join(FILE_DIR, "data/repeats-summary.bylength.tsv.gz")
TREE_FILE = os.path.join(FILE_DIR, "data/COV80_TOPAZ_2021-01-25.nwk")

TAX_LEVELS = ("kingdom", "clade", "phylum", "class", "subclass", "order", "family", "genus", "species")
TITLE = "TARA oceans data visualizer"
FILTER_BY_OPTIONS = ("size_fraction", "depth")

fastani, repeats, taxonomy, tree = DataCacher().load([FASTANI_FILE, TAX_FILE, REPEATS_FILE, TREE_FILE])

st.write(repeats)

subsetted_tree = tree.prune(["SPO-all-DCM-0-8-5-00_bin-566", "NAO-all-MIX-0-8-5-00_bin-161"])

st.pyplot(Phylo.draw(subsetted_tree))

