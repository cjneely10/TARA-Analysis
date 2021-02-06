// Adopted (copied) from https://dev.to/andfanilo/streamlit-components-scatterplot-with-selection-using-plotly-js-3d7n
// Thank you!

// @ts-ignore
import React, { useEffect } from "react"
// @ts-ignore
import { withStreamlitConnection, Streamlit, ComponentProps } from "streamlit-component-lib"
// @ts-ignore
import Plot from "react-plotly.js"

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