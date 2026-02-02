import Plot from "react-plotly.js";

export default function PPMPlot({ t, y }) {
  return (
    <Plot
      data={[{ x: t, y, type: "scatter" }]}
      layout={{
        title: "Outlet CO₂ Mole Fraction (Envelope)",
        xaxis: { title: "Time [min]" },
        yaxis: { title: "CO₂ [ppm]" }
      }}
    />
  );
}
