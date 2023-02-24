
class JmonError(Exception):
    """Base JMON error"""

    pass


class CheckCreateError(JmonError):
    """Failed to create check"""

    pass


class EnvironmentCreateError(JmonError):
    """Failed to create environment"""

    pass
