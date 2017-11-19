from collections import namedtuple

class LendingClubOrder(namedtuple('LendingClubOrder', 'loanId requestedAmount portfolioId')):
    __slots__ = ()
    def __new__(cls, loanId, requestedAmount, portfolioId=None):
        return super(LendingClubOrder, cls).__new__(cls, loanId, requestedAmount, portfolioId)
