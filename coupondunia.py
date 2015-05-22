__author__ = 'ajitkumar'

import requests
from bs4 import BeautifulSoup


def search_page(search_string):
    try:
        payload = search_string
        response = requests.get('http://www.coupondunia.in/'+payload)
        soup = BeautifulSoup(response.content)
        offers = soup.find_all('div', {'class': 'offer-title'})
        offers_description = soup.find_all('div', {'class': 'offer-description-full'})
        offer_list = []
        for offer, offer_description in zip(offers, offers_description):
            offer_dict = {}
            offer_title = offer.a.string
            description = offer_description.string
            if not description:
                description = offer_description.contents[0]
            coupon_code = offer.a['data-code']
            offer_dict['offer_title'] = offer_title
            offer_dict['offer_description'] = description.strip()
            offer_dict['coupon_code'] = coupon_code
            offer_list.append(offer_dict)
        return offer_list
    except Exception, excpt:
        return offer_list


#print search_page('paytm')


