from typing import Optional

from mailtrap.http import HttpClient
from mailtrap.models.inboxes import CreateInboxParams
from mailtrap.models.inboxes import Inbox
from mailtrap.models.inboxes import UpdateInboxParams


class InboxesApi:
    def __init__(self, client: HttpClient, account_id: str) -> None:
        self._account_id = account_id
        self._client = client

    def get_list(self) -> list[Inbox]:
        """Get a list of inboxes."""
        response = self._client.get(self._api_path())
        return [Inbox(**inbox) for inbox in response]

    def get_by_id(self, inbox_id: int) -> Inbox:
        """Get inbox attributes by inbox id."""
        response = self._client.get(self._api_path(inbox_id))
        return Inbox(**response)

    def create(self, project_id: int, inbox_params: CreateInboxParams) -> Inbox:
        """Create an inbox in a project."""
        response = self._client.post(
            f"/api/accounts/{self._account_id}/projects/{project_id}/inboxes",
            json={"inbox": inbox_params.api_data},
        )
        return Inbox(**response)

    def update(self, inbox_id: int, inbox_params: UpdateInboxParams) -> Inbox:
        """Update inbox name, inbox email username."""
        response = self._client.patch(
            self._api_path(inbox_id),
            json={"inbox": inbox_params.api_data},
        )
        return Inbox(**response)

    def delete(self, inbox_id: int) -> Inbox:
        """Delete an inbox with all its emails."""
        response = self._client.delete(self._api_path(inbox_id))
        return Inbox(**response)

    def clean(self, inbox_id: int) -> Inbox:
        """Delete all messages (emails) from inbox."""
        response = self._client.patch(f"{self._api_path(inbox_id)}/clean")
        return Inbox(**response)

    def mark_as_read(self, inbox_id: int) -> Inbox:
        """Mark all messages in the inbox as read."""
        response = self._client.patch(f"{self._api_path(inbox_id)}/all_read")
        return Inbox(**response)

    def reset_credentials(self, inbox_id: int) -> Inbox:
        """Reset SMTP credentials of the inbox."""
        response = self._client.patch(f"{self._api_path(inbox_id)}/reset_credentials")
        return Inbox(**response)

    def enable_email_address(self, inbox_id: int) -> Inbox:
        """Turn the email address of the inbox on/off."""
        response = self._client.patch(f"{self._api_path(inbox_id)}/toggle_email_username")
        return Inbox(**response)

    def reset_email_username(self, inbox_id: int) -> Inbox:
        """Reset username of email address per inbox."""
        response = self._client.patch(f"{self._api_path(inbox_id)}/reset_email_username")
        return Inbox(**response)

    def _api_path(self, inbox_id: Optional[int] = None) -> str:
        path = f"/api/accounts/{self._account_id}/inboxes"
        if inbox_id:
            return f"{path}/{inbox_id}"
        return path
