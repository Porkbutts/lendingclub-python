"""
LendingClub Python Client Library
AUTHOR
Adrian Teng-Amnuay
Github:  porkbutts
LICENSE (The MIT License)
Copyright (c) 2017 Adrian Teng-Amnuay "pumpadrian@gmail.com"
Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:
The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

__author__ = 'porkbutts'

import json
import re
import requests
import warnings
from collections import namedtuple
from decimal import *

from .config import LENDINGCLUB_ENDPOINT
from .errors import LendingClubError

url_path_component_regex = re.compile('^[0-9a-z_\-]+$', re.I)

def lendingclub_url(*args):
    args = list(map(str, args))

    for c in args:
        if not url_path_component_regex.match(c):
            raise ValueError(f"malformed url path component {c}")

    return '/'.join([LENDINGCLUB_ENDPOINT] + args)

def namedtuple_from_json(name, dict):
    return namedtuple(name, dict.keys())(**dict)

class LendingClub(object):
    """
    Primary object for interacting with LendingClub API
    """
    def __init__(self, api_key, investor_id=None):
        """
        :param api_key: LendingClub API key
        :param investor_id: Account number displayed when user is logged in
        """
        self.api_key = api_key
        self.investor_id = investor_id

        # Initialize the session object
        self.session = requests.session()
        self.session.headers.update({'content-type':'application/json', 'Authorization':self.api_key})

        # Initialize Loan and Account resources
        self.loan = self.Loan(self.session)
        if investor_id is None:
            warnings.warn("investor_id is required to use the account resource."
                " This can be obtained from the Account Summary section on the"
                " LendingClub website when a user is logged in.")
        else:
            self.account = self.Account(self.session, self.investor_id)

    class Account(object):
        """
        Account Resource provides information related to the investor's account.
        """
        def __init__(self, session, investor_id):
            """
            :param session: Requests session object
            :param investor_id: Account number displayed when user is logged in
            """
            self.session = session
            self.investor_id = investor_id

        def summary(self):
            """
            This subresource provides a summary of the investor's account.
            https://www.lendingclub.com/developers/summary

            :return: Summary
            :raise: HTTPError if there was an error
            """
            url = lendingclub_url('accounts', self.investor_id, 'summary')
            response = self.session.get(url=url)
            response.raise_for_status()
            return namedtuple_from_json('LendingClubSummary', response.json())

        def available_cash(self):
            """
            This subresource provides the most up to date value of the cash available in the investor's account.
            https://www.lendingclub.com/developers/available-cash

            :return: Available cash
            :raise: HTTPError if there was an error
            """
            url = lendingclub_url('accounts', self.investor_id, 'availablecash')
            response = self.session.get(url=url)
            response.raise_for_status()
            return Decimal(response.json().get("availableCash"))

        def add_funds(self, amount, transfer_frequency, start_date=None, end_date=None):
            """
            This subresource enables user to add funds to the investor's account.
            https://www.lendingclub.com/developers/add-funds

            :param amount: Add Fund amount
            :param transfer_frequency: Frequency of Fund Transfer.
                Valid values are:
                LOAD_NOW, LOAD_ONCE, LOAD_WEEKLY, LOAD_BIWEEKLY, LOAD_ON_DAY_1_AND_16, LOAD_MONTHLY
            :param start_date: Recurring transfer start date or transfer date in case of one time transfers
            :param end_date: Recurring transfer end date or null is returned in case of one time transfers

            :return: Transfer info including estimated transfer date
            :raise: HTTPError if there was an error
            """
            url = lendingclub_url('accounts', self.investor_id, 'funds', 'add')
            request_data = {
                "transferFrequency": transfer_frequency,
                "amount": amount,
                "startDate": start_date,
                "endDate": end_date
            }
            response = self.session.post(url=url, data=json.dumps(request_data))
            response.raise_for_status()
            return namedtuple_from_json('LendingClubTransferInfo', response.json())

        def withdraw_funds(self, amount):
            """
            This subresource enables user to withdraw funds from the investor's account.
            https://www.lendingclub.com/developers/add-funds

            :param amount: Withdraw Fund amount

            :return: Transfer info including estimated transfer date
            :raise: HTTPError if there was an error
            """
            url = lendingclub_url('accounts', self.investor_id, 'funds', 'withdraw')
            request_data = {
                "amount": amount
            }
            response = self.session.post(url=url, data=json.dumps(request_data))
            response.raise_for_status()
            return namedtuple_from_json('LendingClubTransferInfo', response.json())

        def pending_transfers(self):
            """
            This subresource enables user to find pending fund transfers for the investor's account.
            https://www.lendingclub.com/developers/pending-transfers

            :return: List of pending transfers
            :raise: HTTPError if there was an error
            """
            url = lendingclub_url('accounts', self.investor_id, 'funds', 'pending')
            response = self.session.get(url=url)
            response.raise_for_status()
            response_parsed = response.json()
            return ([]  if 'transfers' not in response_parsed
                        else [namedtuple_from_json('LendingClubPendingTransfer', d) for d
                            in response_parsed.get('transfers')])

        def cancel_transfers(self, transfer_ids):
            """
            This subresource enables user to cancel the funds transfer initiated.
            https://www.lendingclub.com/developers/cancel-transfers

            :param transfer_ids: list of transferIds to cancel

            :return: List of cancellation results
            :raise: HTTPError if there was an error
            """
            url = lendingclub_url('accounts', self.investor_id, 'funds', 'cancel')
            request_data = {
                "transferId": transfer_ids
            }
            response = self.session.post(url=url, data=json.dumps(request_data))
            response.raise_for_status()
            return [namedtuple_from_json('LendingClubTransferCancellationResult', d) for d
                    in response.json().get('cancellationResults')]

        def notes_owned(self):
            """
            This subresource provides a list of notes that are owned by the investor.
            https://www.lendingclub.com/developers/notes-owned

            :return: List of notes owned by the investor
            :raise: HTTPError if there was an error
            """
            url = lendingclub_url('accounts', self.investor_id, 'notes')
            response = self.session.get(url=url)
            response.raise_for_status()
            return [namedtuple_from_json('LendingClubNote', d) for d
                    in response.json().get('myNotes')]

        def detailed_notes_owned(self, x_lc_detailed_notes_version=None):
            """
            This subresource provides a detailed list of notes that are owned by the investor.
            In addition to the data provided by Owned Notes resource,
            this one adds financial information regarding the notes.
            https://www.lendingclub.com/developers/detailed-notes-owned

            :param x_lc_detailed_notes_version: A non-required header parameter that returns additional response data.

            :return: List of detailed notes owned by the investor
            :raise: HTTPError if there was an error
            """
            url = lendingclub_url('accounts', self.investor_id, 'detailednotes')
            response = self.session.get(url=url, headers={'X-LC-DETAILED-NOTES-VERSION':x_lc_detailed_notes_version})
            response.raise_for_status()
            return [namedtuple_from_json('LendingClubDetailedNote', d) for d
                    in response.json().get('myNotes')]

        def portfolios_owned(self):
            """
            This subresource provides a list of all portfolios that are owned by the investor.
            https://www.lendingclub.com/developers/portfolios-owned

            :return: List of portfolios owned by the investor
            :raise: HTTPError if there was an error
            """
            url = lendingclub_url('accounts', self.investor_id, 'portfolios')
            response = self.session.get(url=url)
            response.raise_for_status()
            return [namedtuple_from_json('LendingClubPortfolio', d) for d
                    in response.json().get('myPortfolios')]

        def create_portfolio(self, portfolio_name, portfolio_description=None):
            """
            This subresource allows investors to create a new portfolio.
            https://www.lendingclub.com/developers/create-portfolio

            :param portfolio_name: Name of the portfolio to create
            :param portfolio_description: Description of the portfolio to create

            :return: the created portfolio
            :raise: LendingClubError if failed to create portfolio
            :raise: HTTPError if there was an error
            """
            url = lendingclub_url('accounts', self.investor_id, 'portfolios')
            request_data = {
                "actorId": self.investor_id,
                "portfolioName": portfolio_name,
                "portfolioDescription": portfolio_description
            }
            response = self.session.post(url=url, data=json.dumps(request_data))
            response_parsed = response.json()
            if response.status_code == requests.codes.bad_request:
                raise LendingClubError("Failed to create portfolio.",
                                        [e.get('message') for e in response_parsed.get('errors')])
            response.raise_for_status()
            return namedtuple_from_json('LendingClubPortfolio', response_parsed)

        def submit_order(self, orders):
            """
            This subresource allows investors to submit a new order for one or more loans.
            https://www.lendingclub.com/developers/submit-order

            :param orders: List of LendingClubOrder objects

            :return: List of order confirmations
            :raise: HTTPError if there was an error
            """
            url = lendingclub_url('accounts', self.investor_id, 'orders')
            request_data = {
                "aid": self.investor_id,
                "orders": [o._asdict() for o in orders]
            }
            response = self.session.post(url=url, data=json.dumps(request_data))
            response.raise_for_status()
            return [namedtuple_from_json('LendingClubOrderConfirmation', d) for d
                    in response.json().get('orderConfirmations')]

        def filters(self):
            """
            This subresource allows investors to retrieve a list of the filters that they have created.
            https://www.lendingclub.com/developers/filters

            :return: List of created filters
            :raise: HTTPError if there was an error
            """
            url = lendingclub_url('accounts', self.investor_id, 'filters')
            response = self.session.get(url=url)
            response.raise_for_status()
            return [namedtuple_from_json('LendingClubFilter', d) for d in response.json()]

    class Loan(object):
        """
        Loan Resource provides the details of the loans from the LendingClub platform
        """
        def __init__(self, session):
            """
            :param session: Requests session object
            """
            self.session = session

        def listed_loans(self, filter_id=None, show_all=None, x_lc_listing_version=None):
            """
            This subresource provides the details of the loans currently listed on
            the Lending Club platform. The list contains the same loans that an
            investor would see on the browse loans page on the Lending Club website.
            The same restrictions that Lending Club applies on the browse loans page
            also apply to the browse loans API. The API currently returns either the
            entire list of loans listed on the platform or only the loans listed in
            the recent listing period. Loans are listed on the Lending Club platform
            at 6AM, 10AM, 2PM, and 6PM every day.
            https://www.lendingclub.com/developers/listed-loans

            :param filter_id: A non-required integer parameter that will filter the
                contents of the result based on the criteria of the filter. The
                investor's filter identifiers can be retrieved from the filters subresource.
            :param show_all: A non-required Boolean parameter that defines the contents of the result.
            :param x_lc_listing_version: A non-required header parameter that returns additional response data.

            :return: List of loans
            :raise: HTTPError if there was an error
            """
            url = lendingclub_url('loans', 'listing')
            params = {'filterId': filter_id, 'showAll': show_all}
            response = self.session.get(url=url, params=params, headers={'X-LC-LISTING-VERSION':x_lc_listing_version})
            response.raise_for_status()
            response_parsed = response.json()
            return namedtuple('LendingClubListedLoans', 'asOfDate loans')(response_parsed.get('asOfDate'),
                [namedtuple_from_json('LendingClubLoan', d) for d in response_parsed.get('loans')])
