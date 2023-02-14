from typing import List


class MailtrapError(Exception):
    pass


class APIError(MailtrapError):
    def __init__(self, status: int, errors: List[str]) -> None:
        self.status = status
        self.errors = errors

        super().__init__("; ".join(errors))


class AuthorizationError(APIError):
    def __init__(self, errors: List[str]) -> None:
        super().__init__(status=401, errors=errors)
