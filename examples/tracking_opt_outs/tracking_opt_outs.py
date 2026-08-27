import os

import mailtrap as mt
from mailtrap.models.tracking_opt_outs import TrackingOptOut
from mailtrap.models.tracking_opt_outs import TrackingOptOutsListResponse

API_KEY = os.environ["MAILTRAP_API_KEY"]

client = mt.MailtrapClient(token=API_KEY)
tracking_opt_outs_api = client.tracking_opt_outs_api.tracking_opt_outs


def list_tracking_opt_outs() -> TrackingOptOutsListResponse:
    return tracking_opt_outs_api.get_list()


def search_tracking_opt_outs(email: str) -> TrackingOptOutsListResponse:
    params = mt.TrackingOptOutsListParams(
        email=email,
        start_time="2025-01-01T00:00:00Z",
        end_time="2025-12-31T23:59:59Z",
    )
    return tracking_opt_outs_api.get_list(params)


def list_all_tracking_opt_outs() -> list[TrackingOptOut]:
    """Page through the full list, following the `last_id` cursor."""
    opt_outs: list[TrackingOptOut] = []
    page = tracking_opt_outs_api.get_list()
    opt_outs.extend(page.data)

    while page.last_id is not None:
        page = tracking_opt_outs_api.get_list(
            mt.TrackingOptOutsListParams(last_id=page.last_id)
        )
        opt_outs.extend(page.data)

    return opt_outs


def create_tracking_opt_out() -> TrackingOptOut:
    params = mt.CreateTrackingOptOutParams(
        email="tracked@example.com",
        domain_id=12345,
    )
    return tracking_opt_outs_api.create(params)


def delete_tracking_opt_out(tracking_opt_out_id: str) -> TrackingOptOut:
    return tracking_opt_outs_api.delete(tracking_opt_out_id)


if __name__ == "__main__":
    created = create_tracking_opt_out()
    print(created)

    page = list_tracking_opt_outs()
    print(page)

    print(search_tracking_opt_outs("tracked@example.com"))
    print(list_all_tracking_opt_outs())

    deleted = delete_tracking_opt_out(created.id)
    print(deleted)
