class ATMException(Exception):
    def __init__(
        self,
        id=None,
        message=None,
        can_retry=True,
        retries=0,
        details=None,
        description=None,
        expected=None,
    ):
        self.message = message
        self.can_retry = can_retry
        if retries >= 1:
            self.can_retry = False
        if id:
            self.id = id
        if details:
            self.details = details
        if description:
            self.description = description
        if expected:
            self.expected = expected
