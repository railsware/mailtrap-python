import os

import mailtrap as mt
from mailtrap.models.common import DeletedObject
from mailtrap.models.inbound import InboundFolder

API_KEY = os.environ["MAILTRAP_API_KEY"]

client = mt.MailtrapClient(token=API_KEY)
folders_api = client.inbound_api.folders


def list_folders() -> list[InboundFolder]:
    return folders_api.get_list()


def get_folder(folder_id: int) -> InboundFolder:
    return folders_api.get_by_id(folder_id)


def create_folder(name: str) -> InboundFolder:
    return folders_api.create(mt.CreateInboundFolderParams(name=name))


def update_folder(folder_id: int, name: str) -> InboundFolder:
    return folders_api.update(folder_id, mt.UpdateInboundFolderParams(name=name))


def delete_folder(folder_id: int) -> DeletedObject:
    return folders_api.delete(folder_id)


if __name__ == "__main__":
    folder = create_folder("Support")
    print(folder)

    print(list_folders())
    print(get_folder(folder.id))
    print(update_folder(folder.id, "Support (renamed)"))
    print(delete_folder(folder.id))
