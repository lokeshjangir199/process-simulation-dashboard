export async function runSimulation(payload) {
  const res = await fetch(`${import.meta.env.VITE_API_URL}/simulate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  return res.json();
}
