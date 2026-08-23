const COLORS = {
  PENDING: "#9ca3af",
  REVIEW: "#f59e0b",
  APPROVED: "#10b981",
  BLOCKED: "#ef4444",
};

export function StatusBadge({ status }) {
  return (
    <span
      style={{
        background: COLORS[status] ?? "#9ca3af",
        color: "white",
        padding: "2px 8px",
        borderRadius: 999,
        fontSize: 12,
      }}
    >
      {status}
    </span>
  );
}
