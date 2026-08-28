import os
from datetime import datetime
from datetime import timedelta
from datetime import timezone

import mailtrap as mt
from mailtrap.models.api_tokens import ApiToken
from mailtrap.models.api_tokens import ApiTokenWithToken
from mailtrap.models.common import DeletedObject

API_KEY = os.environ["MAILTRAP_API_KEY"]
ACCOUNT_ID = os.environ["MAILTRAP_ACCOUNT_ID"]

client = mt.MailtrapClient(token=API_KEY)
api_tokens_api = client.general_api.api_tokens


def one_year_from_now() -> str:
    return (datetime.now(timezone.utc) + timedelta(days=365)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def list_api_tokens(account_id: int) -> list[ApiToken]:
    return api_tokens_api.get_list(account_id=account_id)


def get_api_token(account_id: int, api_token_id: int) -> ApiToken:
    return api_tokens_api.get_by_id(account_id=account_id, api_token_id=api_token_id)


def create_api_token(account_id: int) -> ApiTokenWithToken:
    # The full token value is only returned once on the response — store it securely.
    # Omit expires_at for the server default expiration.
    return api_tokens_api.create(
        account_id=account_id,
        token_params=mt.CreateApiTokenParams(
            name="My API Token",
            resources=[
                mt.ApiTokenResource(
                    resource_type="account",
                    resource_id=account_id,
                    access_level=100,
                )
            ],
        ),
    )


def create_api_token_with_expiration(account_id: int) -> ApiTokenWithToken:
    # Pass an ISO 8601 date-time for an explicit expiry, or expires_at=None
    # for a token that never expires.
    return api_tokens_api.create(
        account_id=account_id,
        token_params=mt.CreateApiTokenParams(
            name="My API Token With Expiration",
            expires_at=one_year_from_now(),
            resources=[
                mt.ApiTokenResource(
                    resource_type="account",
                    resource_id=account_id,
                    access_level=100,
                )
            ],
        ),
    )


def reset_api_token(account_id: int, api_token_id: int) -> ApiTokenWithToken:
    # The reset response includes the new full token value once — store it securely.
    # Omit token_params for the server default expiration of the new token.
    return api_tokens_api.reset(account_id=account_id, api_token_id=api_token_id)


def reset_api_token_with_expiration(
    account_id: int, api_token_id: int
) -> ApiTokenWithToken:
    # Pass an ISO 8601 date-time for an explicit expiry of the new token,
    # or expires_at=None for a token that never expires.
    return api_tokens_api.reset(
        account_id=account_id,
        api_token_id=api_token_id,
        token_params=mt.ResetApiTokenParams(expires_at=one_year_from_now()),
    )


def delete_api_token(account_id: int, api_token_id: int) -> DeletedObject:
    return api_tokens_api.delete(account_id=account_id, api_token_id=api_token_id)


if __name__ == "__main__":
    tokens = list_api_tokens(ACCOUNT_ID)
    print(tokens)

    created = create_api_token(ACCOUNT_ID)
    print(created)

    created_with_expiration = create_api_token_with_expiration(ACCOUNT_ID)
    print(created_with_expiration)

    fetched = get_api_token(ACCOUNT_ID, created.id)
    print(fetched)

    reset = reset_api_token(ACCOUNT_ID, created.id)
    print(reset)

    reset_with_expiration = reset_api_token_with_expiration(ACCOUNT_ID, reset.id)
    print(reset_with_expiration)

    deleted = delete_api_token(ACCOUNT_ID, reset_with_expiration.id)
    print(deleted)

    deleted_with_expiration = delete_api_token(ACCOUNT_ID, created_with_expiration.id)
    print(deleted_with_expiration)
