from mailtrap.models.api_tokens import ApiTokenResource
from mailtrap.models.api_tokens import CreateApiTokenParams


class TestCreateApiTokenParams:
    def test_create_api_token_params_should_accept_positional_arguments(self) -> None:
        resource = ApiTokenResource(
            resource_type="account", resource_id=3229, access_level=100
        )

        params = CreateApiTokenParams("My API Token", [resource])

        assert params.api_data == {
            "name": "My API Token",
            "resources": [
                {"resource_type": "account", "resource_id": 3229, "access_level": 100}
            ],
        }
