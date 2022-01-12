import os
import streamlit.components.v1 as components

_component_func = components.declare_component("my_component", path="TARAVisualize/components/component-template"
                                                                    "/template/my_component/frontend/build")


def selectable_component(fig):
    return _component_func(spec=fig.to_json())
