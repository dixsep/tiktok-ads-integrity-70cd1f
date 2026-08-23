import { useState } from "react";
import { ReviewQueue } from "./pages/ReviewQueue";
import { AdDetail } from "./pages/AdDetail";

export default function App() {
  const [selected, setSelected] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  return (
    <div style={{ maxWidth: 720, margin: "2rem auto", fontFamily: "system-ui" }}>
      <h1>Ads Integrity · Review</h1>
      {selected === null ? (
        <ReviewQueue key={refreshKey} onSelect={setSelected} />
      ) : (
        <>
          <button onClick={() => setSelected(null)}>← Back to queue</button>
          <AdDetail
            adId={selected}
            onActioned={() => {
              setSelected(null);
              setRefreshKey((k) => k + 1);
            }}
          />
        </>
      )}
    </div>
  );
}
