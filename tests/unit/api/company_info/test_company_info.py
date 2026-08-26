import json
from typing import Any

import pytest
import responses

from mailtrap.api.resources.company_info import CompanyInfoApi
from mailtrap.config import GENERAL_HOST
from mailtrap.exceptions import APIError
from mailtrap.http import HttpClient
from mailtrap.models.company_info import CompanyInfo
from mailtrap.models.company_info import CreateCompanyInfoParams
from mailtrap.models.company_info import UpdateCompanyInfoParams
from tests import conftest

DOMAIN_ID = 432
COMPANY_INFO_URL = f"https://{GENERAL_HOST}/api/domains/{DOMAIN_ID}/company_info"


@pytest.fixture
def company_info_api() -> CompanyInfoApi:
    return CompanyInfoApi(client=HttpClient(GENERAL_HOST))


@pytest.fixture
def sample_company_info_dict() -> dict[str, Any]:
    return {
        "name": "Mailtrap",
        "address": "123 Main St",
        "city": "San Francisco",
        "country": "US",
        "phone": "+1-555-0100",
        "zip_code": "94105",
        "privacy_policy_url": "https://mailtrap.io/privacy",
        "terms_of_service_url": "https://mailtrap.io/terms",
        "website_url": "https://mailtrap.io",
        "info_level": "business",
    }


class TestCompanyInfoApi:

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
                conftest.NOT_FOUND_STATUS_CODE,
                conftest.NOT_FOUND_RESPONSE,
                conftest.NOT_FOUND_ERROR_MESSAGE,
            ),
            (
                conftest.INTERNAL_SERVER_ERROR_STATUS_CODE,
                conftest.INTERNAL_SERVER_ERROR_RESPONSE,
                conftest.INTERNAL_SERVER_ERROR_MESSAGE,
            ),
        ],
    )
    @responses.activate
    def test_get_company_info_should_raise_api_errors(
        self,
        company_info_api: CompanyInfoApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        responses.get(COMPANY_INFO_URL, status=status_code, json=response_json)

        with pytest.raises(APIError) as exc_info:
            company_info_api.get(DOMAIN_ID)

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_get_company_info_should_return_company_info(
        self, company_info_api: CompanyInfoApi, sample_company_info_dict: dict
    ) -> None:
        responses.get(
            COMPANY_INFO_URL,
            json={"data": sample_company_info_dict},
            status=200,
        )

        company_info = company_info_api.get(DOMAIN_ID)

        assert isinstance(company_info, CompanyInfo)
        assert company_info.name == "Mailtrap"
        assert company_info.city == "San Francisco"
        assert company_info.info_level == "business"

    @responses.activate
    def test_get_company_info_should_handle_unset_fields(
        self, company_info_api: CompanyInfoApi
    ) -> None:
        responses.get(
            COMPANY_INFO_URL,
            json={"data": {"info_level": "individual", "name": None}},
            status=200,
        )

        company_info = company_info_api.get(DOMAIN_ID)

        assert isinstance(company_info, CompanyInfo)
        assert company_info.info_level == "individual"
        assert company_info.name is None
        assert company_info.website_url is None

    @pytest.mark.parametrize(
        "status_code,response_json,expected_error_message",
        [
            (
                conftest.UNAUTHORIZED_STATUS_CODE,
                conftest.UNAUTHORIZED_RESPONSE,
                conftest.UNAUTHORIZED_ERROR_MESSAGE,
            ),
            (
                conftest.NOT_FOUND_STATUS_CODE,
                conftest.NOT_FOUND_RESPONSE,
                conftest.NOT_FOUND_ERROR_MESSAGE,
            ),
            (
                conftest.VALIDATION_ERRORS_STATUS_CODE,
                {"errors": "Website url is invalid"},
                "Website url is invalid",
            ),
        ],
    )
    @responses.activate
    def test_create_company_info_should_raise_api_errors(
        self,
        company_info_api: CompanyInfoApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        responses.post(COMPANY_INFO_URL, status=status_code, json=response_json)

        with pytest.raises(APIError) as exc_info:
            params = CreateCompanyInfoParams(
                name="Mailtrap",
                address="123 Main St",
                city="San Francisco",
                country="US",
                zip_code="94105",
                website_url="not-a-url",
            )
            company_info_api.create(DOMAIN_ID, params)

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_create_company_info_should_return_created_company_info(
        self, company_info_api: CompanyInfoApi, sample_company_info_dict: dict
    ) -> None:
        responses.post(
            COMPANY_INFO_URL,
            json={"data": sample_company_info_dict},
            status=200,
        )

        params = CreateCompanyInfoParams(
            name="Mailtrap",
            address="123 Main St",
            city="San Francisco",
            country="US",
            zip_code="94105",
            website_url="https://mailtrap.io",
            info_level="business",
        )
        company_info = company_info_api.create(DOMAIN_ID, params)

        assert isinstance(company_info, CompanyInfo)
        assert company_info.name == "Mailtrap"
        assert responses.calls[0].request.body is not None
        assert json.loads(responses.calls[0].request.body) == {
            "company_info": {
                "name": "Mailtrap",
                "address": "123 Main St",
                "city": "San Francisco",
                "country": "US",
                "zip_code": "94105",
                "website_url": "https://mailtrap.io",
                "info_level": "business",
            }
        }

    @pytest.mark.parametrize(
        "status_code,response_json,expected_error_message",
        [
            (
                conftest.UNAUTHORIZED_STATUS_CODE,
                conftest.UNAUTHORIZED_RESPONSE,
                conftest.UNAUTHORIZED_ERROR_MESSAGE,
            ),
            (
                conftest.NOT_FOUND_STATUS_CODE,
                conftest.NOT_FOUND_RESPONSE,
                conftest.NOT_FOUND_ERROR_MESSAGE,
            ),
            (
                conftest.VALIDATION_ERRORS_STATUS_CODE,
                {"errors": "Zip code is invalid"},
                "Zip code is invalid",
            ),
        ],
    )
    @responses.activate
    def test_update_company_info_should_raise_api_errors(
        self,
        company_info_api: CompanyInfoApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        responses.patch(COMPANY_INFO_URL, status=status_code, json=response_json)

        with pytest.raises(APIError) as exc_info:
            params = UpdateCompanyInfoParams(zip_code="")
            company_info_api.update(DOMAIN_ID, params)

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_update_company_info_should_send_only_supplied_fields(
        self, company_info_api: CompanyInfoApi, sample_company_info_dict: dict
    ) -> None:
        sample_company_info_dict["city"] = "New York"
        sample_company_info_dict["zip_code"] = "10001"
        responses.patch(
            COMPANY_INFO_URL,
            json={"data": sample_company_info_dict},
            status=200,
        )

        params = UpdateCompanyInfoParams(city="New York", zip_code="10001")
        company_info = company_info_api.update(DOMAIN_ID, params)

        assert isinstance(company_info, CompanyInfo)
        assert company_info.city == "New York"
        assert company_info.zip_code == "10001"
        assert responses.calls[0].request.body is not None
        assert json.loads(responses.calls[0].request.body) == {
            "company_info": {"city": "New York", "zip_code": "10001"}
        }
