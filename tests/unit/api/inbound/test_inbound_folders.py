import pytest
import responses

from mailtrap.api.resources.inbound_folders import InboundFoldersApi
from mailtrap.config import GENERAL_HOST
from mailtrap.exceptions import APIError
from mailtrap.http import HttpClient
from mailtrap.models.common import DeletedObject
from mailtrap.models.inbound import CreateInboundFolderParams
from mailtrap.models.inbound import InboundFolder
from mailtrap.models.inbound import UpdateInboundFolderParams
from tests import conftest

FOLDER_ID = 42
BASE_URL = f"https://{GENERAL_HOST}/api/inbound/folders"

ERROR_CASES = [
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
]


@pytest.fixture
def folders_api() -> InboundFoldersApi:
    return InboundFoldersApi(client=HttpClient(GENERAL_HOST))


class TestInboundFoldersApi:

    @responses.activate
    def test_get_list_should_return_folders(self, folders_api: InboundFoldersApi) -> None:
        responses.get(BASE_URL, json=[{"id": FOLDER_ID, "name": "Support"}], status=200)

        folders = folders_api.get_list()

        assert all(isinstance(f, InboundFolder) for f in folders)
        assert folders[0].id == FOLDER_ID
        assert folders[0].name == "Support"

    @pytest.mark.parametrize(
        "status_code,response_json,expected_error_message", ERROR_CASES
    )
    @responses.activate
    def test_get_list_should_raise_api_errors(
        self,
        folders_api: InboundFoldersApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        responses.get(BASE_URL, status=status_code, json=response_json)

        with pytest.raises(APIError) as exc_info:
            folders_api.get_list()

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_get_by_id_should_return_folder(self, folders_api: InboundFoldersApi) -> None:
        responses.get(
            f"{BASE_URL}/{FOLDER_ID}",
            json={"id": FOLDER_ID, "name": "Support"},
            status=200,
        )

        folder = folders_api.get_by_id(FOLDER_ID)

        assert isinstance(folder, InboundFolder)
        assert folder.id == FOLDER_ID

    @responses.activate
    def test_create_should_return_folder(self, folders_api: InboundFoldersApi) -> None:
        responses.post(BASE_URL, json={"id": FOLDER_ID, "name": "Support"}, status=200)

        folder = folders_api.create(CreateInboundFolderParams(name="Support"))

        assert folder.id == FOLDER_ID
        assert responses.calls[-1].request.body == b'{"name": "Support"}'

    @responses.activate
    def test_update_should_return_folder(self, folders_api: InboundFoldersApi) -> None:
        responses.patch(
            f"{BASE_URL}/{FOLDER_ID}",
            json={"id": FOLDER_ID, "name": "Renamed"},
            status=200,
        )

        folder = folders_api.update(FOLDER_ID, UpdateInboundFolderParams(name="Renamed"))

        assert folder.name == "Renamed"

    @responses.activate
    def test_delete_should_return_deleted_object(
        self, folders_api: InboundFoldersApi
    ) -> None:
        responses.delete(f"{BASE_URL}/{FOLDER_ID}", status=204)

        deleted = folders_api.delete(FOLDER_ID)

        assert isinstance(deleted, DeletedObject)
        assert deleted.id == FOLDER_ID
