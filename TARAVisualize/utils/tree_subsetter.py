import tempfile
from typing import List
from pathlib import Path

import ete3
from Bio import Phylo

from TARAVisualize import Tree
from TARAVisualize import st


class TreeSubsetter:
    def __init__(self, tree_path: Path):
        self.tree = ete3.Tree(tree_path.read_text())

    @st.cache
    def prune(self, ids: List[str]) -> Tree:
        tree = self.tree.copy()
        if len(ids) > 0:
            tree.prune(ids)
        with tempfile.NamedTemporaryFile() as file:
            tree.write(features=[], outfile=file.name)
            tree = Phylo.read(file.name, "newick")
            tree.ladderize()
            return tree
