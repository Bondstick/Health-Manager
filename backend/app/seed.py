"""Loads fictional demo data for Maya. Safe to run more than once.

Run with:  docker compose exec api python -m app.seed
"""

from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from . import db
from .models import Consent, Medicine, MedicineEvent, Patient, Reading

DEMO_REF = "DEMO-MAYA"

# Ten days of fictional systolic readings, rising from 128 to 137 mmHg (+9).
SYSTOLIC = [128, 129, 129, 131, 132, 132, 134, 135, 136, 137]


def run():
    db.init_db()
    with db.SessionLocal() as session:
        existing = session.scalar(select(Patient).where(Patient.ref == DEMO_REF))
        if existing:
            print("Demo data already loaded. Nothing changed.")
            return

        now = datetime.now(timezone.utc).replace(hour=8, minute=0, second=0, microsecond=0)
        patient = Patient(ref=DEMO_REF, display_name="Maya (sample)")
        session.add(patient)
        session.flush()

        for purpose, granted in [
            ("readings", True),
            ("medicines", True),
            ("care_team_sharing", False),
        ]:
            session.add(Consent(patient_id=patient.id, purpose=purpose, granted=granted))

        for i, value in enumerate(SYSTOLIC):
            day = now - timedelta(days=len(SYSTOLIC) - 1 - i)
            session.add(
                Reading(
                    patient_id=patient.id,
                    kind="bp_systolic",
                    value=value,
                    unit="mmHg",
                    measured_at=day,
                    source="seed",
                )
            )

        medicine = Medicine(
            patient_id=patient.id,
            name="Sample medicine A",
            dose_text="500 mg",
            times_per_day=["08:00", "20:00"],
        )
        session.add(medicine)
        session.flush()

        # Seven days of dose history: all taken, except one skipped dose with a reason.
        for day_offset in range(7, 0, -1):
            for hhmm in medicine.times_per_day:
                hour, minute = map(int, hhmm.split(":"))
                due = (now - timedelta(days=day_offset)).replace(hour=hour, minute=minute)
                skipped = day_offset == 3 and hhmm == "20:00"
                session.add(
                    MedicineEvent(
                        medicine_id=medicine.id,
                        due_at=due,
                        status="skipped" if skipped else "taken",
                        reason="Felt unwell in the evening" if skipped else None,
                        recorded_at=due + timedelta(minutes=5),
                    )
                )

        session.commit()
        print("Demo data loaded for", DEMO_REF)


if __name__ == "__main__":
    run()
