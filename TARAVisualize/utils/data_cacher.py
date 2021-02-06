from typing import List
from pathlib import Path
import concurrent.futures

from TARAVisualize import np
from TARAVisualize import pd
from TARAVisualize import st
from TARAVisualize import TreeSubsetter


class DataCacher:
    def __init__(self, max_threads: int = 4):
        """ Create DataCacher using streamlit's internal caching system

        :param max_threads: Max allowable concurrent processes
        """
        self.max_threads = max_threads

    @st.cache
    def load(self, file_list: List[str]) -> List:
        """
        Load all internal data into proper parseable formats, in memory
        """
        with concurrent.futures.ThreadPoolExecutor(self.max_threads) as executor:
            futures = []
            for i, function in enumerate((DataCacher.load_fastani_data, DataCacher.load_repeats_data,
                                          DataCacher.load_taxonomy, DataCacher.load_tree)):
                futures.append(executor.submit(function, Path(file_list[i]).resolve()))
            concurrent.futures.wait(futures)
            return [future.result() for future in futures]

    @staticmethod
    def load_taxonomy(data_file: Path) -> pd.DataFrame:
        """ Load taxonomy data into pandas data frame

        :param data_file: Path to data file
        :return: Loaded pandas dataframe
        """
        return pd.read_csv(data_file, delimiter="\t", na_values=".", index_col=0)

    @staticmethod
    def load_fastani_data(data_file: Path) -> pd.DataFrame:
        """ Load FastANI data into nxn DataFrame of comparison data

        :param data_file: FastANI results file
        :return:
        """
        fastani_a = pd.read_csv(data_file, delimiter="\t", header=0,
                                names=["alexander1", "alexander2", "pid", "r1", "r2"])
        record_ids = list(set(fastani_a["alexander1"]))
        as_dict = {(k1, k2): p for k1, k2, p in zip(fastani_a.alexander1, fastani_a.alexander2, fastani_a.pid)}
        out = np.full((len(record_ids), len(record_ids)), 70.0, dtype="float32")
        for i, f1_name in enumerate(record_ids):
            for j, f2_name in enumerate(record_ids):
                if (f1_name, f2_name) in as_dict.keys():
                    value = float(as_dict[(f1_name, f2_name)])
                    if value > out[i, j]:
                        out[i, j] = value
        out_df = pd.DataFrame(out, index=record_ids, columns=record_ids)
        return out_df

    @staticmethod
    def load_repeats_data(file: Path) -> pd.DataFrame:
        """ Load repeats file results into pandas

        :param file: Path to file
        :return:
        """
        return pd.read_csv(file, delimiter="\t", index_col=0)

    @staticmethod
    def load_tree(file: Path) -> TreeSubsetter:
        return TreeSubsetter(file)
