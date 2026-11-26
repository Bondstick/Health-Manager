from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from . import db
from .models import Medicine, MedicineEvent, Patient, Reading
from .trends import compute_trend

router = APIRouter(prefix="/patients/{ref}", tags=["patient"])

LATEST_KINDS = {
    "bp_systolic": ("Systolic blood pressure", "mmHg"),
    "bp_diastolic": ("Diastolic blood pressure", "mmHg"),
    "weight_kg": ("Weight", "kg"),
}


def _patient_or_404(session, ref: str) -> Patient:
    patient = session.scalar(select(Patient).where(Patient.ref == ref))
    if patient is None:
        raise HTTPException(status_code=404, detail=f"No patient with ref {ref}")
    return patient


def _as_utc(dt: datetime) -> datetime:
    return dt.astimezone(timezone.utc) if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


@router.get("/today")
def today(ref: str):
    """Today's medicine doses and latest readings. Times are UTC for now."""
    now = datetime.now(timezone.utc)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)

    with db.SessionLocal() as session:
        patient = _patient_or_404(session, ref)

        doses = []
        medicines = session.scalars(
            select(Medicine).where(Medicine.patient_id == patient.id, Medicine.active.is_(True))
        ).all()
        for medicine in medicines:
            events = session.scalars(
                select(MedicineEvent).where(
                    MedicineEvent.medicine_id == medicine.id,
                    MedicineEvent.due_at >= start,
                    MedicineEvent.due_at < end,
                )
            ).all()
            by_time = {_as_utc(e.due_at).strftime("%H:%M"): e for e in events}
            for hhmm in medicine.times_per_day:
                event = by_time.get(hhmm)
                doses.append(
                    {
                        "medicine": medicine.name,
                        "dose": medicine.dose_text,
                        "due": hhmm,
                        "status": event.status if event else "pending",
                        "reason": event.reason if event else None,
                    }
                )

        latest = {}
        for kind, (label, unit) in LATEST_KINDS.items():
            reading = session.scalars(
                select(Reading)
                .where(Reading.patient_id == patient.id, Reading.kind == kind)
                .order_by(Reading.measured_at.desc())
                .limit(1)
            ).first()
            if reading:
                latest[kind] = {
                    "label": label,
                    "value": reading.value,
                    "unit": unit,
                    "measured_at": _as_utc(reading.measured_at).isoformat(),
                }

    return {"date": start.date().isoformat(), "doses": doses, "latest": latest}


@router.get("/timeline")
def timeline(ref: str, kind: str = "bp_systolic", days: int = 14):
    """Readings of one kind over the last N days, with a trend summary."""
    if kind not in LATEST_KINDS:
        raise HTTPException(status_code=400, detail=f"Unknown kind {kind}")
    label, unit = LATEST_KINDS[kind]
    since = datetime.now(timezone.utc) - timedelta(days=days)

    with db.SessionLocal() as session:
        patient = _patient_or_404(session, ref)
        readings = session.scalars(
            select(Reading)
            .where(
                Reading.patient_id == patient.id,
                Reading.kind == kind,
                Reading.measured_at >= since,
            )
            .order_by(Reading.measured_at.asc())
        ).all()

    points = [
        {
            "measured_at": _as_utc(r.measured_at).isoformat(),
            "value": r.value,
            "source": r.source,
        }
        for r in readings
    ]
    values = [r.value for r in readings]

    if readings:
        span_days = (_as_utc(readings[-1].measured_at) - _as_utc(readings[0].measured_at)).days + 1
    else:
        span_days = days
    trend = compute_trend(values, unit, label, span_days)

    return {
        "kind": kind,
        "label": label,
        "unit": unit,
        "points": points,
        "trend": {
            "direction": trend.direction,
            "change": trend.change,
            "summary": trend.summary,
        },
    }
