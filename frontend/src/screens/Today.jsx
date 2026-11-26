import { useEffect, useState } from "react";
import { fetchToday } from "../api.js";

const STATUS_LABEL = {
  taken: "Taken",
  skipped: "Skipped",
  pending: "Due",
};

function formatTime(iso) {
  return new Date(iso).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

export default function Today() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchToday().then(setData).catch((e) => setError(e.message));
  }, []);

  if (error) return <p className="notice">Could not load today. {error}</p>;
  if (!data) return <p className="notice">Loading today…</p>;

  const readings = Object.values(data.latest);

  return (
    <section>
      <p className="eyebrow">Today · {data.date}</p>
      <h1>Good morning, Maya</h1>

      <h2>Medicines</h2>
      <ul className="list">
        {data.doses.map((d) => (
          <li key={`${d.medicine}-${d.due}`} className={`card dose ${d.status}`}>
            <div>
              <strong>{d.medicine}</strong> {d.dose}
              <div className="muted">Due {d.due} UTC</div>
              {d.reason && <div className="muted">Reason: {d.reason}</div>}
            </div>
            <span className="badge">{STATUS_LABEL[d.status] || d.status}</span>
          </li>
        ))}
      </ul>

      <h2>Latest readings</h2>
      <ul className="list">
        {readings.map((r) => (
          <li key={r.label} className="card reading">
            <span>{r.label}</span>
            <strong>
              {r.value} {r.unit}
            </strong>
            <span className="muted">{formatTime(r.measured_at)}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
