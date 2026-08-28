import json
from typing import Union

from pydantic import Field
from pydantic.dataclasses import dataclass

import mailtrap
from mailtrap.models.common import UNSET
from mailtrap.models.common import RequestParams
from mailtrap.models.common import UnsetType


@dataclass
class NestedParams(RequestParams):
    value: Union[str, None, UnsetType] = UNSET


@dataclass
class ParentParams(RequestParams):
    nested: NestedParams
    items: list[NestedParams] = Field(default_factory=list)


class TestRequestParams:
    def test_api_data_should_drop_unset_values_at_any_depth(self) -> None:
        params = ParentParams(
            nested=NestedParams(),
            items=[NestedParams(), NestedParams(value="set")],
        )

        api_data = params.api_data

        assert api_data == {"nested": {}, "items": [{}, {"value": "set"}]}
        assert json.dumps(api_data) == '{"nested": {}, "items": [{}, {"value": "set"}]}'


class TestPublicExports:
    def test_unset_and_its_type_are_both_exported(self) -> None:
        assert mailtrap.UNSET is UNSET
        assert mailtrap.UnsetType is UnsetType
