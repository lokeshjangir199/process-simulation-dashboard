import Plot from "react-plotly.js";

export default function AdsorptionPlot({ t, y }) {
  return (
    <Plot
      data={[{ x: t, y, type: "scatter" }]}
      layout={{
        title: "CO₂ Adsorbed vs Time",
        xaxis: { title: "Time [min]" },
        yaxis: { title: "CO₂ adsorbed [mol]" }
      }}
    />
  );
}
