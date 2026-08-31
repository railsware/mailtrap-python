from typing import Any
from typing import Optional
from typing import Union

from pydantic import Field
from pydantic.dataclasses import dataclass

from mailtrap.models.common import UNSET
from mailtrap.models.common import RequestParams
from mailtrap.models.common import UnsetType


@dataclass
class ApiTokenResource:
    resource_type: str
    resource_id: Union[int, str]
    access_level: int


@dataclass
class ApiToken:
    id: int
    name: str
    last_4_digits: str
    created_by: str
    expires_at: Optional[str]
    resources: list[ApiTokenResource]


@dataclass
class ApiTokenWithToken(ApiToken):
    token: str = ""


@dataclass
class CreateApiTokenParams(RequestParams):
    name: str
    resources: list[ApiTokenResource] = Field(default_factory=list)
    expires_at: Union[str, None, UnsetType] = UNSET

    @property
    def api_data(self) -> dict[str, Any]:
        data = dict(super().api_data)
        # exclude_none strips an explicit None, but here it must be sent
        # as "expires_at": null (a token that never expires).
        if self.expires_at is None:
            data["expires_at"] = None
        return data


@dataclass
class ResetApiTokenParams(RequestParams):
    expires_at: Union[str, None, UnsetType] = UNSET

    @property
    def api_data(self) -> dict[str, Any]:
        data = dict(super().api_data)
        # exclude_none strips an explicit None, but here it must be sent
        # as "expires_at": null (a token that never expires).
        if self.expires_at is None:
            data["expires_at"] = None
        return data
