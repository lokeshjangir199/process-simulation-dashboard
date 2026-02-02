import { useState } from "react";
import { runSimulation } from "./api";

import PressurePlot from "./plots/PressurePlot";
import AdsorptionPlot from "./plots/AdsorptionPlot";
import FlowPlot from "./plots/FlowPlot";
import PPMPlot from "./plots/PPMPlot";

export default function App() {
  const [inputs, setInputs] = useState({
    flow_ml_min: 2000,
    P_in_atm: 1.0,
    T_K: 298.15,
    eps: 0.30,
    rho_s_L: 0.60,
    L_m: 0.50,
    D_bed_m: 0.08
  });

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  function update(name, value) {
    setInputs({ ...inputs, [name]: Number(value) });
  }

  async function run() {
    setLoading(true);
    const res = await runSimulation(inputs);
    setData(res);
    setLoading(false);
  }

  return (
    <div style={styles.page}>
      {/* LEFT SIDEBAR */}
      <div style={styles.sidebar}>
        <h2 style={styles.sidebarTitle}>Inputs</h2>

        <div style={styles.inputBox}>
          {Object.entries(inputs).map(([key, val]) => (
            <div key={key} style={styles.inputRow}>
              <label>{key}</label>
              <input
                type="number"
                value={val}
                onChange={e => update(key, e.target.value)}
                style={{ width: "110px" }}
              />
            </div>
          ))}
        </div>

        <button style={styles.runBtn} onClick={run} disabled={loading}>
          {loading ? "Running..." : "Simulate"}
        </button>

        {/* intentional empty space below */}
        <div style={{ flexGrow: 1 }} />
      </div>

      {/* RIGHT MAIN AREA */}
      <div style={styles.main}>
        {data ? (
          <div style={styles.grid}>
            <div style={styles.card}><PressurePlot z={data.z} dp={data.pressure} /></div>
            <div style={styles.card}><AdsorptionPlot t={data.time_ads} y={data.co2_adsorbed} /></div>
            <div style={styles.card}><FlowPlot t={data.time_flow} y={data.co2_outlet_flow} /></div>
            <div style={styles.card}><PPMPlot t={data.time_ppm} y={data.co2_outlet_ppm} /></div>
          </div>
        ) : (
          <div style={styles.placeholder}>
            Run a simulation to view results
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  page: {
    display: "flex",
    height: "100vh",
    background: "#03294e",
    fontFamily: "JetBrains Mono, monospace"
  },

  /* LEFT PANEL */
  sidebar: {
    width: "280px",
    background: "#0f172a",
    color: "#f8f8f9",
    padding: "20px",
    display: "flex",
    flexDirection: "column"
  },
  sidebarTitle: {
    marginBottom: "15px",
    fontSize: "25px",
    display: "flex",
    justifyContent: "center"
  
  },
  inputBox: {
    background: "#020617",
    padding: "30px",
    borderRadius: "15px"
  },
  inputRow: {
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  marginBottom: "10px",
  fontSize: "15px",
  gap: "10px"
},
  runBtn: {
    marginTop: "15px",
    padding: "10px",
    borderRadius: "6px",
    border: "none",
    background: "#d5dbff",
    color: "#000000",
    fontWeight: "bold",
    cursor: "pointer"
  },

  /* RIGHT PANEL */
  main: {
    flexGrow: 1,
    padding: "20px",
    overflowY: "auto"
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gridTemplateRows: "1fr 1fr",
    gap: "20px",
    height: "100%"
  },
  card: {
    background: "#f3f3f3",
    borderRadius: "10px",
    padding: "10px",
    boxShadow: "0 4px 12px rgba(0,0,0,0.08)"
  },
  placeholder: {
    height: "100%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "18px",
    color: "#64748b"
  }
};
