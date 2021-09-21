from PIL import ImageGrab
import numpy as np
import time
from config import w, h, nearby_snippet_check_threshold
from mouse_functions import click_only
import math
import os

def load_image_snippets():
    l = os.listdir('trade_snippets')
    d = {}
    for i in l:
        image = np.load(os.path.join('trade_snippets', i))
        d[i.split('.')[0]] = image
    print("Found %d Snippets"%(len(d)))
    return d

#%% Haystack functions
def haystack_pixel_generator(x1, y1, x2, y2, reduced = False):
    return max(0, x1 - nearby_snippet_check_threshold // 2), max(0, y1 - nearby_snippet_check_threshold // 2), min(w, x2 + nearby_snippet_check_threshold // 2), min(h, y2 + nearby_snippet_check_threshold // 2)

def find_matches(haystack, needle):
    arr_h = np.array(np.asarray(haystack)[:, :, :3], 'uint8')
    arr_n = np.array(np.asarray(needle)[:, :, :3], 'uint8')

    y_h, x_h = arr_h.shape[:2]
    y_n, x_n = arr_n.shape[:2]

    xstop = x_h - x_n + 1
    ystop = y_h - y_n + 1

    for xmin in range(0, xstop):
        for ymin in range(0, ystop):
            xmax = xmin + x_n
            ymax = ymin + y_n

            arr_s = arr_h[ymin:ymax, xmin:xmax]     # Extract subimage
            arr_t = (arr_s == arr_n)                # Create test matrix
            if arr_t.all():                         # Only consider exact matches
                matches = (xmin,ymin)
                return matches

def find_matches_green(haystack, x_n, y_n, accepted_green_color):
    arr_h = np.array(np.asarray(haystack)[:, :, :3], 'uint8')
    y_h, x_h = arr_h.shape[:2]
    xstop, ystop = x_h - x_n + 1, y_h - y_n + 1

    for xmin in range(0, xstop):
        for ymin in range(0, ystop):
            avg_green = int(math.floor((np.average(arr_h[ymin:ymin + y_n, xmin:xmin + x_n][:, :, 1])) * 1000))
            if avg_green in range(int((accepted_green_color - 1.2) * 1000), int((accepted_green_color + 1.2) * 1000)):
                return xmin, ymin
    return None

#%% Steam Client Confirmation after login
def confirm_steam_client_internal(steam_client):
    from positions import STEAM_CLIENT_X_1, STEAM_CLIENT_Y_1, \
        STEAM_CLIENT_X_2, STEAM_CLIENT_Y_2
    STEAM_CLIENT_X_1, STEAM_CLIENT_Y_1, STEAM_CLIENT_X_2, STEAM_CLIENT_Y_2 = haystack_pixel_generator(STEAM_CLIENT_X_1, 
                                                                                                      STEAM_CLIENT_Y_1, 
                                                                                                      STEAM_CLIENT_X_2, 
                                                                                                      STEAM_CLIENT_Y_2)
    image = ImageGrab.grab([STEAM_CLIENT_X_1, STEAM_CLIENT_Y_1, STEAM_CLIENT_X_2, STEAM_CLIENT_Y_2]).convert("RGB")
    output = find_matches(image, steam_client)
    if output == None:
        return False
    else:
        return output

def confirm_steam_client(snippets_dict):
    steam_client = snippets_dict['steam_client']
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output = confirm_steam_client_internal(steam_client)
        if output != False:
            return output
    return False

#%% Steam Trade Offers page
def confirm_steam_trade_offers_internal(confirm_steam_trade_offers):
    from positions import STEAM_CLIENT_TRADE_OFFERS_PAGE_X_1, STEAM_CLIENT_TRADE_OFFERS_PAGE_Y_1, \
        STEAM_CLIENT_TRADE_OFFERS_PAGE_X_2, STEAM_CLIENT_TRADE_OFFERS_PAGE_Y_2 
    STEAM_CLIENT_TRADE_OFFERS_PAGE_X_1, STEAM_CLIENT_TRADE_OFFERS_PAGE_Y_1, \
        STEAM_CLIENT_TRADE_OFFERS_PAGE_X_2, STEAM_CLIENT_TRADE_OFFERS_PAGE_Y_2  = haystack_pixel_generator(STEAM_CLIENT_TRADE_OFFERS_PAGE_X_1, 
                                                                                                           STEAM_CLIENT_TRADE_OFFERS_PAGE_Y_1, 
                                                                                                           STEAM_CLIENT_TRADE_OFFERS_PAGE_X_2, 
                                                                                                           STEAM_CLIENT_TRADE_OFFERS_PAGE_Y_2)
    image = ImageGrab.grab([STEAM_CLIENT_TRADE_OFFERS_PAGE_X_1, 
                            STEAM_CLIENT_TRADE_OFFERS_PAGE_Y_1, 
                            STEAM_CLIENT_TRADE_OFFERS_PAGE_X_2, 
                            STEAM_CLIENT_TRADE_OFFERS_PAGE_Y_2]).convert("RGB")
    output = find_matches(image, confirm_steam_trade_offers)
    if output == None:
        return False
    else:
        return output

def confirm_steam_trade_offers(snippets_dict):
    confirm_steam_trade_offers = snippets_dict['steam_trade_offers_page']
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output = confirm_steam_trade_offers_internal(confirm_steam_trade_offers)
        if output != False:
            return output
    return False

#%% Steam (current) trade offer
def confirm_current_steam_trade_offer_internal(current_trade_offer_page):
    from positions import STEAM_CURRENT_TRADE_OFFER_PAGE_1_X_1, STEAM_CURRENT_TRADE_OFFER_PAGE_1_Y_1, \
        STEAM_CURRENT_TRADE_OFFER_PAGE_1_X_2, STEAM_CURRENT_TRADE_OFFER_PAGE_1_Y_2
    STEAM_CURRENT_TRADE_OFFER_PAGE_1_X_1, STEAM_CURRENT_TRADE_OFFER_PAGE_1_Y_1, \
        STEAM_CURRENT_TRADE_OFFER_PAGE_1_X_2, STEAM_CURRENT_TRADE_OFFER_PAGE_1_Y_2 = haystack_pixel_generator(STEAM_CURRENT_TRADE_OFFER_PAGE_1_X_1, 
                                                                                                              STEAM_CURRENT_TRADE_OFFER_PAGE_1_Y_1, 
                                                                                                              STEAM_CURRENT_TRADE_OFFER_PAGE_1_X_2, 
                                                                                                              STEAM_CURRENT_TRADE_OFFER_PAGE_1_Y_2, reduced = True)
    image = ImageGrab.grab([STEAM_CURRENT_TRADE_OFFER_PAGE_1_X_1, 
                            STEAM_CURRENT_TRADE_OFFER_PAGE_1_Y_1, 
                            STEAM_CURRENT_TRADE_OFFER_PAGE_1_X_2, 
                            STEAM_CURRENT_TRADE_OFFER_PAGE_1_Y_2]).convert("RGB")
    output = find_matches(image, current_trade_offer_page)
    if output == None:
        return False
    else:
        return output

def confirm_current_steam_trade_offer(snippets_dict):
    current_trade_offer_page = snippets_dict['current_trade_offer_page']
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output = confirm_current_steam_trade_offer_internal(current_trade_offer_page)
        if output != False:
            return output
    return False

#%% Steam confirm trade contents button
def confirm_confirm_trade_contents_button_internal(trade_offer_page_confirm_button):
    from positions import STEAM_CONFIRM_TRADE_CONTENTS_BUTTON_X_1, STEAM_CONFIRM_TRADE_CONTENTS_BUTTON_Y_1, \
        STEAM_CONFIRM_TRADE_CONTENTS_BUTTON_X_2, STEAM_CONFIRM_TRADE_CONTENTS_BUTTON_Y_2
    STEAM_CONFIRM_TRADE_CONTENTS_BUTTON_X_1, STEAM_CONFIRM_TRADE_CONTENTS_BUTTON_Y_1, \
        STEAM_CONFIRM_TRADE_CONTENTS_BUTTON_X_2, STEAM_CONFIRM_TRADE_CONTENTS_BUTTON_Y_2 = \
            haystack_pixel_generator(STEAM_CONFIRM_TRADE_CONTENTS_BUTTON_X_1, 
                                     STEAM_CONFIRM_TRADE_CONTENTS_BUTTON_Y_1, 
                                     STEAM_CONFIRM_TRADE_CONTENTS_BUTTON_X_2, 
                                     STEAM_CONFIRM_TRADE_CONTENTS_BUTTON_Y_2)
    image = ImageGrab.grab([STEAM_CONFIRM_TRADE_CONTENTS_BUTTON_X_1, 
                            STEAM_CONFIRM_TRADE_CONTENTS_BUTTON_Y_1, 
                            STEAM_CONFIRM_TRADE_CONTENTS_BUTTON_X_2, 
                            STEAM_CONFIRM_TRADE_CONTENTS_BUTTON_Y_2]).convert("RGB")
    output = find_matches(image, trade_offer_page_confirm_button)
    if output == None: return False
    else: return output

def confirm_confirm_trade_contents_button(snippets_dict):
    trade_offer_page_confirm_button = snippets_dict['trade_offer_page_confirm_button']
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(112, 357, 0.1, 1)
        output = confirm_confirm_trade_contents_button_internal(trade_offer_page_confirm_button)
        if output != False:
            return output
    return False

def get_confirm_trade_contents_button_pixels(x, y):
    from positions import STEAM_CONFIRM_TRADE_CONTENTS_BUTTON_X_1, STEAM_CONFIRM_TRADE_CONTENTS_BUTTON_Y_1
    x, y = STEAM_CONFIRM_TRADE_CONTENTS_BUTTON_X_1 + x - 39, STEAM_CONFIRM_TRADE_CONTENTS_BUTTON_Y_1 + y - 114
    return x, y

#%% Suspicious trade window
def confirm_suspicious_trade_dialog_box_internal():
    from positions import STEAM_TRADE_SUSPICIOUS_DIALOG_BOX_X_1, STEAM_TRADE_SUSPICIOUS_DIALOG_BOX_Y_1, \
        STEAM_TRADE_SUSPICIOUS_DIALOG_BOX_X_2, STEAM_TRADE_SUSPICIOUS_DIALOG_BOX_Y_2
    x1, y1, x2, y2 = haystack_pixel_generator(STEAM_TRADE_SUSPICIOUS_DIALOG_BOX_X_1, 
                                              STEAM_TRADE_SUSPICIOUS_DIALOG_BOX_Y_1, 
                                              STEAM_TRADE_SUSPICIOUS_DIALOG_BOX_X_2, 
                                              STEAM_TRADE_SUSPICIOUS_DIALOG_BOX_Y_2, reduced = True)
    image = ImageGrab.grab([x1, y1, x2, y2]).convert("RGB")
    x, y = STEAM_TRADE_SUSPICIOUS_DIALOG_BOX_X_2 - STEAM_TRADE_SUSPICIOUS_DIALOG_BOX_X_1, STEAM_TRADE_SUSPICIOUS_DIALOG_BOX_Y_2 - STEAM_TRADE_SUSPICIOUS_DIALOG_BOX_Y_1
    output = find_matches_green(image, x, y, 162)
    if output == None:
        return False
    else:
        return output

def confirm_suspicious_trade_dialog_box():
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output = confirm_suspicious_trade_dialog_box_internal()
        if output != False:
            return output
    return False

def get_yes_this_is_a_gift_button(x, y):
    from positions import STEAM_TRADE_SUSPICIOUS_DIALOG_BOX_X_1, STEAM_TRADE_SUSPICIOUS_DIALOG_BOX_Y_1
    x, y = STEAM_TRADE_SUSPICIOUS_DIALOG_BOX_X_1 + x, STEAM_TRADE_SUSPICIOUS_DIALOG_BOX_Y_1 + y - 36
    return x, y

#%% accept trade
def confirm_accept_trade_internal():
    from positions import STEAM_CURRENT_TRADE_OFFER_PAGE_2_X_1, STEAM_CURRENT_TRADE_OFFER_PAGE_2_Y_1, \
        STEAM_CURRENT_TRADE_OFFER_PAGE_2_X_2, STEAM_CURRENT_TRADE_OFFER_PAGE_2_Y_2 
    x1, y1, x2, y2 = haystack_pixel_generator(STEAM_CURRENT_TRADE_OFFER_PAGE_2_X_1, 
                                              STEAM_CURRENT_TRADE_OFFER_PAGE_2_Y_1, 
                                              STEAM_CURRENT_TRADE_OFFER_PAGE_2_X_2, 
                                              STEAM_CURRENT_TRADE_OFFER_PAGE_2_Y_2 , reduced = True)
    image = ImageGrab.grab([x1, y1, x2, y2]).convert("RGB")
    x, y = STEAM_CURRENT_TRADE_OFFER_PAGE_2_X_2 - STEAM_CURRENT_TRADE_OFFER_PAGE_2_X_1, STEAM_CURRENT_TRADE_OFFER_PAGE_2_Y_2 - STEAM_CURRENT_TRADE_OFFER_PAGE_2_Y_1
    output = find_matches_green(image, x, y, 175)
    if output == None:
        return False
    else:
        return output

def confirm_accept_trade():
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output = confirm_accept_trade_internal()
        if output != False:
            return output
    return False

def get_accept_trade_button(x, y):
    from positions import STEAM_CURRENT_TRADE_OFFER_PAGE_2_X_1, STEAM_CURRENT_TRADE_OFFER_PAGE_2_Y_1
    x, y = STEAM_CURRENT_TRADE_OFFER_PAGE_2_X_1 + x + 68, STEAM_CURRENT_TRADE_OFFER_PAGE_2_Y_1 + y - 29 - 12
    return x, y

#%% email confirmation ok
def confirm_email_authentication_internal(steam_additional_confirmation_needed):
    from positions import STEAM_EMAIL_CONFIRMATION_ACCEPT_X_1, STEAM_EMAIL_CONFIRMATION_ACCEPT_Y_1, \
        STEAM_EMAIL_CONFIRMATION_ACCEPT_X_2, STEAM_EMAIL_CONFIRMATION_ACCEPT_Y_2
    STEAM_EMAIL_CONFIRMATION_ACCEPT_X_1, STEAM_EMAIL_CONFIRMATION_ACCEPT_Y_1, \
        STEAM_EMAIL_CONFIRMATION_ACCEPT_X_2, STEAM_EMAIL_CONFIRMATION_ACCEPT_Y_2 = \
            haystack_pixel_generator(STEAM_EMAIL_CONFIRMATION_ACCEPT_X_1, 
                                     STEAM_EMAIL_CONFIRMATION_ACCEPT_Y_1, 
                                     STEAM_EMAIL_CONFIRMATION_ACCEPT_X_2, 
                                     STEAM_EMAIL_CONFIRMATION_ACCEPT_Y_2, reduced = True)
    image = ImageGrab.grab([STEAM_EMAIL_CONFIRMATION_ACCEPT_X_1, 
                            STEAM_EMAIL_CONFIRMATION_ACCEPT_Y_1, 
                            STEAM_EMAIL_CONFIRMATION_ACCEPT_X_2, 
                            STEAM_EMAIL_CONFIRMATION_ACCEPT_Y_2]).convert("RGB")
    output = find_matches(image, steam_additional_confirmation_needed)
    if output == None:
        return False
    else:
        return output

def confirm_email_authentication(snippets_dict):
    steam_additional_confirmation_needed = snippets_dict['steam_additional_confirmation_needed']
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output = confirm_email_authentication_internal(steam_additional_confirmation_needed)
        if output != False:
            return output
    return False

def get_email_authorization_needed_button(x, y):
    from positions import STEAM_EMAIL_CONFIRMATION_ACCEPT_X_1, STEAM_EMAIL_CONFIRMATION_ACCEPT_Y_1
    x, y = STEAM_EMAIL_CONFIRMATION_ACCEPT_X_1 + x - 35, STEAM_EMAIL_CONFIRMATION_ACCEPT_Y_1 + y - 38
    return x, y
