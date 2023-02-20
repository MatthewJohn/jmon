from enum import Enum


class ClientType(Enum):
    """Types of clients"""

    BROWSER_FIREFOX = "BROWSER_FIREFOX"
    BROWSER_CHROME = "BROWSER_CHROME"
    REQUESTS = "REQUESTS"
