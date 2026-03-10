"""
Integration tests.

Tests require a running PostgreSQL instance and a valid GEMINI_API_KEY.
Set these in the root .env before running, or as CI/CD secrets.

Run:
  docker exec backend pytest tests/
"""

import asyncio
import os
import pytest
from dotenv import load_dotenv

from database import get_db
from services.text_to_sql import answer_question
from services.llm.gemini import GeminiClient

# Load root-level .env (one level above backend/)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))


# ── Shared fixture ─────────────────────────────────────────────────────────────

@pytest.fixture()
def db():
    """
    Yields a real SQLAlchemy session using the existing get_db() from database.py.
    Automatically closed after each test.
    """
    session = next(get_db())
    yield session


# ── Gemini Connection ──────────────────────────────────────────────────────────

class TestGeminiConnection:

    def test_gemini_returns_a_response(self):
        """Gemini should return a non-empty string for a simple prompt."""
        client = GeminiClient()
        response = client.generate("Reply with the single word: pong")
        assert isinstance(response, str), "Response should be a string."
        assert len(response) > 0, "Response should not be empty."


# ── answer_question (main service) ────────────────────────────────────────────

class TestAnswerQuestion:
    """
    Integration tests for the answer_question service.

    These tests hit the real PostgreSQL database and the real Gemini API.
    Requires the backend container to be running with a seeded database.

    DB state assumed:
      user_id=2  → student@campus.com
      student_id=1 → division: "Computer Science"
    """

    def test_student_division_name(self, db):
        """
        Acting as student_id=1 (user_id=2), ask for the student's division name.
        The LLM must query the DB and return an answer containing 'Computer Science'.
        """
        user_metadata = {
            "role": "student",
            "student_id": 1,
            "user_id": 2,
        }

        response = asyncio.run(
            answer_question(
                question="What is the name of my division?",
                user_metadata=user_metadata,
                db=db,
            )
        )

        assert isinstance(response, str), "Response must be a string."
        assert len(response) > 0, "Response must not be empty."
        assert "Computer Science" in response, (
            f"Expected 'Computer Science' in response, got: {response!r}"
        )

    def test_non_existent_user_returns_non_existent(self, db):
        """
        Acting as student_id=0 (user_id=0), which does not exist in the DB.
        The SQL query should return no rows, and the LLM must reply
        with a message containing 'non existent'.
        """
        user_metadata = {
            "role": "student",
            "student_id": 0,
            "user_id": 0,
        }

        response = asyncio.run(
            answer_question(
                question="What is the name of my division?",
                user_metadata=user_metadata,
                db=db,
            )
        )

        assert isinstance(response, str), "Response must be a string."
        assert len(response) > 0, "Response must not be empty."
        assert "non existent" in response.lower(), (
            f"Expected 'non existent' in response, got: {response!r}"
        )

    def test_off_topic_question_returns_not_relevant(self, db):
        """
        Asking a question unrelated to the campus database (e.g. cake recipe)
        should NOT trigger a SQL query. The LLM must respond with
        a message containing 'not relevant'.
        """
        user_metadata = {"role": "admin"}

        response = asyncio.run(
            answer_question(
                question="How do I bake a chocolate cake?",
                user_metadata=user_metadata,
                db=db,
            )
        )

        assert isinstance(response, str), "Response must be a string."
        assert len(response) > 0, "Response must not be empty."
        assert "not relevant" in response.lower(), (
            f"Expected 'not relevant' in response, got: {response!r}"
        )
