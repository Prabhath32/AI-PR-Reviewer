
import pytest

from app.domain.review import (
    InvalidReviewTransition,
    ReviewStatus,
    assert_transition,
)


def test_valid_review_transition():
    assert_transition(
        ReviewStatus.QUEUED,
        ReviewStatus.FETCHING_CONTEXT,
    )


def test_terminal_status_cannot_requeue():
    with pytest.raises(InvalidReviewTransition):
        assert_transition(
            ReviewStatus.COMPLETED,
            ReviewStatus.QUEUED,
        )
