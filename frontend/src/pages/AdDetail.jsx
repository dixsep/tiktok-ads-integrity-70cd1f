import { useEffect, useState } from "react";
import { fetchAd, reviewAction } from "../api/client";
import { StatusBadge } from "../components/StatusBadge";

export function AdDetail({ adId, onActioned }) {
  const [ad, setAd] = useState(null);
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    fetchAd(adId).then(setAd).catch((e) => setError(e.message));
  }, [adId]);

  async function act(action) {
    setBusy(true);
    setError(null);
    try {
      await reviewAction(adId, action);
      onActioned();
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  if (error) return <p style={{ color: "crimson" }}>Error: {error}</p>;
  if (!ad) return <p>Loading ad…</p>;

  return (
    <div>
      <h2>
        {ad.headline} <StatusBadge status={ad.status} />
      </h2>
      <p>{ad.body}</p>
      <p>
        Landing: <code>{ad.landing_domain}</code> · risk{" "}
        {ad.risk_score?.toFixed(2)}
      </p>
      <h3>Reasons</h3>
      <ul>
        {(ad.reasons ?? []).map((r, i) => (
          <li key={i}>{r}</li>
        ))}
      </ul>
      <button disabled={busy} onClick={() => act("approve")}>
        Approve
      </button>{" "}
      <button disabled={busy} onClick={() => act("block")}>
        Block
      </button>
    </div>
  );
}
