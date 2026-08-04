import os

import mailtrap as mt
from mailtrap.models.accounts import Account

API_KEY = os.environ["MAILTRAP_API_KEY"]

client = mt.MailtrapClient(token=API_KEY)
accounts_api = client.general_api.accounts


def get_accounts() -> list[Account]:
    return accounts_api.get_list()


if __name__ == "__main__":
    accounts = get_accounts()
    print(accounts)
