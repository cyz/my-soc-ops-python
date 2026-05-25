import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestHomePage:
    def test_home_returns_200(self, client: TestClient):
        response = client.get("/")
        assert response.status_code == 200

    def test_home_contains_start_screen(self, client: TestClient):
        response = client.get("/")
        assert "Soc Ops" in response.text
        assert "Start Game" in response.text
        assert "How to play" in response.text

    def test_home_sets_session_cookie(self, client: TestClient):
        response = client.get("/")
        assert "session" in response.cookies


class TestStartGame:
    def test_start_returns_game_board(self, client: TestClient):
        # First visit to get session
        client.get("/")
        response = client.post("/start")
        assert response.status_code == 200
        assert "FREE SPACE" in response.text
        assert "← Back" in response.text

    def test_board_has_25_squares(self, client: TestClient):
        client.get("/")
        response = client.post("/start")
        # Count the toggle buttons (squares with hx-post="/toggle/")
        assert response.text.count('hx-post="/toggle/') == 24  # 24 + 1 free space

    def test_game_screen_has_accessible_button_labels(self, client: TestClient):
        client.get("/")
        response = client.post("/start")
        assert 'aria-label="Back to start screen"' in response.text
        assert 'role="group"' in response.text
        assert 'aria-label="Social bingo board"' in response.text


class TestToggleSquare:
    def test_toggle_marks_square(self, client: TestClient):
        client.get("/")
        client.post("/start")
        response = client.post("/toggle/0")
        assert response.status_code == 200
        # The response should contain the game screen with a marked square
        assert "FREE SPACE" in response.text


class TestResetGame:
    def test_reset_returns_start_screen(self, client: TestClient):
        client.get("/")
        client.post("/start")
        response = client.post("/reset")
        assert response.status_code == 200
        assert "Start Game" in response.text
        assert "How to play" in response.text


class TestDismissModal:
    def test_dismiss_returns_game_screen(self, client: TestClient):
        client.get("/")
        client.post("/start")
        response = client.post("/dismiss-modal")
        assert response.status_code == 200
        assert "FREE SPACE" in response.text


class TestAccessibility:
    def test_home_contains_accessible_start_button(self, client: TestClient):
        response = client.get("/")
        assert 'aria-label="Start game"' in response.text

    def test_bingo_modal_has_dialog_aria_attributes(self, client: TestClient):
        client.get("/")
        client.post("/start")

        for square_id in [0, 1, 2, 3]:
            client.post(f"/toggle/{square_id}")

        response = client.post("/toggle/4")
        assert 'role="dialog"' in response.text
        assert 'aria-modal="true"' in response.text
        assert 'aria-labelledby="bingo-title"' in response.text
        assert 'aria-describedby="bingo-description"' in response.text
