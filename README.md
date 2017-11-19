Unofficial LendingClub Python Library
==================================

Python Library for the LendingClub API

## Version

0.1.0

## Requirements
- [LendingClub Account](https://www.lendingclub.com/)
- [Requests](http://docs.python-requests.org/en/latest/)

## Installation

Automatic installation using [pip](http://pypi.python.org/pypi):

    pip install lcpy

## Examples

### Account Summary
```python
>>> from lendingclub import LendingClub
>>> lc = LendingClub('your_api_key', 'your_account_id')
>>> summary = lc.account.summary()
>>> summary
LendingClubSummary(investorId=123456789, availableCash=0, accountTotal=2500, accruedInterest=0, infundingBalance=2500, receivedInterest=0, receivedPrincipal=0, receivedLateFees=0, outstandingPrincipal=0, totalNotes=100, totalPortfolios=2, netAnnualizedReturn={'primaryNAR': None, 'primaryAdjustedNAR': None, 'primaryUserAdjustedNAR': None, 'tradedNAR': None, 'tradedAdjustedNAR': None, 'tradedUserAdjustedNAR': None, 'combinedNAR': None, 'combinedAdjustedNAR': None, 'combinedUserAdjustedNAR': None}, adjustments={'adjustmentForPastDueNotes': 0, 'userAdjustmentForPastDueNotes': None})
>>> summary.available_cash
0
```

### Order Loans
```python
>>> from lendingclub import LendingClub
>>> lc = LendingClub('your_api_key', 'your_account_id')
>>> loans = lc.loan.listed_loans().loans
>>> len(loans)
12
>>> from lendingclub.models import LendingClubOrder
>>> orders = [LendingClubOrder(x.id, 25) for x in loans if x.grade=='A']
>>> lc.account.submit_order(orders)
```

## Changelog

0.1.0

* Initial Commit

## Contributing

Contributions are greatly appreciated.  Please make all requests using built in issue tracking at GitHub.

## Credits

- Adrian Teng-Amnuay &lt;pumpadrian@gmail.com&gt;

## License

(The MIT License)

Copyright (c) 2017 Adrian Teng-Amnuay &lt;pumpadrian@gmail.com&gt;

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
