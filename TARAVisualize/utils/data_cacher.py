import concurrent.futures
from typing import List, Tuple

from TARAVisualize import st
from TARAVisualize.utils.caching_functions import *


@st.cache_data
def load(file_list: List[str]) -> Tuple:
    """
    Load all internal data into proper parsable formats, in memory
    """
    fxns = (load_fastani_data, load_repeats_data, load_taxonomy, load_tree,
            load_quality, load_aai_data)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for file, function in zip(file_list, fxns):
            futures.append(executor.submit(function, Path(file).resolve()))
        concurrent.futures.wait(futures)
        return tuple((future.result() for future in futures))
