from typing import Set

from TARAVisualize import st
from TARAVisualize import TreeSubsetter


def generate_phylogeny(tree: TreeSubsetter, tree_image: str):
    st.title("Phylogeny")
    st.image(tree_image)
    tree.clean()
