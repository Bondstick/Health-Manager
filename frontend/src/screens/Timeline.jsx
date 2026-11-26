import { useEffect, useState } from "react";
import { fetchTimeline } from "../api.js";

// Simple line chart drawn in SVG, so the app needs no chart library.
function LineChart({ points, unit }) {
  if (points.length < 2) return <p className="muted">Not enough readings to draw a chart.</p>;

  const width = 320;
  const height = 160;
  const pad = 24;
  const values = points.map((p) => p.value);
  const min = Math.min(...values) - 2;
  const max = Math.max(...values) + 2;

  const x = (i) => pad + (i * (width - 2 * pad)) / (points.length - 1);
  const y = (v) => height - pad - ((v - min) * (height - 2 * pad)) / (max - min || 1);

  const path = points.map((p, i) => `${i === 0 ? "M" : "L"} ${x(i)} ${y(p.value)}`).join(" ");

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      role="img"
      aria-label={`Line chart of ${points.length} readings, from ${values[0]} to ${values[values.length - 1]} ${unit}`}
      className="chart"
    >
      <path d={path} fill="none" stroke="#0B5563" strokeWidth="3" />
      {points.map((p, i) => (
        <circle key={p.measured_at} cx={x(i)} cy={y(p.value)} r="4" fill="#0B3C49" />
      ))}
      <text x={pad} y={height - 4} fontSize="12" fill="#4A5E62">
        {values[0]} {unit}
      </text>
      <text x={width - pad} y={height - 4} fontSize="12" fill="#4A5E62" textAnchor="end">
        {values[values.length - 1]} {unit}
      </text>
    </svg>
  );
}

export default function Timeline() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTimeline("bp_systolic", 14).then(setData).catch((e) => setError(e.message));
  }, []);

  if (error) return <p className="notice">Could not load the timeline. {error}</p>;
  if (!data) return <p className="notice">Loading timeline…</p>;

  const trendClass = data.trend.direction === "rising" ? "alert" : "ok";

  return (
    <section>
      <p className="eyebrow">Timeline · last 14 days</p>
      <h1>{data.label}</h1>

      <div className={`card trend ${trendClass}`}>
        <strong>{data.trend.summary}</strong>
        {data.trend.direction === "rising" && (
          <p>This is a sample trend. Discuss any change with your care team.</p>
        )}
      </div>

      <div className="card">
        <LineChart points={data.points} unit={data.unit} />
      </div>

      <h2>Readings</h2>
      <ul className="list">
        {data.points.map((p) => (
          <li key={p.measured_at} className="card reading">
            <span>{new Date(p.measured_at).toLocaleDateString()}</span>
            <strong>
              {p.value} {data.unit}
            </strong>
            <span className="muted">{p.source}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
