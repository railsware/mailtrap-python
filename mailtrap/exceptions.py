class MailtrapError(Exception):
    pass


class ClientConfigurationError(MailtrapError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class APIError(MailtrapError):
    def __init__(self, status: int, errors: list[str]) -> None:
        self.status = status
        self.errors = errors

        super().__init__("; ".join(errors))


class AuthorizationError(APIError):
    def __init__(self, errors: list[str]) -> None:
        super().__init__(status=401, errors=errors)
