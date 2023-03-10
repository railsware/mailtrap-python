from mailtrap.mail.from_template import MailFromTemplate
from mailtrap.mail.mail import Address
from mailtrap.mail.mail import Attachment


class TestAttachment:
    ADDRESS = Address(email="joe@mail.com")
    ADDRESS_API_DATA = {"email": "joe@mail.com"}

    ATTACHMENT = Attachment(content=b"base64_content", filename="file.txt")
    ATTACHMENT_API_DATA = {"content": "base64_content", "filename": "file.txt"}

    def test_api_data_should_return_dict_with_required_props_only(self) -> None:
        entity = MailFromTemplate(
            sender=self.ADDRESS,
            to=[self.ADDRESS],
            template_uuid="fake_uuid",
        )
        assert entity.api_data == {
            "from": self.ADDRESS_API_DATA,
            "to": [self.ADDRESS_API_DATA],
            "template_uuid": "fake_uuid",
        }

    def test_api_data_should_return_dict_with_all_props(self) -> None:
        entity = MailFromTemplate(
            sender=self.ADDRESS,
            to=[self.ADDRESS],
            template_uuid="fake_uuid",
            template_variables={"username": "Joe"},
            cc=[self.ADDRESS],
            bcc=[self.ADDRESS],
            attachments=[self.ATTACHMENT],
            headers={"key": "value"},
            custom_variables={"var": 42},
        )

        assert entity.api_data == {
            "from": self.ADDRESS_API_DATA,
            "to": [self.ADDRESS_API_DATA],
            "template_uuid": "fake_uuid",
            "template_variables": {"username": "Joe"},
            "cc": [self.ADDRESS_API_DATA],
            "bcc": [self.ADDRESS_API_DATA],
            "attachments": [self.ATTACHMENT_API_DATA],
            "headers": {"key": "value"},
            "custom_variables": {"var": 42},
        }
