from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from server import app as server_app


@pytest.fixture
def client(world, tmp_path, monkeypatch):
    monkeypatch.setattr(server_app, "_SESSIONS", {})
    monkeypatch.setattr(
        server_app, "SESSIONS_DB", tmp_path / "sessions.db"
    )
    return TestClient(server_app.app)


def test_session_rejects_claimed_role(client):
    response = client.post(
        "/sessions",
        json={"user_id": 1, "role": "support"},
    )

    assert response.status_code == 403
    assert server_app._SESSIONS == {}


def test_token_cannot_authorize_another_session(client, monkeypatch):
    first = client.post(
        "/sessions", json={"user_id": 1, "role": "shopper"}
    )
    second = client.post(
        "/sessions", json={"user_id": 1, "role": "shopper"}
    )
    assert first.status_code == second.status_code == 200

    build_agent = Mock(side_effect=AssertionError("agent must not run"))
    monkeypatch.setattr(server_app, "build_agent", build_agent)

    response = client.post(
        f"/sessions/{second.json()['session_id']}/messages",
        headers={"Authorization": f"Bearer {first.json()['token']}"},
        json={"message": "Show my recent orders."},
    )

    assert response.status_code == 403
    build_agent.assert_not_called()
