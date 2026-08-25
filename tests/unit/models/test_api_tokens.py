from mailtrap.models.api_tokens import ApiTokenResource
from mailtrap.models.api_tokens import CreateApiTokenParams
from mailtrap.models.api_tokens import ResetApiTokenParams


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

    def test_create_api_token_params_api_data_should_omit_unset_expires_at(self) -> None:
        params = CreateApiTokenParams(name="My API Token")

        assert params.api_data == {"name": "My API Token", "resources": []}

    def test_create_api_token_params_api_data_should_keep_explicit_none_expires_at(
        self,
    ) -> None:
        params = CreateApiTokenParams(name="My API Token", expires_at=None)

        assert params.api_data == {
            "name": "My API Token",
            "resources": [],
            "expires_at": None,
        }

    def test_create_api_token_params_api_data_should_pass_expires_at_through(
        self,
    ) -> None:
        params = CreateApiTokenParams(
            name="My API Token", expires_at="2027-06-01T00:00:00Z"
        )

        assert params.api_data == {
            "name": "My API Token",
            "resources": [],
            "expires_at": "2027-06-01T00:00:00Z",
        }


class TestResetApiTokenParams:
    def test_reset_api_token_params_api_data_should_omit_unset_expires_at(self) -> None:
        params = ResetApiTokenParams()

        assert params.api_data == {}

    def test_reset_api_token_params_api_data_should_keep_explicit_none_expires_at(
        self,
    ) -> None:
        params = ResetApiTokenParams(expires_at=None)

        assert params.api_data == {"expires_at": None}

    def test_reset_api_token_params_api_data_should_pass_expires_at_through(self) -> None:
        params = ResetApiTokenParams(expires_at="2027-06-01T00:00:00Z")

        assert params.api_data == {"expires_at": "2027-06-01T00:00:00Z"}
