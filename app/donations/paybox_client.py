import json
import datetime
import requests
from config.settings import PAYBOX_SECRET_KEY, PAYBOX_MERCHANT_ID
import uuid
import base64
import hashlib
from collections import OrderedDict
class Paybox:
    CURRENCY = "KZT"

    def __init__(self):
        self.API_URL = "https://api.paybox.money/init_payment.php"
        # self.POST_PAYMENT = self.API_URL+"payments"

    def get_request_body(self, order, amount, description):
        request_body_to_sort = {
            "pg_order_id": order,
            "pg_merchant_id": PAYBOX_MERCHANT_ID,
            "pg_amount": amount,
            "pg_currency": self.CURRENCY,
            "pg_description": description,
            "pg_testing_mode": 1,
            "pg_salt": "asd"
            }
        request_body_sorted = OrderedDict(sorted(request_body_to_sort.items()))
        request_body = {
            "0": 'init_payment.php'
        }
        request_body.update(request_body_sorted)
        request_body_1 = {
            "1": PAYBOX_SECRET_KEY
        }
        request_body.update(request_body_1)
        pg_sig = hashlib.md5((";".join([ str(x) for x in request_body.values()])).encode()).hexdigest()
        pg_sig_1 = {
            "pg_sig":str(pg_sig)
        }
        request_body_to_sort.update(pg_sig_1)
        # print(request_body_to_sort)
        return request_body_to_sort


    def paybox_request(self, order, amount, description):

        request_body = self.get_request_body(order, amount, description)
        payment_request = requests.post(self.API_URL, request_body)

        return payment_request

    def __str__(self):
        return self.API_URL