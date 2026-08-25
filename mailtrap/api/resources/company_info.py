from mailtrap.http import HttpClient
from mailtrap.models.company_info import CompanyInfo
from mailtrap.models.company_info import CompanyInfoResponse
from mailtrap.models.company_info import CreateCompanyInfoParams
from mailtrap.models.company_info import UpdateCompanyInfoParams


class CompanyInfoApi:
    def __init__(self, client: HttpClient, account_id: str) -> None:
        self._account_id = account_id
        self._client = client

    def get(self, sending_domain_id: int) -> CompanyInfo:
        """
        Get the company info associated with a sending domain.
        """
        response = self._client.get(self._api_path(sending_domain_id))
        return CompanyInfoResponse(**response).data

    def create(
        self, sending_domain_id: int, company_info_params: CreateCompanyInfoParams
    ) -> CompanyInfo:
        """
        Create the company info for a sending domain. Company info is required
        for domain compliance verification.
        """
        response = self._client.post(
            self._api_path(sending_domain_id),
            json={"company_info": company_info_params.api_data},
        )
        return CompanyInfoResponse(**response).data

    def update(
        self, sending_domain_id: int, company_info_params: UpdateCompanyInfoParams
    ) -> CompanyInfo:
        """
        Update the company info for a sending domain. Only the fields supplied
        in `company_info_params` are sent to the API.
        """
        response = self._client.patch(
            self._api_path(sending_domain_id),
            json={"company_info": company_info_params.api_data},
        )
        return CompanyInfoResponse(**response).data

    def _api_path(self, sending_domain_id: int) -> str:
        return (
            f"/api/accounts/{self._account_id}"
            f"/sending_domains/{sending_domain_id}/company_info"
        )
