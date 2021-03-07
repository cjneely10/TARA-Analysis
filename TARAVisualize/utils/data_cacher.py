import concurrent.futures
from typing import List, Tuple

from TARAVisualize import st
from TARAVisualize.utils.caching_functions import *


class DataCacher:
    @st.cache
    def load(self, file_list: List[str]) -> Tuple:
        """
        Load all internal data into proper parsable formats, in memory
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for i, function in enumerate((load_fastani_data, load_repeats_data, load_taxonomy, load_tree,
                                          load_quality, load_kegg, load_kegg_details)):
                futures.append(executor.submit(function, Path(file_list[i]).resolve()))
            concurrent.futures.wait(futures)
            return tuple((future.result() for future in futures))
