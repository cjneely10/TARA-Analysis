import streamlit.components.v1 as components

_component_func = components.declare_component(
    "my_component",
    url="http://localhost:3001",
)


def selectable_component(fig):
    return _component_func(spec=fig.to_json())
