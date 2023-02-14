from mailtrap.exceptions import APIError
from mailtrap.exceptions import AuthorizationError


class TestAPIError:
    def test_str_representation_single_error_message(self) -> None:
        error = APIError(status=400, errors=["Error msg"])

        assert str(error) == "Error msg"

    def test_str_representation_multiple_error_messages(self) -> None:
        error = APIError(status=400, errors=["Error msg 1", "Error msg 2"])

        assert str(error) == "Error msg 1; Error msg 2"


class TestAuthorizationError:
    def test_str_representation_single_error_message(self) -> None:
        error = AuthorizationError(errors=["Error msg"])

        assert str(error) == "Error msg"

    def test_str_representation(self) -> None:
        error = AuthorizationError(errors=["Error msg 1", "Error msg 2"])

        assert str(error) == "Error msg 1; Error msg 2"
