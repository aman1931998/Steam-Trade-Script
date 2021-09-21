import urllib.request

def parse_make_offer_with_url_output(trade_offer_data):
    if type(trade_offer_data) != dict:
        return False
    if 'tradeofferid' in trade_offer_data.keys():
        if trade_offer_data['tradeofferid'].isdigit():
            return True
        else:
            return False
    else:
        return False

def load_url(url):
    weburl = urllib.request.urlopen(url)
    code = weburl.getcode()
    return code

