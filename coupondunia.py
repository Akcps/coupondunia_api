__author__ = 'ajitkumar'

import requests
from bs4 import BeautifulSoup
import unicodedata


def search_page(search_string):
    try:
        payload = search_string
        response = requests.get('http://www.coupondunia.in/'+payload)
        soup = BeautifulSoup(response.content)
        offers = soup.find_all('div', {'class': 'coupon-big coupon single-merchant'})
        offer_list = list()
        for offer in offers:
            new_offer = dict()
            offers_coupon = offer.find_all('div', {'class': 'online_offer offer-title get-title-code'})
            offer_title = offers_coupon[0].span.text
            offer_title = unicodedata.normalize('NFKD', offer_title).encode('ascii', 'ignore')
            new_offer['offer_title'] = offer_title
            url = offers_coupon[0]['data-coupon-url']
            new_offer['coupon_code'] = get_offer_code(url)
            offers_description = offer.find_all('div', {'class': 'meta offer-desc'})
            offer_desc = offers_description[0].text
            offer_desc = offer_desc.strip()
            offer_desc = unicodedata.normalize('NFKD', offer_desc).encode('ascii', 'ignore')
            new_offer['offer_description'] = offer_desc
            offer_list.append(new_offer)
        return offer_list
    except Exception, excpt:
        print excpt
        return offer_list


def get_offer_code(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content)
        val = soup.find_all('div', {'class': 'coupon-code_new coupon-code inline-block'})
        offer_code = val[0].text
        offer_code = offer_code.strip()
        return offer_code
    except Exception, excpt:
        print excpt
        return ''

#print search_page('paytm')


