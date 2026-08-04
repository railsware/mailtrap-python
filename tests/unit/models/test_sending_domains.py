from mailtrap.models.sending_domains import CreateSendingDomainParams
from mailtrap.models.sending_domains import SendingDomain
from mailtrap.models.sending_domains import SendSetupInstructionsParams


def _sending_domain_dict() -> dict:
    return {
        "id": 1,
        "domain_name": "example.com",
        "demo": False,
        "compliance_status": "verified",
        "dns_verified": True,
        "open_tracking_enabled": True,
        "click_tracking_enabled": True,
        "auto_unsubscribe_link_enabled": False,
        "custom_domain_tracking_enabled": False,
        "health_alerts_enabled": True,
        "critical_alerts_enabled": True,
        "permissions": {
            "can_read": True,
            "can_update": True,
            "can_destroy": True,
        },
    }


class TestSendingDomain:
    def test_parses_inbound_flags_when_present(self) -> None:
        data = {
            **_sending_domain_dict(),
            "inbound_enabled": True,
            "inbound_verified": False,
        }
        domain = SendingDomain(**data)
        assert domain.inbound_enabled is True
        assert domain.inbound_verified is False

    def test_inbound_flags_default_when_absent(self) -> None:
        domain = SendingDomain(**_sending_domain_dict())
        assert domain.inbound_enabled is None
        assert domain.inbound_verified is None


class TestCreateSendingDomainParams:
    def test_api_data_should_return_dict_with_all_props(self) -> None:
        entity = CreateSendingDomainParams(domain_name="test.co")
        assert entity.api_data == {"domain_name": "test.co"}


class TestSendSetupInstructionsParams:
    def test_api_data_should_return_dict_with_all_props(self) -> None:
        entity = SendSetupInstructionsParams(email="example@mail.com")
        assert entity.api_data == {"email": "example@mail.com"}
