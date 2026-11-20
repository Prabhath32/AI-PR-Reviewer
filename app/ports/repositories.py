
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class PullRequestSnapshot:
    github_repository_id: int
    number: int
    head_sha: str
    base_sha: str


class PullRequestReader(Protocol):
    async def get_snapshot(
        self,
        *,
        repository_id: int,
        pull_number: int,
    ) -> PullRequestSnapshot:
        ...

    async def get_changed_file_paths(
        self,
        *,
        repository_id: int,
        pull_number: int,
        head_sha: str,
    ) -> list[str]:
        ...
