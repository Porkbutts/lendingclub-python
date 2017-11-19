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

## Getting Started

In order to begin working with the LendingClub API, you will need your API key and Account ID.

* [Instructions on retrieving the API key](https://www.lendingclub.com/developers/authentication)
*  The Account ID can be obtained from the Account Summary section on the LendingClub website when a user is logged in.

## Examples

### Account Summary
```python
>>> from lendingclub import LendingClub
>>> lc = LendingClub('your_api_key', 'your_account_id')
>>> lc.account.summary()
LendingClubSummary(investorId=123456789, availableCash=0, accountTotal=2500, accruedInterest=0, infundingBalance=2500, receivedInterest=0, receivedPrincipal=0, receivedLateFees=0, outstandingPrincipal=0, totalNotes=100, totalPortfolios=2, netAnnualizedReturn={'primaryNAR': None, 'primaryAdjustedNAR': None, 'primaryUserAdjustedNAR': None, 'tradedNAR': None, 'tradedAdjustedNAR': None, 'tradedUserAdjustedNAR': None, 'combinedNAR': None, 'combinedAdjustedNAR': None, 'combinedUserAdjustedNAR': None}, adjustments={'adjustmentForPastDueNotes': 0, 'userAdjustmentForPastDueNotes': None})
```

### Available Cash
```python
>>> from lendingclub import LendingClub
>>> lc = LendingClub('your_api_key', 'your_account_id')
>>> lc.account.available_cash()
Decimal('0')
```

### View Owned Notes
```python
>>> from lendingclub import LendingClub
>>> lc = LendingClub('your_api_key', 'your_account_id')
>>> notes = lc.account.notes_owned()

# View just the first two notes for brevity
>>> notes[:2]
[LendingClubNote(loanId=120119426, noteId=172055989, orderId=172454222, interestRate=10.42, loanLength=36, loanStatus='In Review', grade='B', subGrade='B3', loanAmount=20000, noteAmount=25, paymentsReceived=0, issueDate=None, orderDate='2017-11-17T10:25:42.000-08:00', loanStatusDate='2017-11-17T22:45:01.000-08:00'), LendingClubNote(loanId=121298234, noteId=172055990, orderId=172454222, interestRate=18.06, loanLength=36, loanStatus='In Review', grade='D', subGrade='D2', loanAmount=15000, noteAmount=25, paymentsReceived=0, issueDate=None, orderDate='2017-11-17T10:25:42.000-08:00', loanStatusDate='2017-11-17T10:26:39.000-08:00')]
```

## Advanced Examples

### Find the top ten Grade-A loans ranked by interest rate and submit an order for ten $100 notes

```python
>>> from lendingclub import LendingClub
>>> lc = LendingClub('your_api_key', 'your_account_id')
>>> loans = lc.loan.listed_loans().loans
>>> grade_a_loans = [x for x in loans if x.grade=='A']
>>> sorted_grade_a_loans = sorted(grade_a_loans, key=lambda x: x.intRate, reverse=True)
>>> top_ten_grade_a_loans = sorted_grade_a_loans[:10]
>>> from lendingclub.models import LendingClubOrder
>>> lc.account.submit_order([LendingClubOrder(x.id, 100) for x in top_ten_grade_a_loans])
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
