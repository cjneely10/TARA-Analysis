#!/usr/bin/env python
import sys
import ete3

assert len(sys.argv) == 3

# Render as half-circle
circular_style = ete3.TreeStyle()
circular_style.mode = "c"
circular_style.scale = 20
circular_style.show_branch_support = True
circular_style.show_branch_support = True
circular_style.arc_start = 180
circular_style.arc_span = 270
# Generate tree
tree = ete3.Tree(sys.argv[1])
# Render as circular plot
tree.render(sys.argv[2], tree_style=circular_style, w=800, units="px")
