const headers = { "X-Tenant-ID": "1" }

async function getJson(url: string) {
  try {
    const res = await fetch(url, { cache: "no-store", headers })
    if (!res.ok) return null
    return await res.json()
  } catch {
    return null
  }
}

export default async function Home() {
  const summary = await getJson("http://api:8000/api/v1/costs/summary")
  const budget = await getJson("http://api:8000/api/v1/budgets")
  const prediction = await getJson("http://api:8000/api/v1/predictions/1")

  return (
    <main style={{ padding: 24, fontFamily: "sans-serif" }}>
      <h1>CloudBudget 2.0 Dashboard</h1>
      <h3>Cost summary</h3>
      <pre>{JSON.stringify(summary ?? { message: "No data" }, null, 2)}</pre>
      <h3>Budget status</h3>
      <pre>{JSON.stringify(budget ?? { message: "No budget configured" }, null, 2)}</pre>
      <h3>Forecast</h3>
      <pre>{JSON.stringify(prediction ?? { message: "Forecast unavailable" }, null, 2)}</pre>
    </main>
  )
}
