const BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";
const MODERATOR_KEY = import.meta.env.VITE_MODERATOR_KEY ?? "dev-moderator-key";

async function http(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, options);
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? `request failed (${res.status})`);
  }
  return res.status === 204 ? null : res.json();
}

export function fetchQueue(status = "REVIEW") {
  return http(`/moderation/queue?status=${status}`);
}

export function fetchAd(adId) {
  return http(`/moderation/ads/${adId}`);
}

export function reviewAction(adId, action) {
  // action is "approve" | "block"
  return http(`/review/ads/${adId}/${action}`, {
    method: "POST",
    headers: { "X-Moderator-Key": MODERATOR_KEY },
  });
}
