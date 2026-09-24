from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from . import store

STATIC_DIR = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(_: FastAPI):
    store.init_db()
    yield


app = FastAPI(title="Robotics Building Blocks Tutor", lifespan=lifespan)


class AnswerIn(BaseModel):
    choice: int = Field(ge=0, le=2, description="Option id as returned by /api/lessons/next")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/lessons/next")
def get_next_lesson(after: Optional[str] = None) -> dict:
    """Next lesson to study. Pass `after=<lesson_id>` to avoid repeating the lesson just shown."""
    lesson = store.next_lesson(exclude=after)
    if lesson is None:
        return {"done": True, "progress": store.progress()}
    return {
        "done": False,
        "id": lesson.id,
        "module": lesson.module,
        "title": lesson.title,
        "teach": lesson.teach,
        "question": lesson.question,
        "options": store.shuffled_options(lesson),
    }


@app.post("/api/lessons/{lesson_id}/answer")
def answer(lesson_id: str, body: AnswerIn) -> dict:
    lesson = store.get_lesson(lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Unknown lesson")
    correct = store.record_answer(lesson, body.choice)
    return {
        "correct": correct,
        "correct_choice": lesson.correct,
        "correct_text": lesson.options[lesson.correct],
        "explanation": lesson.explanation,
        "progress": store.progress(),
    }


@app.get("/api/progress")
def get_progress() -> dict:
    return store.progress()
