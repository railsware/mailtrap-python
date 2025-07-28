from typing import List, cast

from mailtrap.api.base import LIST_RESPONSE_TYPE, RESPONSE_TYPE, BaseHttpApiClient, HttpMethod
from mailtrap.constants import MAILTRAP_HOST
from mailtrap.models.common import DeletedObject
from mailtrap.models.projects import Project


class ProjectsApiClient(BaseHttpApiClient):

    def _build_url(self, account_id: str, *parts: str) -> str:
        base_url = f"https://{MAILTRAP_HOST}/api/accounts/{account_id}/projects"
        return "/".join([base_url, *parts])

    def get_list(self, account_id: str) -> List[Project]:
        response: LIST_RESPONSE_TYPE = cast(LIST_RESPONSE_TYPE, self._request(
            HttpMethod.GET, 
            self._build_url(account_id)
        ))
        return [Project.from_dict(proj) for proj in response]

    def get_by_id(self, account_id: str, project_id: str) -> Project:
        response: RESPONSE_TYPE = cast(RESPONSE_TYPE, self._request(
            HttpMethod.GET, 
            self._build_url(account_id, project_id)
        ))
        return Project.from_dict(response)
    
    def create(self, account_id: str, name: str) -> Project:
        response: RESPONSE_TYPE = cast(RESPONSE_TYPE, self._request(
            HttpMethod.POST, 
            self._build_url(account_id), 
            json={"project": {"name": name}},
        ))
        return Project.from_dict(response)
    
    def update(self, account_id: str, project_id: str, name: str) -> Project:
        response: RESPONSE_TYPE = cast(RESPONSE_TYPE, self._request(
            HttpMethod.PATCH, 
            self._build_url(account_id, project_id), 
            json={"project": {"name": name}},
        ))
        return Project.from_dict(response)
    
    def delete(self, account_id: str, project_id: str) -> DeletedObject:
        response: RESPONSE_TYPE = cast(RESPONSE_TYPE, self._request(
            HttpMethod.DELTE, 
            self._build_url(account_id, project_id),
        ))
        return DeletedObject(response["id"])
