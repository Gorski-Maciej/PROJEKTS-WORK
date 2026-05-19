import { useEffect, useState } from "react";

type CostItem = {
  service: string;
  monthly_cost: number;
};

export default function App() {
  const [costs, setCosts] = useState<CostItem[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/costs", {
      headers: { Authorization: "Bearer demo" }
    })
      .then((res) => res.json())
      .then((data) => setCosts(data.items ?? []))
      .catch(() => setCosts([]));
  }, []);

  return (
    <main>
      <h1>CloudBudget Dashboard</h1>
      <ul>
        {costs.map((item) => (
          <li key={item.service}>
            {item.service}: ${item.monthly_cost}
          </li>
        ))}
      </ul>
    </main>
  );
}
