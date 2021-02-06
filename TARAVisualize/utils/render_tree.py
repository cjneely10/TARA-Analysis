#!/usr/bin/env python
import sys
import ete3

circular_style = ete3.TreeStyle()
circular_style.mode = "c"
circular_style.scale = 20
circular_style.show_branch_support = True
circular_style.show_branch_support = True
circular_style.arc_start = 180  # 0 degrees = 3 o'clock
circular_style.arc_span = 180

tree = ete3.Tree(sys.argv[1])

tree.render(sys.argv[2], tree_style=circular_style, w=800, units="px")
