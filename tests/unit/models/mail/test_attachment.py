from mailtrap.models.mail.attachment import Attachment
from mailtrap.models.mail.attachment import Disposition


class TestAttachment:
    def test_api_data_should_return_dict_with_required_props_only(self) -> None:
        entity = Attachment(content=b"base64_content", filename="photo.jpg")
        assert entity.api_data == {"content": "base64_content", "filename": "photo.jpg"}

    def test_api_data_should_return_dict_with_all_props(self) -> None:
        entity = Attachment(
            content=b"base64_content",
            filename="photo.jpg",
            disposition=Disposition.INLINE,
            mimetype="image/jpg",
            content_id="test_id",
        )
        assert entity.api_data == {
            "content": "base64_content",
            "filename": "photo.jpg",
            "type": "image/jpg",
            "disposition": "inline",
            "content_id": "test_id",
        }
