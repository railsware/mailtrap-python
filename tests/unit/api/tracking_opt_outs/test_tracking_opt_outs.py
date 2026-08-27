import json
from typing import Any

import pytest
import responses

from mailtrap.api.resources.tracking_opt_outs import TrackingOptOutsApi
from mailtrap.config import GENERAL_HOST
from mailtrap.exceptions import APIError
from mailtrap.http import HttpClient
from mailtrap.models.tracking_opt_outs import CreateTrackingOptOutParams
from mailtrap.models.tracking_opt_outs import TrackingOptOut
from mailtrap.models.tracking_opt_outs import TrackingOptOutsListParams
from mailtrap.models.tracking_opt_outs import TrackingOptOutsListResponse
from tests import conftest

OPT_OUT_ID = "64d71bf3-1276-417b-86e1-8e66f138acfe"
BASE_URL = f"https://{GENERAL_HOST}/api/tracking_opt_outs"


@pytest.fixture
def tracking_opt_outs_api() -> TrackingOptOutsApi:
    return TrackingOptOutsApi(client=HttpClient(GENERAL_HOST))


@pytest.fixture
def sample_opt_out_dict() -> dict[str, Any]:
    return {
        "id": OPT_OUT_ID,
        "email": "tracked@example.com",
        "created_at": "2025-01-15T10:30:00Z",
        "domain_name": "example.com",
    }


class TestTrackingOptOutsApi:

    @pytest.mark.parametrize(
        "status_code,response_json,expected_error_message",
        [
            (
                conftest.UNAUTHORIZED_STATUS_CODE,
                conftest.UNAUTHORIZED_RESPONSE,
                conftest.UNAUTHORIZED_ERROR_MESSAGE,
            ),
            (
                conftest.FORBIDDEN_STATUS_CODE,
                conftest.FORBIDDEN_RESPONSE,
                conftest.FORBIDDEN_ERROR_MESSAGE,
            ),
            (
                conftest.RATE_LIMIT_ERROR_STATUS_CODE,
                conftest.RATE_LIMIT_ERROR_RESPONSE,
                conftest.RATE_LIMIT_ERROR_MESSAGE,
            ),
        ],
    )
    @responses.activate
    def test_get_list_should_raise_api_errors(
        self,
        tracking_opt_outs_api: TrackingOptOutsApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        responses.get(BASE_URL, status=status_code, json=response_json)

        with pytest.raises(APIError) as exc_info:
            tracking_opt_outs_api.get_list()

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_get_list_should_return_page_and_cursor(
        self, tracking_opt_outs_api: TrackingOptOutsApi, sample_opt_out_dict: dict
    ) -> None:
        responses.get(
            BASE_URL,
            json={"data": [sample_opt_out_dict], "last_id": OPT_OUT_ID},
            status=200,
        )

        result = tracking_opt_outs_api.get_list()

        assert isinstance(result, TrackingOptOutsListResponse)
        assert result.last_id == OPT_OUT_ID
        assert isinstance(result.data[0], TrackingOptOut)
        assert result.data[0].email == "tracked@example.com"
        assert result.data[0].domain_name == "example.com"

    @responses.activate
    def test_get_list_should_handle_null_cursor(
        self, tracking_opt_outs_api: TrackingOptOutsApi, sample_opt_out_dict: dict
    ) -> None:
        responses.get(
            BASE_URL,
            json={"data": [sample_opt_out_dict], "last_id": None},
            status=200,
        )

        assert tracking_opt_outs_api.get_list().last_id is None

    @responses.activate
    def test_get_list_should_pass_filters_as_query_params(
        self, tracking_opt_outs_api: TrackingOptOutsApi
    ) -> None:
        responses.get(BASE_URL, json={"data": [], "last_id": None}, status=200)

        tracking_opt_outs_api.get_list(
            TrackingOptOutsListParams(
                email="tracked@example.com",
                start_time="2025-01-01T00:00:00Z",
                end_time="2025-12-31T23:59:59Z",
                last_id=OPT_OUT_ID,
            )
        )

        query = responses.calls[0].request.params
        assert query == {
            "email": "tracked@example.com",
            "start_time": "2025-01-01T00:00:00Z",
            "end_time": "2025-12-31T23:59:59Z",
            "last_id": OPT_OUT_ID,
        }

    @responses.activate
    def test_get_list_should_omit_unset_filters(
        self, tracking_opt_outs_api: TrackingOptOutsApi
    ) -> None:
        responses.get(BASE_URL, json={"data": [], "last_id": None}, status=200)

        tracking_opt_outs_api.get_list(
            TrackingOptOutsListParams(email="tracked@example.com")
        )

        assert responses.calls[0].request.params == {"email": "tracked@example.com"}

    @pytest.mark.parametrize(
        "status_code,response_json,expected_error_message",
        [
            (
                conftest.UNAUTHORIZED_STATUS_CODE,
                conftest.UNAUTHORIZED_RESPONSE,
                conftest.UNAUTHORIZED_ERROR_MESSAGE,
            ),
            (
                conftest.VALIDATION_ERRORS_STATUS_CODE,
                {"errors": "Email is invalid"},
                "Email is invalid",
            ),
        ],
    )
    @responses.activate
    def test_create_should_raise_api_errors(
        self,
        tracking_opt_outs_api: TrackingOptOutsApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        responses.post(BASE_URL, status=status_code, json=response_json)

        with pytest.raises(APIError) as exc_info:
            tracking_opt_outs_api.create(
                CreateTrackingOptOutParams(email="tracked@example.com", domain_id=12345)
            )

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_create_should_send_flat_body_and_unwrap_data(
        self, tracking_opt_outs_api: TrackingOptOutsApi, sample_opt_out_dict: dict
    ) -> None:
        responses.post(BASE_URL, json={"data": sample_opt_out_dict}, status=201)

        opt_out = tracking_opt_outs_api.create(
            CreateTrackingOptOutParams(email="tracked@example.com", domain_id=12345)
        )

        assert isinstance(opt_out, TrackingOptOut)
        assert opt_out.id == OPT_OUT_ID
        assert json.loads(responses.calls[0].request.body) == {
            "email": "tracked@example.com",
            "domain_id": 12345,
        }

    @responses.activate
    def test_delete_should_return_deleted_opt_out_from_bare_response(
        self, tracking_opt_outs_api: TrackingOptOutsApi, sample_opt_out_dict: dict
    ) -> None:
        responses.delete(f"{BASE_URL}/{OPT_OUT_ID}", json=sample_opt_out_dict, status=200)

        opt_out = tracking_opt_outs_api.delete(OPT_OUT_ID)

        assert isinstance(opt_out, TrackingOptOut)
        assert opt_out.email == "tracked@example.com"

    @responses.activate
    def test_delete_should_raise_api_errors(
        self, tracking_opt_outs_api: TrackingOptOutsApi
    ) -> None:
        responses.delete(
            f"{BASE_URL}/{OPT_OUT_ID}",
            status=conftest.NOT_FOUND_STATUS_CODE,
            json=conftest.NOT_FOUND_RESPONSE,
        )

        with pytest.raises(APIError) as exc_info:
            tracking_opt_outs_api.delete(OPT_OUT_ID)

        assert conftest.NOT_FOUND_ERROR_MESSAGE in str(exc_info.value)
