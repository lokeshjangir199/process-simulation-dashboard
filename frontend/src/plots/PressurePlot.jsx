import Plot from "react-plotly.js";

export default function PressurePlot({ z, dp }) {
  return (
    <Plot
      data={[{ x: z, y: dp, type: "scatter" }]}
      layout={{
        title: "Pressure Drop vs Bed Length",
        xaxis: { title: "Bed length [m]" },
        yaxis: { title: "ΔP [bar]" }
      }}
    />
  );
}
