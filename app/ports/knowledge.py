
from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True, slots=True)
class KnowledgeHit:
    source_id: str
    content: str
    revision: str | None
    score: float


class KnowledgeReader(Protocol):
    async def search(
        self,
        *,
        organization_id: UUID,
        repository_id: UUID,
        query: str,
        limit: int = 5,
    ) -> list[KnowledgeHit]:
        ...
