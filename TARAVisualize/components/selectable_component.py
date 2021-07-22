import os

import streamlit.components.v1 as components

build_dir = os.path.join(os.path.dirname(__file__), "build")
_component_func = components.declare_component("my_component", path=build_dir)


def selectable_component(fig):
    return _component_func(spec=fig.to_json())
