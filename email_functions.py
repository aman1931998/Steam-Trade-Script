from datetime import datetime, timedelta
import imaplib
import email

def establish_connection_to_mailserver(domain):
    try:
        imap = imaplib.IMAP4_SSL(domain, imaplib.IMAP4_SSL_PORT)
    except:
        raise Exception("Unable to establish connection with the mail server.")
    return imap


def imap_login_into_mail(imap, email_address, email_password):
    assert type(imap) == imaplib.IMAP4_SSL and '@' in email_address
    # Logging in
    output = imap.login(email_address, email_password)
    if output[0] == 'OK':
        return imap
    else:
        raise Exception("Unable to Log in.")

def imap_logout_of_mail(imap):
    output = imap.logout()
    if output[0] == 'BYE':
        return True
    else:
        raise Exception("Unable to Log out.")

def get_trade_acceptance_URL(imap, trade_offer_id, steamID):
    trade_offer_id, steamID = str(trade_offer_id), str(steamID)
    test_string = "https://steamcommunity.com/tradeoffer/%s/confirm?accountid=%s&tradeofferid=%s&confirmation_code="%(trade_offer_id, steamID, trade_offer_id)
    # Selecting inbox
    rv, data = imap.select("INBOX", readonly = True)
    
    # Getting all unseen mails
    rv, data = imap.search(None, '(UNSEEN)')
    if data == [''] or data == [b'']:
        return None, "No new mail found."
    
    # getting ID of latest mail
    ids = data[0].split()
    latest_id = ids[-1]
    
    # Opening latest mail
    result, data = imap.fetch(latest_id, "(RFC822)")
    msg = email.message_from_bytes(data[0][1])  
    assert msg.is_multipart() == True
    # msg_items = msg.items()
    msg_date_time = msg['Date']
    msg_date_time = datetime.strptime(msg_date_time[:msg_date_time.rindex(' ')], "%a, %d %b %Y %H:%M:%S") + timedelta(hours = 12, minutes = 30)   # - timedelta(hours = int(msg_date_time[msg_date_time.rindex(' ') + 1:][2:3]))
    # if datetime.now() - msg_date_time > timedelta(minutes = 5):
    #     return None, "No new mail received yet."
    msg_part = list(msg.walk())[0] ###
    msg_body_full = msg_part.get_payload()
    msg_body = msg_body_full[1]  ###
    trade_acceptance_link = None
    msg_body_parts = msg_body.get_payload().split('\n')
    for body_part in msg_body_parts:
        body_part = body_part.replace("&amp;", "&")
        if test_string in body_part:
            start_index = body_part.index(test_string)
            end_index = start_index + body_part[start_index:].index(" ") - 1
            trade_acceptance_link = body_part[start_index: end_index]
            break
    return trade_acceptance_link

