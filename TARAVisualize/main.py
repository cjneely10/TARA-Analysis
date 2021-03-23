import concurrent.futures
import os

from TARAVisualize import st
from TARAVisualize.loader.distribution import distribution
from TARAVisualize.loader.fastani import generate_fastani, filter_fastani_aai
from TARAVisualize.loader.gene_clustering import generate_kegg_pca
from TARAVisualize.loader.header_and_sidebar import get_mags_list
from TARAVisualize.loader.phylogeny import generate_phylogeny
from TARAVisualize.loader.quality import generate_quality
from TARAVisualize.loader.repeats import generate_repeats, repeats_filter
from TARAVisualize.loader.taxonomy import get_taxonomy
from TARAVisualize.utils.data_cacher import DataCacher
from TARAVisualize.loader.download_selection import download_selected_mag_data

# Paths to data files
FILE_DIR = os.path.join(os.path.dirname(__file__), "data")
TAX_FILE = os.path.join(FILE_DIR, "tax-summary.tsv.gz")
FASTANI_FILE = os.path.join(FILE_DIR, "all-alex-v-alex.fastani.out.gz")
REPEATS_FILE = os.path.join(FILE_DIR, "repeats-summary.bylength.tsv.gz")
TREE_FILE = os.path.join(FILE_DIR, "COV80_TOPAZ_2021-01-25.nwk")
ID_MAPPING_FILE = os.path.join(FILE_DIR, "renamed-eukaryotic-mags.tsv")
BUSCO_N50_FILE = os.path.join(FILE_DIR, "busco-n50-summary.txt.gz")
KEGG_FILE = os.path.join(FILE_DIR, "kegg-counts.txt.gz")
KEGG_DETAILS = os.path.join(FILE_DIR, "kegg-summary-test.txt")
AAI_FILE = os.path.join(FILE_DIR, "aai_summary.tsv.gz")

# Load all data into full dataframes
fastani, repeats, metadata, tree, busco_n50, kegg_data, kegg_id_dict, aai_df = DataCacher().load(
    [FASTANI_FILE, REPEATS_FILE, TAX_FILE, TREE_FILE, BUSCO_N50_FILE, KEGG_FILE, KEGG_DETAILS,
     AAI_FILE])
# Get user filter selections
selected_mags = get_mags_list(metadata)

if selected_mags:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Filter data concurrently
        futures = [executor.submit(tree.prune, selected_mags),
                   executor.submit(lambda: metadata[metadata.index.isin(selected_mags)]),
                   executor.submit(repeats_filter, repeats[repeats.index.isin(selected_mags)]),
                   executor.submit(filter_fastani_aai, fastani, selected_mags),
                   executor.submit(lambda: busco_n50[busco_n50.index.isin(selected_mags)]),
                   executor.submit(lambda: kegg_data[kegg_data.index.isin(selected_mags)]),
                   executor.submit(filter_fastani_aai, aai_df, selected_mags)]
        concurrent.futures.wait(futures)
        # Get filtered data from thread pool
        tree_path, metadata, filtered_repeats, fastani, busco_n50, kegg_data, aai_df = \
            (future.result() for future in futures)
        # Load application components to page
        download_selected_mag_data([busco_n50, filtered_repeats.fillna(0), metadata.fillna("N/A")])
        generate_quality(busco_n50)
        generate_fastani(fastani, aai_df)
        generate_phylogeny(tree, tree_path)
        generate_repeats(filtered_repeats, repeats)
        distribution(metadata)
        get_taxonomy(metadata)
        generate_kegg_pca(kegg_data)

else:
    st.title("Select a filter")
    generate_phylogeny(tree, tree.render(True), False)
