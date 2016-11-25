"""
https://www.bitstamp.net/api/
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.rest import BitstampREST
from bitex.utils import return_json

# Init Logging Facilities
log = logging.getLogger(__name__)


class Bitstamp(BitstampREST):
    def __init__(self, key='', secret='', key_file=''):
        super(Bitstamp, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('POST', endpoint, authenticate=True, **kwargs)

    """
    BitEx Standardized Methods
    """

    @return_json(None)
    def ticker(self, pair):
        return self.public_query('v2/ticker/%s/' % pair)

    @return_json(None)
    def order_book(self, pair):
        return self.public_query('v2/order_book/%s' % pair)

    @return_json(None)
    def trades(self, pair, **kwargs):
        return self.public_query('v2/transactions/%s' % pair, params=kwargs)

    @return_json(None)
    def bid(self, pair, price, size, **kwargs):
        q = {'amount': size, 'price': price}
        q.update(kwargs)
        return self.private_query('v2/buy/%s/' % pair, params=q)

    @return_json(None)
    def ask(self, pair, price, size, **kwargs):
        q = {'amount': size, 'price': price}
        q.update(kwargs)
        return self.private_query('v2/sell/%s/' % pair, params=q)

    @return_json(None)
    def cancel_order(self, order_id, all=False, **kwargs):
        raise NotImplementedError()

    @return_json(None)
    def order(self, order_id, **kwargs):
        q = {'id': order_id}
        q.update(kwargs)
        return self.private_query('order_status/', params=q)

    @return_json(None)
    def balance(self, **kwargs):
        return self.private_query('v2/balance/')

    @return_json(None)
    def withdraw(self, amount, receiver, **kwargs):
        q = {'amount': amount, 'address': receiver}
        q.update(kwargs)
        return self.private_query('bitcoin_withdrawal/', params=q)

    @return_json(None)
    def deposit_address(self, **kwargs):
        return self.private_query('bitcoin_deposit_address/')

    """
    Exchange Specific Methods
    """

    @return_json(None)
    def hourly_ticker(self, pair):
        return self.public_query('v2/ticker_hour/%s' % pair)

    @return_json(None)
    def eurusd_rate(self):
        return self.public_query('eur_usd')

    def pairs(self):
        return ['btcusd', 'btceur', 'eurusd']
