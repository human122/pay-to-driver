# from django.shortcuts import render

from xml.etree import ElementTree
import requests

from .config import QIWI_API_LOGIN, QIWI_API_PASSWORD


def get_qiwi_park(qiwi_park_object):
    data = '<request><request-type>ping</request-type><terminal-id>' + \
        QIWI_API_LOGIN + '</terminal-id><extra name="password">' + \
        QIWI_API_PASSWORD + '</extra></request>'
    r = requests.post('https://api.qiwi.com/xml/topup.jsp', data=data)
    if r.status_code == 200:
        root = ElementTree.fromstring(r.text)
        balance = [
            float(sub.text) for c in root for sub in c if c.tag == 'balances'
            ][0]
        if qiwi_park_object.amount != balance:
            qiwi_park_object.amount = balance
            qiwi_park_object.save()
        return balance
