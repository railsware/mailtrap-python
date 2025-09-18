from typing import Any
from typing import Optional
from typing import cast

from mailtrap.http import HttpClient
from mailtrap.models.messages import AnalysisReport
from mailtrap.models.messages import AnalysisReportResponse
from mailtrap.models.messages import EmailMessage
from mailtrap.models.messages import ForwardedMessage
from mailtrap.models.messages import SpamReport
from mailtrap.models.messages import UpdateEmailMessageParams


class MessagesApi:
    def __init__(self, client: HttpClient, account_id: str) -> None:
        self._account_id = account_id
        self._client = client

    def show_message(self, inbox_id: int, message_id: int) -> EmailMessage:
        """Get email message by ID."""
        response = self._client.get(self._api_path(inbox_id, message_id))
        return EmailMessage(**response)

    def update(
        self, inbox_id: int, message_id: int, message_params: UpdateEmailMessageParams
    ) -> EmailMessage:
        """
        Update message attributes
        (right now only the **is_read** attribute is available for modification).
        """
        response = self._client.patch(
            self._api_path(inbox_id, message_id),
            json={"message": message_params.api_data},
        )
        return EmailMessage(**response)

    def delete(self, inbox_id: int, message_id: int) -> EmailMessage:
        """Delete message from inbox."""
        response = self._client.delete(self._api_path(inbox_id, message_id))
        return EmailMessage(**response)

    def get_list(
        self,
        inbox_id: int,
        search: Optional[str] = None,
        last_id: Optional[int] = None,
        page: Optional[int] = None,
    ) -> list[EmailMessage]:
        """
        Get messages from the inbox.

        The response contains up to 30 messages per request. You can use pagination
        parameters (`last_id` or `page`) to retrieve additional results.

        Args:
            inbox_id (int): ID of the inbox to retrieve messages from.
            search (Optional[str]):
                Search query string. Matches `subject`, `to_email`, and `to_name`.
                Example: `"welcome"`
            last_id (Optional[int]):
                If specified, returns a page of records before the given `last_id`.
                Overrides `page` if both are provided.
                Must be `>= 1`.
                Example: `123`
            page (Optional[int]):
                Page number for paginated results.
                Ignored if `last_id` is also provided.
                Must be `>= 1`.
                Example: `5`

        Returns:
            list[EmailMessage]: A list of email messages.

        Notes:
            - Only one of `last_id` or `page` should typically be used.
            - `last_id` has higher priority if both are provided.
            - Each response contains at most 30 messages.
        """
        params: dict[str, Any] = {}
        if search:
            params["search"] = search
        if last_id:
            params["last_id"] = last_id
        if page:
            params["page"] = page

        response = self._client.get(self._api_path(inbox_id), params=params)
        return [EmailMessage(**message) for message in response]

    def forward(self, inbox_id: int, message_id: int, email: str) -> ForwardedMessage:
        """
        Forward message to an email address.
        The email address must be confirmed by the recipient in advance.
        """
        response = self._client.post(
            f"{self._api_path(inbox_id, message_id)}/forward", json={"email": email}
        )
        return ForwardedMessage(**response)

    def get_spam_report(self, inbox_id: int, message_id: int) -> SpamReport:
        """Get a brief spam report by message ID."""
        response = self._client.get(f"{self._api_path(inbox_id, message_id)}/spam_report")
        return SpamReport(**response["report"])

    def get_html_analysis(self, inbox_id: int, message_id: int) -> AnalysisReport:
        """Get a brief HTML report by message ID."""
        response = self._client.get(f"{self._api_path(inbox_id, message_id)}/analyze")
        return AnalysisReportResponse(**response).report

    def get_text_message(self, inbox_id: int, message_id: int) -> str:
        """Get text email body, if it exists."""
        return cast(
            str, self._client.get(f"{self._api_path(inbox_id, message_id)}/body.txt")
        )

    def get_raw_message(self, inbox_id: int, message_id: int) -> str:
        """Get raw email body."""
        return cast(
            str, self._client.get(f"{self._api_path(inbox_id, message_id)}/body.raw")
        )

    def get_html_source(self, inbox_id: int, message_id: int) -> str:
        """Get HTML source of email."""
        return cast(
            str,
            self._client.get(f"{self._api_path(inbox_id, message_id)}/body.htmlsource"),
        )

    def get_html_message(self, inbox_id: int, message_id: int) -> str:
        """Get formatted HTML email body. Not applicable for plain text emails."""
        return cast(
            str, self._client.get(f"{self._api_path(inbox_id, message_id)}/body.html")
        )

    def get_message_as_eml(self, inbox_id: int, message_id: int) -> str:
        """Get email message in .eml format."""
        return cast(
            str, self._client.get(f"{self._api_path(inbox_id, message_id)}/body.eml")
        )

    def get_mail_headers(self, inbox_id: int, message_id: int) -> dict[str, Any]:
        """Get mail headers of a message."""
        response = self._client.get(
            f"{self._api_path(inbox_id, message_id)}/mail_headers"
        )
        return cast(dict[str, Any], response["headers"])

    def _api_path(self, inbox_id: int, message_id: Optional[int] = None) -> str:
        path = f"/api/accounts/{self._account_id}/inboxes/{inbox_id}/messages"
        if message_id:
            return f"{path}/{message_id}"
        return path
