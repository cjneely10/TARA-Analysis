from typing import Set

from TARAVisualize import st
from TARAVisualize import plt
from TARAVisualize import TreeSubsetter


def generate_phylogeny(tree: TreeSubsetter, selected_mags: Set[str]):
    st.title("Phylogeny")
    st.image(tree.prune(selected_mags))
    tree.clean()
