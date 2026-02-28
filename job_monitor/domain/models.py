from dataclasses import asdict, dataclass
from typing import Optional


@dataclass(frozen=True)
class SearchCriteria:
    role: str
    location: str = ""
    days: int = 2

    @property
    def query(self) -> str:
        return f"{self.role} {self.location}".strip()


@dataclass
class JobPost:
    text: str
    post_url: str
    source: str
    matched_role: str
    matched_location: str
    timestamp_scraped: str
    inferred_post_age_days: Optional[int] = None

    def to_record(self) -> dict:
        return asdict(self)

