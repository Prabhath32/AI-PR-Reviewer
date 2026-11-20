
import pytest

from app.services.pr_urls import (
    InvalidPullRequestURL,
    parse_github_pr_url,
)


def test_valid_pr_url():
    value = parse_github_pr_url(
        "https://github.com/acme/project/pull/42"
    )

    assert (
        value.owner,
        value.repository,
        value.pull_number,
    ) == ("acme", "project", 42)


@pytest.mark.parametrize(
    "url",
    [
        "http://github.com/acme/project/pull/42",
        "https://github.com.evil.test/acme/project/pull/42",
        "https://github.com/acme/project/pull/0",
        "https://github.com/acme/project/pull/42?secret=value",
        "https://user@github.com/acme/project/pull/42",
        "https://github.com/acme/project/issues/42",
        "https://github.com/acme/project/pull/42/extra",
    ],
)
def test_rejects_unsafe_or_incorrect_urls(url):
    with pytest.raises(InvalidPullRequestURL):
        parse_github_pr_url(url)
