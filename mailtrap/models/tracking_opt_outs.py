from datetime import datetime
from typing import Optional

from pydantic import Field
from pydantic.dataclasses import dataclass

from mailtrap.models.common import RequestParams


@dataclass
class TrackingOptOut:
    id: str
    email: str
    created_at: datetime
    domain_name: Optional[str] = None


@dataclass
class TrackingOptOutResponse:
    data: TrackingOptOut


@dataclass
class TrackingOptOutsListResponse:
    """A page of tracking opt-outs. `last_id` is the cursor for the next page,
    or `None` when there are no more pages."""

    data: list[TrackingOptOut] = Field(default_factory=list)
    last_id: Optional[str] = None


@dataclass
class TrackingOptOutsListParams(RequestParams):
    email: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    last_id: Optional[str] = None


@dataclass
class CreateTrackingOptOutParams(RequestParams):
    email: str
    domain_id: int
