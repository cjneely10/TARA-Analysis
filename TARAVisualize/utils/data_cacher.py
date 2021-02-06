import concurrent.futures
from typing import List, Tuple, Set

from TARAVisualize import st
from TARAVisualize.utils.caching_functions import *


class DataCacher:
    def __init__(self, id_mapping_file: str, max_threads: int = 4):
        """ Create DataCacher using streamlit's internal caching system

        :param max_threads: Max allowable concurrent processes
        """
        self.max_threads = max_threads
        self.id_mappings = {}
        for line in open(id_mapping_file, "r"):
            line = line.rstrip("\r\n").split("\t")
            self.id_mappings[line[0]] = line[1]

    @st.cache
    def load(self, file_list: List[str]) -> Tuple:
        """
        Load all internal data into proper parseable formats, in memory
        """
        with concurrent.futures.ThreadPoolExecutor(self.max_threads) as executor:
            futures = []
            for i, function in enumerate((load_fastani_data, load_repeats_data,
                                          load_taxonomy, load_tree)):
                futures.append(executor.submit(function, Path(file_list[i]).resolve(), self.id_mappings))
            concurrent.futures.wait(futures)
            return tuple((future.result() for future in futures))

    @staticmethod
    @st.cache
    def filter(ids_list: Set[str], data_frames: List[pd.DataFrame]):
        with concurrent.futures.ThreadPoolExecutor(len(data_frames)) as executor:
            futures = []
            for data_frame in data_frames:
                futures.append(executor.submit(lambda : data_frame[data_frame.index.isin(ids_list)]))
            concurrent.futures.wait(futures)
            return [future.result() for future in futures]
