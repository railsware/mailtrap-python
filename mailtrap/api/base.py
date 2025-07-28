from abc import ABC
from enum import Enum
from typing import Any, Dict, List, NoReturn, Union, cast
from requests import Response, Session

from mailtrap.exceptions import APIError, AuthorizationError

RESPONSE_TYPE = Dict[str, Any]
LIST_RESPONSE_TYPE = List[Dict[str, Any]]


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELTE = "DELETE"


def _extract_errors(data: Dict[str, Any]) -> List[str]:
    if "errors" in data:
        errors = data["errors"]

        if isinstance(errors, list):
            return [str(err) for err in errors]

        if isinstance(errors, dict):
            flat_errors = []
            for key, value in errors.items():
                if isinstance(value, list):
                    flat_errors.extend([f"{key}: {v}" for v in value])
                else:
                    flat_errors.append(f"{key}: {value}")
            return flat_errors

        return [str(errors)]

    elif "error" in data:
        return [str(data["error"])]

    return ["Unknown error"]


class BaseHttpApiClient(ABC):
    def __init__(self, session: Session):
        self.session = session

    def _request(self, method: HttpMethod, url: str, **kwargs: Any) -> Union[RESPONSE_TYPE, LIST_RESPONSE_TYPE]:
        response = self.session.request(method.value, url, **kwargs)
        if response.ok:
            data = cast(Union[RESPONSE_TYPE, LIST_RESPONSE_TYPE], response.json())
            return data

        self._handle_failed_response(response)

    @staticmethod
    def _handle_failed_response(response: Response) -> NoReturn:
        status_code = response.status_code

        try:
            data = response.json()
        except ValueError:
            raise APIError(status_code, errors=["Unknown Error"])

        errors = _extract_errors(data)

        if status_code == 401:
            raise AuthorizationError(errors=errors)

        raise APIError(status_code, errors=errors)

