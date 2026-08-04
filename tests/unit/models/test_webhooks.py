from mailtrap.models.webhooks import CreateWebhookParams
from mailtrap.models.webhooks import UpdateWebhookParams
from mailtrap.models.webhooks import Webhook


class TestWebhook:
    def test_parses_inbound_receiving_webhook(self) -> None:
        webhook = Webhook(
            id=1,
            url="https://example.com/hook",
            active=True,
            webhook_type="inbound_receiving",
            payload_format="json",
            inbound_inbox_id=665,
        )
        assert webhook.webhook_type == "inbound_receiving"
        assert webhook.inbound_inbox_id == 665

    def test_inbound_inbox_id_defaults_to_none(self) -> None:
        webhook = Webhook(
            id=1,
            url="https://example.com/hook",
            active=True,
            webhook_type="email_sending",
            payload_format="json",
        )
        assert webhook.inbound_inbox_id is None


class TestCreateWebhookParams:
    def test_api_data_includes_inbound_inbox_id(self) -> None:
        params = CreateWebhookParams(
            url="https://example.com/hook",
            webhook_type="inbound_receiving",
            inbound_inbox_id=665,
        )
        assert params.api_data == {
            "url": "https://example.com/hook",
            "webhook_type": "inbound_receiving",
            "inbound_inbox_id": 665,
        }


class TestUpdateWebhookParams:
    def test_api_data_includes_inbound_inbox_id(self) -> None:
        params = UpdateWebhookParams(inbound_inbox_id=665)
        assert params.api_data == {"inbound_inbox_id": 665}
