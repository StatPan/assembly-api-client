class AssemblyAPIError(Exception):
    """Base exception for Assembly API errors."""

    pass


class SpecParseError(AssemblyAPIError):
    """Raised when spec parsing fails."""

    pass


class APIRequestError(AssemblyAPIError):
    """Raised when an API request fails."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")
