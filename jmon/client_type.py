from enum import Enum


class ClientType(Enum):
    """Types of clients"""

    BROWSER_FIREFOX = "BROWSER_FIREFOX"
    BROWSER_CHROME = "BROWSER_CHROME"
    REQUESTS = "REQUESTS"

    @classmethod
    def get_all(cls):
        """Return all names of client types, in order"""
        return [cls.REQUESTS, cls.BROWSER_FIREFOX, cls.BROWSER_CHROME]
