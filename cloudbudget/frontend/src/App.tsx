import { useEffect, useState } from "react";

type CostItem = {
  service: string;
  monthly_cost: number;
};

export default function App() {
  const [costs, setCosts] = useState<CostItem[]>([]);

  useEffect(() => {
    const loadCosts = async () => {
      try {
        const loginRes = await fetch("http://localhost:8000/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username: "demo", password: "demo" }),
        });
        const loginData = await loginRes.json();
        const token = loginData?.access_token;
        if (!token) {
          setCosts([]);
          return;
        }

        const costsRes = await fetch("http://localhost:8000/api/v1/costs", {
          headers: { Authorization: `Bearer ${token}` },
        });
        const costsData = await costsRes.json();
        setCosts(costsData.items ?? []);
      } catch {
        setCosts([]);
      }
    };

    loadCosts();
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
