import pytest
from pydantic import ValidationError

from mailtrap.models.templates import CreateEmailTemplateParams
from mailtrap.models.templates import UpdateEmailTemplateParams


class TestCreateEmailTemplateParams:
    def test_api_data_should_return_dict_with_required_props_only(self) -> None:
        entity = CreateEmailTemplateParams(name="test", subject="test", category="test")
        assert entity.api_data == {
            "name": "test",
            "subject": "test",
            "category": "test",
        }

    def test_api_data_should_return_dict_with_all_props(self) -> None:
        entity = CreateEmailTemplateParams(
            name="test",
            subject="test",
            category="test",
            body_text="test",
            body_html="test",
        )
        assert entity.api_data == {
            "name": "test",
            "subject": "test",
            "category": "test",
            "body_text": "test",
            "body_html": "test",
        }


class TestUpdateEmailTemplateParams:
    def test_raise_error_when_all_fields_are_missing(self) -> None:
        with pytest.raises(ValidationError) as exc:
            _ = UpdateEmailTemplateParams()

        assert "At least one field must be provided for update actio" in str(exc)

    def test_api_data_should_return_dict_with_required_props_only(self) -> None:
        entity = UpdateEmailTemplateParams(name="test", subject="test", category="test")
        assert entity.api_data == {
            "name": "test",
            "subject": "test",
            "category": "test",
        }

    def test_api_data_should_return_dict_with_all_props(self) -> None:
        entity = UpdateEmailTemplateParams(
            name="test",
            subject="test",
            category="test",
            body_text="test",
            body_html="test",
        )
        assert entity.api_data == {
            "name": "test",
            "subject": "test",
            "category": "test",
            "body_text": "test",
            "body_html": "test",
        }
