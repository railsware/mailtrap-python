import json
from unittest.mock import Mock

import pytest

from mailtrap.exceptions import APIError
from mailtrap.exceptions import AuthorizationError
from mailtrap.http import HttpClient


class TestHttpClient:

    def test_extract_errors_with_singular_error_key(self) -> None:
        data = {"error": "Simple error message"}
        errors = HttpClient._extract_errors(data)
        assert errors == ["Simple error message"]

    def test_extract_errors_with_string_value(self) -> None:
        data = {"errors": "Error message"}
        errors = HttpClient._extract_errors(data)
        assert errors == ["Error message"]

    def test_extract_errors_with_string_list(self) -> None:
        data = {"errors": ["Error 1", "Error 2"]}
        errors = HttpClient._extract_errors(data)
        assert errors == ["Error 1", "Error 2"]

    def test_extract_errors_with_nested_dict(self) -> None:
        data = {"errors": {"field1": ["Error in field1"], "field2": "Error in field2"}}
        errors = HttpClient._extract_errors(data)
        assert "field1: Error in field1" in errors
        assert "field2: Error in field2" in errors

    def test_extract_errors_with_unknown_format(self) -> None:
        data = {"unknown_key": "Some error"}
        errors = HttpClient._extract_errors(data)
        assert errors == ["Unknown error"]

    def test_handle_failed_response_401_raises_authorization_error(self) -> None:
        client = HttpClient("test.mailtrap.com")

        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.content = b'{"error": "Unauthorized"}'
        mock_response.json.return_value = {"error": "Unauthorized"}

        with pytest.raises(AuthorizationError) as exc_info:
            client._handle_failed_response(mock_response)

        assert "Unauthorized" in str(exc_info.value)

    def test_handle_failed_response_404_with_empty_content(self) -> None:
        client = HttpClient("test.mailtrap.com")

        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.content = b""

        with pytest.raises(APIError) as exc_info:
            client._handle_failed_response(mock_response)

        assert exc_info.value.status == 404
        assert "Not Found" in exc_info.value.errors

    def test_handle_failed_response_with_empty_content(self) -> None:
        client = HttpClient("test.mailtrap.com")

        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.content = b""

        with pytest.raises(APIError) as exc_info:
            client._handle_failed_response(mock_response)

        assert exc_info.value.status == 500
        assert "Empty response body" in exc_info.value.errors

    def test_handle_failed_response_invalid_json(self) -> None:
        client = HttpClient("test.mailtrap.com")

        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.content = b"Invalid JSON content"
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)

        with pytest.raises(APIError) as exc_info:
            client._handle_failed_response(mock_response)

        assert exc_info.value.status == 400
        assert "Invalid JSON" in exc_info.value.errors

    def test_handle_failed_response_generic_error(self) -> None:
        client = HttpClient("test.mailtrap.com")

        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.content = b'{"error": "Internal server error"}'
        mock_response.json.return_value = {"error": "Internal server error"}

        with pytest.raises(APIError) as exc_info:
            client._handle_failed_response(mock_response)

        assert exc_info.value.status == 500
        assert "Internal server error" in exc_info.value.errors
