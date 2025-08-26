import pytest

from mailtrap.models.contacts import ContactListParams
from mailtrap.models.contacts import CreateContactFieldParams
from mailtrap.models.contacts import UpdateContactFieldParams


class TestCreateContactFieldParams:
    def test_create_contact_field_params_api_data_should_return_correct_dict(
        self,
    ) -> None:
        params = CreateContactFieldParams(
            name="Test Field", data_type="integer", merge_tag="test_field"
        )

        api_data = params.api_data

        assert api_data == {
            "name": "Test Field",
            "data_type": "integer",
            "merge_tag": "test_field",
        }


class TestUpdateContactFieldParams:
    def test_update_contact_field_params_with_none_values_should_raise_error(
        self,
    ) -> None:
        with pytest.raises(
            ValueError, match="At least one field must be provided for update action"
        ):
            _ = UpdateContactFieldParams()

    def test_update_contact_field_params_with_partial_values_should_not_raise_error(
        self,
    ) -> None:
        params = UpdateContactFieldParams(name="Updated Field")
        assert params.name == "Updated Field"
        assert params.merge_tag is None

    def test_update_contact_field_params_api_data_should_exclude_none_values(
        self,
    ) -> None:
        params = UpdateContactFieldParams(name="Updated Field")
        api_data = params.api_data

        assert api_data == {"name": "Updated Field"}

    def test_update_contact_field_params_api_data_with_all_values(self) -> None:
        params = UpdateContactFieldParams(name="Updated Field", merge_tag="updated_field")
        api_data = params.api_data

        assert api_data == {"name": "Updated Field", "merge_tag": "updated_field"}


class TestContactListParams:
    def test_create_contact_field_params_api_data_should_return_correct_dict(
        self,
    ) -> None:
        params = ContactListParams(name="Test List")
        api_data = params.api_data
        assert api_data == {"name": "Test List"}
