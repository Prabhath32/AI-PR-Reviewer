
import re
from urllib.parse import urlsplit

from app.contracts.review import RepositoryLocator

_REPO_PART = re.compile(r"^[A-Za-z0-9_.-]{1,100}$")
_PR_SEGMENT = re.compile(r"^[1-9][0-9]*$")


class InvalidPullRequestURL(ValueError):
    pass


def parse_github_pr_url(value: str) -> RepositoryLocator:
    try:
        url = urlsplit(value)
    except ValueError as exc:
        raise InvalidPullRequestURL(
            "Malformed GitHub PR URL"
        ) from exc

    if (
        url.scheme != "https"
        or url.hostname != "github.com"
        or url.port is not None
        or url.username is not None
        or url.password is not None
        or url.query
        or url.fragment
    ):
        raise InvalidPullRequestURL(
            "Expected a canonical https://github.com PR URL"
        )

    parts = url.path.strip("/").split("/")

    if len(parts) != 4 or parts[2] != "pull":
        raise InvalidPullRequestURL(
            "Expected /<owner>/<repository>/pull/<number>"
        )

    owner, repository, _, number = parts

    if (
        not _REPO_PART.fullmatch(owner)
        or not _REPO_PART.fullmatch(repository)
    ):
        raise InvalidPullRequestURL(
            "Invalid repository identifier"
        )

    if not _PR_SEGMENT.fullmatch(number) or len(number) > 12:
        raise InvalidPullRequestURL(
            "Invalid pull request number"
        )

    return RepositoryLocator(
        owner=owner,
        repository=repository,
        pull_number=int(number),
    )
