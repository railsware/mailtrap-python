from typing import Dict
from typing import List
from typing import NoReturn
from typing import Union

import requests

from mailtrap.exceptions import APIError
from mailtrap.exceptions import AuthorizationError
from mailtrap.mail.base import BaseMail


class MailtrapClient:
    DEFAULT_HOST = "send.api.mailtrap.io"
    DEFAULT_PORT = 443

    def __init__(
        self,
        token: str,
        api_host: str = DEFAULT_HOST,
        api_port: int = DEFAULT_PORT,
    ) -> None:
        self.token = token
        self.api_host = api_host
        self.api_port = api_port

    def send(self, mail: BaseMail) -> Dict[str, Union[bool, List[str]]]:
        url = f"{self.base_url}/api/send"
        response = requests.post(url, headers=self.headers, json=mail.api_data)

        if response.ok:
            data = response.json()  # type: Dict[str, Union[bool, List[str]]]
            return data

        self._handle_failed_response(response)

    @property
    def base_url(self) -> str:
        return f"https://{self.api_host.rstrip('/')}:{self.api_port}"

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "User-Agent": (
                "mailtrap-python (https://github.com/railsware/mailtrap-python)"
            ),
        }

    @staticmethod
    def _handle_failed_response(response: requests.Response) -> NoReturn:
        status_code = response.status_code
        data = response.json()

        if status_code == 401:
            raise AuthorizationError(data["errors"])

        raise APIError(status_code, data["errors"])
