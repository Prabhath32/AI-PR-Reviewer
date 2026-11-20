from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.review import ReviewStatus


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ReviewProfile(StrEnum):
    STANDARD = "standard"
    SECURITY = "security"


class ReviewRequest(StrictModel):
    pr_url: str = Field(min_length=1, max_length=2048)
    review_profile: ReviewProfile = ReviewProfile.STANDARD


class RepositoryLocator(StrictModel):
    owner: str
    repository: str
    pull_number: int = Field(ge=1)


class ValidatedReviewRequest(StrictModel):
    repository: RepositoryLocator
    review_profile: ReviewProfile
    syntactically_valid: bool = True
    authorization_checked: bool = False


class ReviewAccepted(StrictModel):
    review_id: UUID
    status: ReviewStatus


class ReviewFinding(StrictModel):
    severity: str
    category: str
    title: str
    description: str
    recommendation: str
    file_path: str
    line_number: int = Field(ge=1)
    head_sha: str
    evidence: str