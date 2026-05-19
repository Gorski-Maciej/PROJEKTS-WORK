import { useEffect, useState } from 'react';

interface Cost { id: number; service: string; amount: number; date: string; }

export default function App() {
  const [costs, setCosts] = useState<Cost[]>([]);
  useEffect(() => {
    fetch('http://localhost:8100/api/v1/costs')
      .then(r => r.json()).then(setCosts).catch(console.error);
  }, []);
  return (
    <div style={{ padding: 20 }}>
      <h1>CloudBudget Dashboard</h1>
      <ul>{costs.map(c => <li key={c.id}>{c.service}: ${c.amount}</li>)}</ul>
    </div>
  );
}
