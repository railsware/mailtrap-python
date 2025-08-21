from mailtrap.http import HttpClient
from mailtrap.models.common import DeletedObject
from mailtrap.models.templates import CreateEmailTemplateParams
from mailtrap.models.templates import EmailTemplate
from mailtrap.models.templates import UpdateEmailTemplateParams


class TemplatesApi:
    def __init__(self, client: HttpClient, account_id: str) -> None:
        self._account_id = account_id
        self._client = client

    def get_list(self) -> list[EmailTemplate]:
        response = self._client.get(f"/api/accounts/{self._account_id}/email_templates")
        return [EmailTemplate(**template) for template in response]

    def get_by_id(self, template_id: int) -> EmailTemplate:
        response = self._client.get(
            f"/api/accounts/{self._account_id}/email_templates/{template_id}"
        )
        return EmailTemplate(**response)

    def create(self, template_params: CreateEmailTemplateParams) -> EmailTemplate:
        response = self._client.post(
            f"/api/accounts/{self._account_id}/email_templates",
            json={"email_template": template_params.api_data},
        )
        return EmailTemplate(**response)

    def update(
        self, template_id: int, template_params: UpdateEmailTemplateParams
    ) -> EmailTemplate:
        response = self._client.patch(
            f"/api/accounts/{self._account_id}/email_templates/{template_id}",
            json={"email_template": template_params.api_data},
        )
        return EmailTemplate(**response)

    def delete(self, template_id: int) -> DeletedObject:
        self._client.delete(
            f"/api/accounts/{self._account_id}/email_templates/{template_id}"
        )
        return DeletedObject(template_id)
