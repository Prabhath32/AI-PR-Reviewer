
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.contracts.review import (
    ReviewRequest,
    ValidatedReviewRequest,
)
from app.services.pr_urls import (
    InvalidPullRequestURL,
    parse_github_pr_url,
)

router = APIRouter()


class HealthResponse(BaseModel):
    status: str


@router.get(
    "/health/live",
    response_model=HealthResponse,
    tags=["health"],
)
def liveness() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get(
    "/health/ready",
    response_model=HealthResponse,
    tags=["health"],
)
def readiness() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post(
    "/reviews/validate",
    response_model=ValidatedReviewRequest,
    tags=["reviews"],
    summary="Validate PR URL syntax; does not authorize or fetch",
)
def validate_review_request(
    payload: ReviewRequest,
) -> ValidatedReviewRequest:
    try:
        locator = parse_github_pr_url(payload.pr_url)
    except InvalidPullRequestURL as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    return ValidatedReviewRequest(
        repository=locator,
        review_profile=payload.review_profile,
    )
