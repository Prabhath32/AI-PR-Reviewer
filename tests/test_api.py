
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app


def build_client() -> TestClient:
    return TestClient(
        create_app(Settings(_env_file=None, app_env="test"))
    )


def test_health_routes():
    with build_client() as client:
        assert client.get(
            "/api/v1/health/live"
        ).json() == {"status": "ok"}

        assert client.get(
            "/api/v1/health/ready"
        ).status_code == 200


def test_validate_does_not_claim_authorization():
    with build_client() as client:
        response = client.post(
            "/api/v1/reviews/validate",
            json={
                "pr_url": (
                    "https://github.com/"
                    "example/sample/pull/15"
                )
            },
        )

    assert response.status_code == 200
    assert response.json()["authorization_checked"] is False
    assert response.json()["repository"]["pull_number"] == 15


def test_invalid_url_is_unprocessable():
    with build_client() as client:
        response = client.post(
            "/api/v1/reviews/validate",
            json={"pr_url": "https://example.org/not-github"},
        )

    assert response.status_code == 422
