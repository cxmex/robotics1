import pytest
from fastapi.testclient import TestClient

from app.curriculum import LESSONS, LESSONS_BY_ID, MODULES
from app.main import app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("ROBOTICS_TUTOR_DB", str(tmp_path / "test.db"))
    with TestClient(app) as c:
        yield c


def answer(client, lesson_id, correct=True):
    lesson = LESSONS_BY_ID[lesson_id]
    choice = lesson.correct if correct else (lesson.correct + 1) % 3
    return client.post(f"/api/lessons/{lesson_id}/answer", json={"choice": choice}).json()


def test_first_lesson_is_first_in_curriculum(client):
    data = client.get("/api/lessons/next").json()
    assert data["id"] == LESSONS[0].id
    assert len(data["options"]) == 3
    assert "correct" not in data and "explanation" not in data  # answer not leaked


def test_options_are_a_permutation_of_original_ids(client):
    data = client.get("/api/lessons/next").json()
    assert sorted(o["id"] for o in data["options"]) == [0, 1, 2]


def test_answer_grades_by_original_option_id(client):
    first = LESSONS[0]
    r = answer(client, first.id, correct=True)
    assert r["correct"] is True and r["correct_choice"] == first.correct
    r = answer(client, first.id, correct=False)
    assert r["correct"] is False and r["correct_text"] == first.options[first.correct]


def test_wrong_answer_is_retried_before_new_material(client):
    first, second = LESSONS[0], LESSONS[1]
    answer(client, first.id, correct=False)
    # Asking "after" the failed lesson still returns it when nothing else is failed.
    assert client.get("/api/lessons/next").json()["id"] == first.id
    answer(client, first.id, correct=True)
    assert client.get("/api/lessons/next").json()["id"] == second.id


def test_next_module_locked_until_current_mastered(client):
    first_module = [l for l in LESSONS if l.module == MODULES[0].id]
    for lesson in first_module[:-1]:
        answer(client, lesson.id)
    p = client.get("/api/progress").json()
    assert p["modules"][0]["mastered"] is False
    assert p["modules"][1]["unlocked"] is False

    answer(client, first_module[-1].id)
    p = client.get("/api/progress").json()
    assert p["modules"][0]["mastered"] is True
    assert p["modules"][1]["unlocked"] is True
    assert p["modules"][2]["unlocked"] is False


def test_completing_everything_sets_ready_for_python(client):
    assert client.get("/api/progress").json()["ready_for_python"] is False
    for lesson in LESSONS:
        answer(client, lesson.id)
    p = client.get("/api/progress").json()
    assert p["ready_for_python"] is True
    assert p["modules_mastered"] == p["modules_total"]
    assert p["total_attempts"] == len(LESSONS)
    # Nothing is due immediately after answering correctly (box 2 = due in 1 day).
    assert client.get("/api/lessons/next").json()["done"] is True


def test_progress_persists_across_app_restarts(tmp_path, monkeypatch):
    monkeypatch.setenv("ROBOTICS_TUTOR_DB", str(tmp_path / "persist.db"))
    with TestClient(app) as c:
        answer(c, LESSONS[0].id)
    with TestClient(app) as c:
        assert c.get("/api/progress").json()["total_attempts"] == 1


def test_unknown_lesson_404_and_bad_choice_422(client):
    assert client.post("/api/lessons/nope/answer", json={"choice": 0}).status_code == 404
    assert client.post(f"/api/lessons/{LESSONS[0].id}/answer", json={"choice": 3}).status_code == 422


def test_index_page_served(client):
    r = client.get("/")
    assert r.status_code == 200 and "Robotics building blocks" in r.text
