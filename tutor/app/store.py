"""Progress tracking: attempts log, spaced-review state, mastery gating.

Rules
- A module is *mastered* when every lesson in it has been attempted and at least
  MASTERY_THRESHOLD of its lessons were answered correctly the last time.
- Module N+1 unlocks only when module N is mastered.
- Each lesson sits in a Leitner box 1..5. Correct moves it up a box, wrong sends
  it back to box 1. Higher boxes are reviewed after longer gaps.
- The "ready for Python" flag is true when every module is mastered.
"""

import os
import random
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterator, Optional

from .curriculum import LESSONS, LESSONS_BY_ID, MODULES, Lesson

MASTERY_THRESHOLD = 0.75
MAX_BOX = 5
# Days until a lesson is due again, by box. Box 1 (just failed / brand new) is due immediately.
REVIEW_DAYS = {1: 0, 2: 1, 3: 3, 4: 7, 5: 14}

DEFAULT_DB = Path(__file__).resolve().parent.parent / "tutor.db"


def db_path() -> Path:
    return Path(os.environ.get("ROBOTICS_TUTOR_DB", DEFAULT_DB))


def now() -> datetime:
    return datetime.now(timezone.utc)


@contextmanager
def connect() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(db_path())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lesson_id TEXT NOT NULL,
                chosen INTEGER NOT NULL,
                correct INTEGER NOT NULL,
                ts TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS lesson_state (
                lesson_id TEXT PRIMARY KEY,
                box INTEGER NOT NULL,
                due_ts TEXT NOT NULL,
                last_correct INTEGER NOT NULL
            );
            """
        )


def record_answer(lesson: Lesson, chosen: int) -> bool:
    """Log an attempt, update the lesson's review state, and return whether it was correct."""
    correct = chosen == lesson.correct
    ts = now()
    with connect() as conn:
        conn.execute(
            "INSERT INTO attempts (lesson_id, chosen, correct, ts) VALUES (?, ?, ?, ?)",
            (lesson.id, chosen, int(correct), ts.isoformat()),
        )
        row = conn.execute("SELECT box FROM lesson_state WHERE lesson_id = ?", (lesson.id,)).fetchone()
        old_box = row["box"] if row else 1
        new_box = min(old_box + 1, MAX_BOX) if correct else 1
        due = ts + timedelta(days=REVIEW_DAYS[new_box])
        conn.execute(
            """
            INSERT INTO lesson_state (lesson_id, box, due_ts, last_correct) VALUES (?, ?, ?, ?)
            ON CONFLICT(lesson_id) DO UPDATE SET box = excluded.box,
                due_ts = excluded.due_ts, last_correct = excluded.last_correct
            """,
            (lesson.id, new_box, due.isoformat(), int(correct)),
        )
    return correct


def _states() -> dict[str, sqlite3.Row]:
    with connect() as conn:
        return {r["lesson_id"]: r for r in conn.execute("SELECT * FROM lesson_state")}


def module_status() -> list[dict]:
    """Per-module stats, with mastery and unlock state resolved in order."""
    states = _states()
    result: list[dict] = []
    previous_mastered = True
    for module in MODULES:
        lessons = [l for l in LESSONS if l.module == module.id]
        attempted = sum(1 for l in lessons if l.id in states)
        correct = sum(1 for l in lessons if l.id in states and states[l.id]["last_correct"])
        mastered = attempted == len(lessons) and correct / len(lessons) >= MASTERY_THRESHOLD
        result.append(
            {
                "id": module.id,
                "title": module.title,
                "summary": module.summary,
                "lessons": len(lessons),
                "attempted": attempted,
                "correct": correct,
                "mastered": mastered,
                "unlocked": previous_mastered,
            }
        )
        previous_mastered = previous_mastered and mastered
    return result


def next_lesson(exclude: Optional[str] = None) -> Optional[Lesson]:
    """Pick what to study next.

    Priority: (1) lessons last answered wrong, (2) unseen lessons in unlocked
    modules, in curriculum order, (3) review lessons that are due. `exclude`
    avoids showing the same lesson twice in a row when there is an alternative.
    """
    states = _states()
    unlocked = {m["id"] for m in module_status() if m["unlocked"]}
    candidates = [l for l in LESSONS if l.module in unlocked]

    failed = [l for l in candidates if l.id in states and not states[l.id]["last_correct"]]
    unseen = [l for l in candidates if l.id not in states]
    current = now()
    due = sorted(
        (l for l in candidates
         if l.id in states and states[l.id]["last_correct"]
         and datetime.fromisoformat(states[l.id]["due_ts"]) <= current),
        key=lambda l: states[l.id]["due_ts"],
    )

    for group in (failed, unseen, due):
        pick = [l for l in group if l.id != exclude] or group
        if pick:
            return pick[0]
    return None


def progress() -> dict:
    modules = module_status()
    states = _states()
    with connect() as conn:
        total_attempts = conn.execute("SELECT COUNT(*) FROM attempts").fetchone()[0]
        recent = [
            {"lesson_id": r["lesson_id"], "correct": bool(r["correct"]), "ts": r["ts"]}
            for r in conn.execute("SELECT lesson_id, correct, ts FROM attempts ORDER BY id DESC LIMIT 10")
        ]
    mastered = sum(1 for m in modules if m["mastered"])
    return {
        "modules": modules,
        "modules_mastered": mastered,
        "modules_total": len(modules),
        "lessons_correct": sum(1 for s in states.values() if s["last_correct"]),
        "lessons_total": len(LESSONS),
        "total_attempts": total_attempts,
        "ready_for_python": mastered == len(modules),
        "recent": recent,
    }


def shuffled_options(lesson: Lesson) -> list[dict]:
    """Options as {id, text}, shuffled. `id` is the original index and is what the client sends back."""
    options = [{"id": i, "text": text} for i, text in enumerate(lesson.options)]
    random.shuffle(options)
    return options


def get_lesson(lesson_id: str) -> Optional[Lesson]:
    return LESSONS_BY_ID.get(lesson_id)
