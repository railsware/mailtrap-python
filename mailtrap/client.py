from typing import Any
from typing import NoReturn
from typing import Optional
from typing import Union

import requests

from mailtrap.exceptions import APIError
from mailtrap.exceptions import AuthorizationError
from mailtrap.exceptions import ClientConfigurationError
from mailtrap.mail.base import BaseMail


class MailtrapClient:
    DEFAULT_HOST = "send.api.mailtrap.io"
    DEFAULT_PORT = 443
    BULK_HOST = "bulk.api.mailtrap.io"
    SANDBOX_HOST = "sandbox.api.mailtrap.io"
    TEMPLATES_HOST = "mailtrap.io"

    def __init__(
        self,
        token: str,
        api_host: Optional[str] = None,
        api_port: int = DEFAULT_PORT,
        app_host: Optional[str] = None,
        bulk: bool = False,
        sandbox: bool = False,
        inbox_id: Optional[str] = None,
    ) -> None:
        self.token = token
        self.api_host = api_host
        self.api_port = api_port
        self.app_host = app_host
        self.bulk = bulk
        self.sandbox = sandbox
        self.inbox_id = inbox_id

        self._validate_itself()

    def send(self, mail: BaseMail) -> dict[str, Union[bool, list[str]]]:
        response = requests.post(
            self.api_send_url, headers=self.headers, json=mail.api_data
        )

        if response.ok:
            data: dict[str, Union[bool, list[str]]] = response.json()
            return data

        self._handle_failed_response(response)

    def email_templates(self, account_id: int) -> list[dict[str, Any]]:
        response = requests.get(self._templates_url(account_id), headers=self.headers)

        if response.ok:
            data: list[dict[str, Any]] = response.json()
            return data

        self._handle_failed_response(response)

    def create_email_template(
        self, account_id: int, data: dict[str, Any]
    ) -> dict[str, Any]:
        response = requests.post(
            self._templates_url(account_id), headers=self.headers, json=data
        )

        if response.status_code == 201:
            return response.json()

        self._handle_failed_response(response)

    def update_email_template(
        self, account_id: int, template_id: int, data: dict[str, Any]
    ) -> dict[str, Any]:
        response = requests.patch(
            self._templates_url(account_id, template_id),
            headers=self.headers,
            json=data,
        )

        if response.ok:
            return response.json()

        self._handle_failed_response(response)

    def delete_email_template(self, account_id: int, template_id: int) -> None:
        response = requests.delete(
            self._templates_url(account_id, template_id), headers=self.headers
        )

        if response.status_code == 204:
            return None

        self._handle_failed_response(response)

    @property
    def base_url(self) -> str:
        return f"https://{self._host.rstrip('/')}:{self.api_port}"

    @property
    def app_base_url(self) -> str:
        host = self.app_host if self.app_host else self.TEMPLATES_HOST
        return f"https://{host.rstrip('/')}"

    @property
    def api_send_url(self) -> str:
        url = f"{self.base_url}/api/send"
        if self.sandbox and self.inbox_id:
            return f"{url}/{self.inbox_id}"

        return url

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "User-Agent": (
                "mailtrap-python (https://github.com/railsware/mailtrap-python)"
            ),
        }

    def _templates_url(self, account_id: int, template_id: Optional[int] = None) -> str:
        url = f"{self.app_base_url}/api/accounts/{account_id}/email_templates"
        if template_id is not None:
            url = f"{url}/{template_id}"
        return url

    @property
    def _host(self) -> str:
        if self.api_host:
            return self.api_host
        if self.sandbox:
            return self.SANDBOX_HOST
        if self.bulk:
            return self.BULK_HOST
        return self.DEFAULT_HOST

    @staticmethod
    def _handle_failed_response(response: requests.Response) -> NoReturn:
        status_code = response.status_code
        data = response.json()

        if status_code == 401:
            raise AuthorizationError(data["errors"])

        raise APIError(status_code, data["errors"])

    def _validate_itself(self) -> None:
        if self.sandbox and not self.inbox_id:
            raise ClientConfigurationError("`inbox_id` is required for sandbox mode")

        if not self.sandbox and self.inbox_id:
            raise ClientConfigurationError(
                "`inbox_id` is not allowed in non-sandbox mode"
            )

        if self.bulk and self.sandbox:
            raise ClientConfigurationError("bulk mode is not allowed in sandbox mode")
