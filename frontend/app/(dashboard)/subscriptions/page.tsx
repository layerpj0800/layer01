'use client';

import { useEffect, useState } from 'react';

interface Plan {
  id: number;
  price: number;
}

export default function SubscriptionPage() {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('/api/v1/subscriptions/plans/1')
      .then((res) => res.json())
      .then(setPlans)
      .catch(() => setError('Failed to load plans'));
  }, []);

  const purchase = async (planId: number) => {
    const res = await fetch('/api/v1/subscriptions/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ plan_id: planId }),
    });
    if (!res.ok) {
      alert('Failed to purchase');
      return;
    }
    const data = await res.json();
    await fetch('/api/v1/subscriptions/verify-payment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ merchant_uid: data.merchant_uid }),
    });
    alert('Subscription active');
  };

  return (
    <div>
      <h1 className="text-xl mb-4">Plans</h1>
      {error && <p>{error}</p>}
      <ul>
        {plans.map((p) => (
          <li key={p.id} className="mb-2">
            {p.price} <button onClick={() => purchase(p.id)}>Buy</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
