from pathlib import Path
import concurrent.futures
from typing import List, Tuple, Set

from TARAVisualize import np
from TARAVisualize import pd
from TARAVisualize import st
from TARAVisualize import TreeSubsetter


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
            for i, function in enumerate((self.load_fastani_data, self.load_repeats_data,
                                          self.load_taxonomy, self.load_tree)):
                futures.append(executor.submit(function, Path(file_list[i]).resolve()))
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

    def load_taxonomy(self, data_file: Path) -> pd.DataFrame:
        """ Load taxonomy data into pandas data frame

        :param data_file: Path to data file
        :return: Loaded pandas dataframe
        """
        tax_df = pd.read_csv(data_file, delimiter="\t", na_values=".", index_col=0, dtype="object")
        # return tax_df.rename(self.id_mappings)
        return tax_df

    def load_fastani_data(self, data_file: Path) -> pd.DataFrame:
        """ Load FastANI data into nxn DataFrame of comparison data

        :param data_file: FastANI results file
        :return:
        """
        fastani_a = pd.read_csv(data_file, delimiter="\t", header=0,
                                names=["alexander1", "alexander2", "pid", "r1", "r2"])
        # record_ids = [self.id_mappings[val] for val in set(fastani_a["alexander1"])]
        record_ids = set(fastani_a["alexander1"])
        as_dict = {(k1, k2): p for k1, k2, p in zip(fastani_a.alexander1, fastani_a.alexander2, fastani_a.pid)}
        # as_dict = {(self.id_mappings[k1], self.id_mappings[k2]): p for k1, k2, p in zip(fastani_a.alexander1, fastani_a.alexander2, fastani_a.pid)}
        out = np.full((len(record_ids), len(record_ids)), 70.0, dtype="float32")
        for i, f1_name in enumerate(record_ids):
            for j, f2_name in enumerate(record_ids):
                if (f1_name, f2_name) in as_dict.keys():
                    value = float(as_dict[(f1_name, f2_name)])
                    if value > out[i, j]:
                        out[i, j] = value
        return pd.DataFrame(out, index=record_ids, columns=record_ids, dtype="float32")

    def load_repeats_data(self, file: Path) -> pd.DataFrame:
        """ Load repeats file results into pandas

        :param file: Path to file
        :return:
        """
        repeats_df = pd.read_csv(file, delimiter="\t", index_col=0, dtype="object")
        # return repeats_df.rename(self.id_mappings)
        for i in repeats_df.columns:
            repeats_df[i] = repeats_df[i].apply(lambda _: float(_))
        return repeats_df

    def load_tree(self, file: Path) -> TreeSubsetter:
        """ Read in newick file into subsettable tree

        :param file: Path to newick file
        :return: Tree with ability to respond to subset requests
        """
        return TreeSubsetter(file)
