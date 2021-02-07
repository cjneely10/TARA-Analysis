from pathlib import Path

from TARAVisualize import np
from TARAVisualize import pd
from TARAVisualize.utils.tree_subsetter import TreeSubsetter


def load_taxonomy(data_file: Path) -> pd.DataFrame:
    """ Load taxonomy data into pandas data frame

    :param data_file: Path to data file
    :return: Loaded pandas dataframe
    """
    tax_df = pd.read_csv(data_file, delimiter="\t", na_values=".", index_col=0, dtype="object")
    return tax_df


def load_fastani_data(data_file: Path) -> pd.DataFrame:
    """ Load FastANI data into nxn DataFrame of comparison data

    :param data_file: FastANI results file
    :return:
    """
    fastani_a = pd.read_csv(data_file, delimiter="\t", header=0,
                            names=["alexander1", "alexander2", "pid", "r1", "r2"])
    record_ids = set(fastani_a["alexander1"])
    as_dict = {(k1, k2): p for k1, k2, p in zip(fastani_a.alexander1, fastani_a.alexander2, fastani_a.pid)}
    out = np.full((len(record_ids), len(record_ids)), 70.0, dtype="float32")
    for i, f1_name in enumerate(record_ids):
        for j, f2_name in enumerate(record_ids):
            if (f1_name, f2_name) in as_dict.keys():
                value = float(as_dict[(f1_name, f2_name)])
                if value > out[i, j]:
                    out[i, j] = value
    return pd.DataFrame(out, index=record_ids, columns=record_ids, dtype="float32")


def load_repeats_data(file: Path) -> pd.DataFrame:
    """ Load repeats file results into pandas

    :param file: Path to file
    :return:
    """
    repeats_df = pd.read_csv(file, delimiter="\t", index_col=0, dtype="object")
    for i in repeats_df.columns:
        repeats_df[i] = repeats_df[i].apply(lambda _: float(_))
    return repeats_df


def load_tree(file: Path) -> TreeSubsetter:
    """ Read in newick file into subsettable tree

    :param file: Path to newick file
    :return: Tree with ability to respond to subset requests
    """
    return TreeSubsetter(file)
