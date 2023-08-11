import os
import random
import string
from pathlib import Path
from typing import Set

from plumbum import local, CommandNotFound

from TARAVisualize import ete3


class TreeSubsetter:
    def __init__(self, tree_path: Path):
        self.tree_path = tree_path
        self.tree = ete3.Tree(tree_path.read_text())
        self.id =  ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=20))
        self.tmp_tree = os.path.join("~", f"{self.id}.newick")
        self.tmp_png = os.path.join("~", f"{self.id}.png")

    def prune(self, ids: Set[str]) -> str:
        self.clean()
        tree = self.tree.copy()
        if len(ids) > 5:
            tree.prune([_id for _id in ids if _id in tree.get_leaf_names()], preserve_branch_length=True)
        tree.write(features=[], outfile=self.tmp_tree)
        return self.render()

    def clean(self):
        if os.path.exists(self.tmp_tree):
            os.remove(self.tmp_tree)
        if os.path.exists(self.tmp_png):
            os.remove(self.tmp_png)

    def render(self, full: bool = False) -> str:
        if full:
            self.tree.write(features=[], outfile=self.tmp_tree)
        try:
            local["/home/appuser/venv/bin/python"][os.path.join(os.path.dirname(__file__), "render_tree.py"), self.tmp_tree, self.tmp_png]()
        except:
            local["python"][os.path.join(os.path.dirname(__file__), "render_tree.py"), self.tmp_tree, self.tmp_png]()
        return self.tmp_png

    def __del__(self):
        self.clean()
