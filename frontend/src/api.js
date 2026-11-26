// Base address of the FastAPI backend. Override with VITE_API_URL when deploying.
export const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// The demo patient. Real sign-in replaces this later.
export const PATIENT_REF = "DEMO-MAYA";

async function getJson(path) {
  const res = await fetch(`${API_URL}${path}`);
  if (!res.ok) {
    throw new Error(`Request failed (${res.status}): ${path}`);
  }
  return res.json();
}

export function fetchToday() {
  return getJson(`/patients/${PATIENT_REF}/today`);
}

export function fetchTimeline(kind = "bp_systolic", days = 14) {
  return getJson(`/patients/${PATIENT_REF}/timeline?kind=${kind}&days=${days}`);
}
