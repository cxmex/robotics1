# Robotics Building Blocks Tutor

A small FastAPI app. It shows one lesson at a time with 3 answer options, records each result in SQLite, and only unlocks the next module once you have mastered the current one. When every module is mastered it reports `ready_for_python: true`.

Companion to `../ROBOTICS-LEARNING-RESEARCH.md` (see section 5 for why it is built this way).

## Run

```
cd robotics/tutor
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000. API docs are at `/docs`. Progress is stored in `tutor.db` next to `app/`; delete that file to start over. Set `ROBOTICS_TUTOR_DB` to store it elsewhere.

## How it decides what to show

1. Lessons you last answered wrong come first, until you get them right.
2. Then unseen lessons in unlocked modules, in curriculum order.
3. Then spaced reviews that are due. A correct answer moves a lesson up a Leitner box (review after 1, 3, 7, 14 days); a wrong answer sends it back to box 1.

A module counts as mastered when every lesson in it has been attempted and at least 75% are currently correct. The next module unlocks when the previous one is mastered.

## API

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/lessons/next?after=<id>` | Next lesson (options shuffled; answer not included) |
| POST | `/api/lessons/{id}/answer` `{"choice": 0-2}` | Grade and record; `choice` is the option `id` from the lesson |
| GET | `/api/progress` | Modules, mastery, unlocks, recent attempts, `ready_for_python` |

## Add lessons

Edit `app/curriculum.py`: append a `Lesson` with exactly 3 options and set `correct` to the index of the right one. Import-time validation checks ids and option counts.

## Tests

```
pip install pytest httpx
python -m pytest
```

## Limits

- Single user, no login.
- Multiple-choice quizzing builds concepts, not the skill of tuning a controller or debugging a robot. Pair it with the simulation and hardware projects in the research report.
