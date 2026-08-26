from mailtrap.api.resources.tracking_opt_outs import TrackingOptOutsApi
from mailtrap.http import HttpClient


class TrackingOptOutsBaseApi:
    def __init__(self, client: HttpClient) -> None:
        self._client = client

    @property
    def tracking_opt_outs(self) -> TrackingOptOutsApi:
        return TrackingOptOutsApi(client=self._client)
