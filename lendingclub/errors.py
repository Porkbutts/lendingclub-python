__author__ = 'porkbutts'

class LendingClubError(Exception):
    def __init__(self, message, errors=None):
        super(LendingClubError, self).__init__(self, ' '.join([message] + (errors or [])))
