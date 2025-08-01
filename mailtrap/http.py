from typing import Any, Optional, Type, TypeVar
from typing import NoReturn

from requests import Response, Session

from mailtrap.config import DEFAULT_REQUEST_TIMEOUT
from mailtrap.exceptions import APIError
from mailtrap.exceptions import AuthorizationError

T = TypeVar("T")


class HttpClient:
    def __init__(
        self, 
        host: str, 
        headers: Optional[dict[str, str]] = None, 
        timeout: int = DEFAULT_REQUEST_TIMEOUT
    ):
        self._host = host
        self._session = Session()
        self._session.headers.update(headers or {})
        self._timeout = timeout

    def _url(self, path: str) -> str:
        return f"https://{self._host}/{path.lstrip('/')}"

    def _handle_failed_response(self, response: Response) -> NoReturn:
        status_code = response.status_code
        try:
            data = response.json()
        except ValueError:
            raise APIError(status_code, errors=["Unknown Error"])

        errors = _extract_errors(data)

        if status_code == 401:
            raise AuthorizationError(errors=errors)

        raise APIError(status_code, errors=errors)

    def _process_response(
        self, 
        response: Response, 
        expected_type: Type[T]
    ) -> T:
        if not response.ok:
            self._handle_failed_response(response)
        data = response.json()
        if not isinstance(data, expected_type):
            raise APIError(response.status_code, errors=[f"Expected response type {expected_type.__name__}"])
        return data

    def _process_response_dict(self, response: Response) -> dict[str, Any]:
        return self._process_response(response, dict)

    def _process_response_list(self, response: Response) -> list[dict[str, Any]]:
        return self._process_response(response, list)

    def get(
        self, 
        path: str, 
        params: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        response = self._session.get(self._url(path), params=params, timeout=self._timeout)
        return self._process_response_dict(response)
    
    def list(
        self, 
        path: str, 
        params: Optional[dict[str, Any]] = None
    ) -> list[dict[str, Any]]:
        response = self._session.get(self._url(path), params=params, timeout=self._timeout)
        return self._process_response_list(response)

    def post(
        self, 
        path: str, 
        json: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        response = self._session.post(self._url(path), json=json, timeout=self._timeout)
        return self._process_response_dict(response)

    def put(
        self, 
        path: str, 
        json: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        response = self._session.put(self._url(path), json=json, timeout=self._timeout)
        return self._process_response_dict(response)

    def patch(
        self, 
        path: str, 
        json: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        response = self._session.patch(self._url(path), json=json, timeout=self._timeout)
        return self._process_response_dict(response)

    def delete(self, path: str) -> dict[str, Any]:
        response = self._session.delete(self._url(path), timeout=self._timeout)
        return self._process_response_dict(response)


def _extract_errors(data: dict[str, Any]) -> list[str]:    
    def flatten_errors(errors: Any) -> list[str]:
        if isinstance(errors, list):
            return [str(error) for error in errors]
        
        if isinstance(errors, dict):
            flat_errors = []
            for key, value in errors.items():
                if isinstance(value, list):
                    flat_errors.extend([f"{key}: {v}" for v in value])
                else:
                    flat_errors.append(f"{key}: {value}")
            return flat_errors

        return [str(errors)]
    
    if "errors" in data:
        return flatten_errors(data["errors"])
    
    if "error" in data:
        return flatten_errors(data["error"])

    return ["Unknown error"]
