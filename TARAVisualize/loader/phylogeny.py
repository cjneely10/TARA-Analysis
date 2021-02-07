from TARAVisualize import st
from TARAVisualize import TreeSubsetter


def generate_phylogeny(tree: TreeSubsetter, tree_image: str, display_title: bool = True):
    if display_title:
        st.title("Phylogeny")
    st.image(tree_image)
    tree.clean()
