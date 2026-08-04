import os

import mailtrap as mt
from mailtrap.models.billing import BillingCycleUsage

API_KEY = os.environ["MAILTRAP_API_KEY"]
ACCOUNT_ID = os.environ["MAILTRAP_ACCOUNT_ID"]

client = mt.MailtrapClient(token=API_KEY)
billing_api = client.general_api.billing


def get_current_billing_usage(account_id: int) -> BillingCycleUsage:
    return billing_api.get_current_billing_usage(account_id=account_id)


if __name__ == "__main__":
    usage = get_current_billing_usage(ACCOUNT_ID)
    print(usage)
