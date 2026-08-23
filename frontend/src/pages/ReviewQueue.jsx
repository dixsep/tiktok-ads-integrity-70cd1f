import { useEffect, useState } from "react";
import { fetchQueue } from "../api/client";
import { StatusBadge } from "../components/StatusBadge";

export function ReviewQueue({ onSelect }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;
    setLoading(true);
    fetchQueue("REVIEW")
      .then((data) => {
        if (active) setItems(data.items);
      })
      .catch((e) => active && setError(e.message))
      .finally(() => active && setLoading(false));
    return () => {
      active = false;
    };
  }, []);

  if (loading) return <p>Loading review queue…</p>;
  if (error) return <p style={{ color: "crimson" }}>Error: {error}</p>;
  if (items.length === 0) return <p>Queue is empty. 🎉</p>;

  return (
    <ul style={{ listStyle: "none", padding: 0 }}>
      {items.map((ad) => (
        <li
          key={ad.id}
          onClick={() => onSelect(ad.id)}
          style={{ cursor: "pointer", padding: 8, borderBottom: "1px solid #eee" }}
        >
          <StatusBadge status={ad.status} /> <strong>{ad.headline}</strong>{" "}
          <span style={{ color: "#888" }}>risk {ad.risk_score?.toFixed(2)}</span>
        </li>
      ))}
    </ul>
  );
}
