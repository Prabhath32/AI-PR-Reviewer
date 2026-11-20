
from enum import StrEnum


class ReviewStatus(StrEnum):
    QUEUED = "queued"
    FETCHING_CONTEXT = "fetching_context"
    ANALYZING = "analyzing"
    VALIDATING = "validating"
    COMPLETED = "completed"
    PARTIAL = "partial"
    FAILED = "failed"
    CANCELLED = "cancelled"


class InvalidReviewTransition(ValueError):
    pass


ALLOWED_TRANSITIONS: dict[
    ReviewStatus, frozenset[ReviewStatus]
] = {
    ReviewStatus.QUEUED: frozenset({
        ReviewStatus.FETCHING_CONTEXT,
        ReviewStatus.CANCELLED,
    }),
    ReviewStatus.FETCHING_CONTEXT: frozenset({
        ReviewStatus.ANALYZING,
        ReviewStatus.FAILED,
        ReviewStatus.CANCELLED,
    }),
    ReviewStatus.ANALYZING: frozenset({
        ReviewStatus.VALIDATING,
        ReviewStatus.FAILED,
        ReviewStatus.CANCELLED,
    }),
    ReviewStatus.VALIDATING: frozenset({
        ReviewStatus.COMPLETED,
        ReviewStatus.PARTIAL,
        ReviewStatus.FAILED,
    }),
    ReviewStatus.COMPLETED: frozenset(),
    ReviewStatus.PARTIAL: frozenset(),
    ReviewStatus.FAILED: frozenset(),
    ReviewStatus.CANCELLED: frozenset(),
}


def assert_transition(
    current: ReviewStatus,
    target: ReviewStatus,
) -> None:
    if target not in ALLOWED_TRANSITIONS[current]:
        raise InvalidReviewTransition(
            f"Invalid review transition: {current} -> {target}"
        )
