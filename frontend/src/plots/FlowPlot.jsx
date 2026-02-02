import Plot from "react-plotly.js";

export default function FlowPlot({ t, y }) {
  return (
    <Plot
      data={[{ x: t, y, type: "scatter" }]}
      layout={{
        title: "Outlet CO₂ Molar Flow (Envelope)",
        xaxis: { title: "Time [min]" },
        yaxis: { title: "CO₂ molar flow [mol/min]" }
      }}
    />
  );
}
