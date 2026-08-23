import { useEffect, useState } from "react";

const BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

export function Analytics() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${BASE}/analytics/summary?days=7`)
      .then((r) => r.json())
      .then(setData)
      .catch((e) => setError(e.message));
  }, []);

  if (error) return <p style={{ color: "crimson" }}>Error: {error}</p>;
  if (!data) return <p>Loading analytics…</p>;

  return (
    <div>
      <h2>Last {data.window_days} days</h2>

      <h3>Decisions</h3>
      <table>
        <tbody>
          {data.decision_counts.map((row) => (
            <tr key={row.status}>
              <td>{row.status}</td>
              <td>{row.n}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Top rule hits</h3>
      <table>
        <tbody>
          {data.top_rule_hits.map((row) => (
            <tr key={row.rule_id}>
              <td>{row.rule_id}</td>
              <td>{row.n}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Riskiest advertisers</h3>
      <table>
        <tbody>
          {data.advertiser_risk.map((row) => (
            <tr key={row.advertiser_id}>
              <td>#{row.advertiser_id}</td>
              <td>avg {row.avg_risk}</td>
              <td>block rate {row.block_rate}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
