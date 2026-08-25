import os

import mailtrap as mt
from mailtrap.models.company_info import CompanyInfo

API_KEY = os.environ["MAILTRAP_API_KEY"]
ACCOUNT_ID = os.environ["MAILTRAP_ACCOUNT_ID"]
DOMAIN_ID = int(os.environ["MAILTRAP_DOMAIN_ID"])

client = mt.MailtrapClient(token=API_KEY, account_id=ACCOUNT_ID)
company_info_api = client.sending_domains_api.company_info


def get_company_info(domain_id: int) -> CompanyInfo:
    return company_info_api.get(domain_id)


def create_company_info(domain_id: int) -> CompanyInfo:
    params = mt.CreateCompanyInfoParams(
        name="Mailtrap",
        address="123 Main St",
        city="San Francisco",
        country="US",
        zip_code="94105",
        website_url="https://mailtrap.io",
        phone="+1-555-0100",
        privacy_policy_url="https://mailtrap.io/privacy",
        terms_of_service_url="https://mailtrap.io/terms",
        info_level="business",
    )
    return company_info_api.create(domain_id, params)


def update_company_info(domain_id: int) -> CompanyInfo:
    params = mt.UpdateCompanyInfoParams(city="New York", zip_code="10001")
    return company_info_api.update(domain_id, params)


if __name__ == "__main__":
    created = create_company_info(DOMAIN_ID)
    print(created)

    company_info = get_company_info(DOMAIN_ID)
    print(company_info)

    updated = update_company_info(DOMAIN_ID)
    print(updated)
