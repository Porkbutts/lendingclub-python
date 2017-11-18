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
        def __init__(self, session, investor_id):
            self.session = session
            self.investor_id = investor_id

        def summary(self):
            url = lendingclub_url('accounts', self.investor_id, 'summary')
            response = self.session.get(url=url)
            response.raise_for_status()
            return namedtuple_from_json('LendingClubSummary', response.json())

        def available_cash(self):
            url = lendingclub_url('accounts', self.investor_id, 'availablecash')
            response = self.session.get(url=url)
            response.raise_for_status()
            return Decimal(response.json().get("availableCash"))

        def add_funds(self, amount, transfer_frequency, start_date=None, end_date=None, estimated_funds_transfer_date=None):
            pass

        def withdraw_funds(self, amount):
            url = lendingclub_url('accounts', self.investor_id, 'funds', 'withdraw')
            request_data = {
                "amount": amount
            }
            response = self.session.post(url=url, data=json.dumps(request_data))
            response.raise_for_status()
            return namedtuple_from_json('LendingClubWithdrawFundsResponse', response.json())

        def pending_transfers(self):
            url = lendingclub_url('accounts', self.investor_id, 'funds', 'pending')
            response = self.session.get(url=url)
            response.raise_for_status()
            response_parsed = response.json()
            return ([]  if 'transfers' not in response_parsed
                        else [namedtuple_from_json('LendingClubPendingTransfer', d) for d
                            in response_parsed.get('transfers')])

        def cancel_transfers(self, transfer_ids):
            url = lendingclub_url('accounts', self.investor_id, 'funds', 'cancel')
            request_data = {
                "transferId": transfer_ids
            }
            response = self.session.post(url=url, data=json.dumps(request_data))
            response.raise_for_status()
            return [namedtuple_from_json('LendingClubCancellationResult', d) for d
                    in response.json().get('cancellationResults')]

        def notes_owned(self):
            url = lendingclub_url('accounts', self.investor_id, 'notes')
            response = self.session.get(url=url)
            response.raise_for_status()
            return [namedtuple_from_json('LendingClubNote', d) for d
                    in response.json().get('myNotes')]

        def detailed_notes_owned(self, x_lc_detailed_notes_version=None):
            url = lendingclub_url('accounts', self.investor_id, 'detailednotes')
            response = self.session.get(url=url, headers={'X-LC-DETAILED-NOTES-VERSION':x_lc_detailed_notes_version})
            response.raise_for_status()
            return [namedtuple_from_json('LendingClubDetailedNote', d) for d
                    in response.json().get('myNotes')]

        def portfolios_owned(self):
            url = lendingclub_url('accounts', self.investor_id, 'portfolios')
            response = self.session.get(url=url)
            response.raise_for_status()
            return [namedtuple_from_json('LendingClubPortfolio', d) for d
                    in response.json().get('myPortfolios')]

        def create_portfolio(self, portfolio_name, portfolio_description=None):
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

        def submit_order(self):
            pass

        def filters(self):
            url = lendingclub_url('accounts', self.investor_id, 'filters')
            response = self.session.get(url=url)
            response.raise_for_status()
            return [namedtuple_from_json('LendingClubFilter', d) for d in response.json()]

    class Loan(object):
        def __init__(self, session):
            self.session = session

        def listed_loans(self, filter_id=None, show_all=None, x_lc_listing_version=None):
            url = lendingclub_url('loans', 'listing')
            params = {'filterId': filter_id, 'showAll': show_all}
            response = self.session.get(url=url, params=params, headers={'X-LC-LISTING-VERSION':x_lc_listing_version})
            response.raise_for_status()
            response_parsed = response.json()
            return namedtuple('LendingClubListedLoans', 'asOfDate loans')(response_parsed.get('asOfDate'),
             [namedtuple_from_json('LendingClubLoan', d) for d in response_parsed.get('loans')])
