import os

import streamlit.components.v1 as components

parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "component-template/template/my_component/frontend/build")
_component_func = components.declare_component("my_component", path="TARA/Visualize/components/component-template/template/my_component/frontend/build")


def selectable_component(fig):
    return _component_func(spec=fig.to_json())
