import React, { useEffect } from "../../component-template/template/my_component/frontend/node_modules/react"
import { withStreamlitConnection, Streamlit, ComponentProps } from "../../component-template/template/my_component/frontend/node_modules/streamlit-component-lib"
import Plot from "../../component-template/template/my_component/frontend/node_modules/react-plotly.js"

function MyComponent(props: ComponentProps) {
  useEffect(() => Streamlit.setFrameHeight())

  const handleSelected = function (eventData: any) {
    Streamlit.setComponentValue(
      eventData.points.map((p: any) => {
        return { index: p.pointIndex, x: p.x, y: p.y }
      })
    )
  }

  const { data, layout, frames, config } = JSON.parse(props.args.spec)

  return (
    <Plot
      data={data}
      layout={layout}
      frames={frames}
      config={config}
      onSelected={handleSelected}
    />
  )
}

export default withStreamlitConnection(MyComponent)