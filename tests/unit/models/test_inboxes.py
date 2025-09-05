import pytest
from pydantic import ValidationError

from mailtrap.models.inboxes import CreateInboxParams
from mailtrap.models.inboxes import UpdateInboxParams


class TestCreateInboxParams:
    def test_api_data_should_return_dict_with_all_props(self) -> None:
        entity = CreateInboxParams(name="test")
        assert entity.api_data == {"name": "test"}


class TestUpdateInboxParams:
    def test_raise_error_when_all_fields_are_missing(self) -> None:
        with pytest.raises(ValidationError) as exc:
            _ = UpdateInboxParams()

        assert "At least one field must be provided for update actio" in str(exc)

    def test_api_data_should_return_dict_with_all_props(self) -> None:
        entity = UpdateInboxParams(name="test", email_username="test_username")
        assert entity.api_data == {"name": "test", "email_username": "test_username"}

    def test_api_data_should_return_dict_with_required_props_only(self) -> None:
        entity = UpdateInboxParams(name="test")
        assert entity.api_data == {"name": "test"}

        entity = UpdateInboxParams(email_username="test_username")
        assert entity.api_data == {"email_username": "test_username"}
