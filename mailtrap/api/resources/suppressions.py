from typing import Optional

from mailtrap.http import HttpClient
from mailtrap.models.suppressions import Suppression


class SuppressionsApi:
    def __init__(self, client: HttpClient, account_id: str) -> None:
        self._account_id = account_id
        self._client = client

    def get_list(self, email: Optional[str] = None) -> list[Suppression]:
        """
        List and search suppressions by email.
        The endpoint returns up to 1000 suppressions per request.
        """
        params = {"email": email} if email is not None else None
        response = self._client.get(self._api_path(), params=params)
        return [Suppression(**suppression) for suppression in response]

    def delete(self, suppression_id: str) -> Suppression:
        """
        Delete a suppression by ID. Mailtrap will no longer prevent
        sending to this email unless it's recorded in suppressions again.
        """
        response = self._client.delete(self._api_path(suppression_id))
        return Suppression(**response)

    def _api_path(self, suppression_id: Optional[str] = None) -> str:
        path = f"/api/accounts/{self._account_id}/suppressions"
        if suppression_id is not None:
            return f"{path}/{suppression_id}"
        return path
