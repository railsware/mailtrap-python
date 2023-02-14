from mailtrap.mail.address import Address


class TestAddress:
    def test_api_data_should_return_dict_with_required_props_only(self) -> None:
        entity = Address(email="joe@mail.com")
        assert entity.api_data == {"email": "joe@mail.com"}

    def test_api_data_should_return_dict_with_all_props(self) -> None:
        entity = Address(email="joe@mail.com", name="Joe")
        assert entity.api_data == {"email": "joe@mail.com", "name": "Joe"}
