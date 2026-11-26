import { useState } from "react";
import Today from "./screens/Today.jsx";
import Timeline from "./screens/Timeline.jsx";

const TABS = [
  { id: "today", label: "Today" },
  { id: "timeline", label: "Timeline" },
];

export default function App() {
  const [tab, setTab] = useState("today");

  return (
    <div className="app">
      <main className="screen">
        {tab === "today" ? <Today /> : <Timeline />}
      </main>

      <nav className="tabs" aria-label="Main">
        {TABS.map((t) => (
          <button
            key={t.id}
            className={tab === t.id ? "tab active" : "tab"}
            aria-current={tab === t.id ? "page" : undefined}
            onClick={() => setTab(t.id)}
          >
            {t.label}
          </button>
        ))}
      </nav>
    </div>
  );
}
