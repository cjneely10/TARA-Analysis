import os
import streamlit.components.v1 as components

build = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "component-template/template/my_component/frontend/build")
_component_func = components.declare_component("my_component", path=build)


def selectable_component(fig):
    return _component_func(spec=fig.to_json())
