import os
from plumbum import local
from typing import Set
from pathlib import Path

from TARAVisualize import ete3


class TreeSubsetter:
    def __init__(self, tree_path: Path):
        self.tree = ete3.Tree(tree_path.read_text())
        self.tmp_tree = os.path.join(os.path.dirname(__file__), "tmp-tree.newick")
        self.tmp_png = os.path.join(os.path.dirname(__file__), "tmp.png")

    def prune(self, ids: Set[str]) -> str:
        tree = self.tree.copy()
        if len(ids) > 0:
            ids = [_id for _id in ids if _id in tree.get_leaf_names()]
            tree.prune(ids)
        tree.write(features=[], outfile=self.tmp_tree)
        local[os.path.join(os.path.dirname(__file__), "render_tree.py")][self.tmp_tree, self.tmp_png]()
        return self.tmp_png

    def clean(self):
        if os.path.exists(self.tmp_tree):
            os.remove(self.tmp_tree)
        if os.path.exists(self.tmp_png):
            os.remove(self.tmp_png)
