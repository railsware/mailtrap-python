from typing import Optional

from pydantic.dataclasses import dataclass

from mailtrap.models.common import RequestParams


@dataclass
class CompanyInfo:
    info_level: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    zip_code: Optional[str] = None
    privacy_policy_url: Optional[str] = None
    terms_of_service_url: Optional[str] = None
    website_url: Optional[str] = None


@dataclass
class CompanyInfoResponse:
    data: CompanyInfo


@dataclass
class CreateCompanyInfoParams(RequestParams):
    name: str
    address: str
    city: str
    country: str
    zip_code: str
    website_url: str
    phone: Optional[str] = None
    privacy_policy_url: Optional[str] = None
    terms_of_service_url: Optional[str] = None
    info_level: Optional[str] = None


@dataclass
class UpdateCompanyInfoParams(RequestParams):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    zip_code: Optional[str] = None
    privacy_policy_url: Optional[str] = None
    terms_of_service_url: Optional[str] = None
    website_url: Optional[str] = None
    info_level: Optional[str] = None
