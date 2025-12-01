class AssemblyAPIError(Exception):
    """Custom exception for Assembly API errors."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


class SpecParseError(Exception):
    """Raised when spec parsing fails."""

    pass
