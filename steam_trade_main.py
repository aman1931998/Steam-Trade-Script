print("Script Name: steam_trade_main.py")
import time
import sys
from steampy.client import SteamClient, Asset
import config as cfg
from datetime import datetime

from helper_functions import check_and_create_account_trade_history_objects, cleanup_after_error
from snippet_functions import load_image_snippets, confirm_steam_client, confirm_steam_trade_offers, confirm_current_steam_trade_offer, \
    confirm_confirm_trade_contents_button, get_confirm_trade_contents_button_pixels, confirm_suspicious_trade_dialog_box, get_yes_this_is_a_gift_button, \
        confirm_accept_trade, get_accept_trade_button, confirm_email_authentication, get_email_authorization_needed_button
from steam_functions import open_trade_offers_page, open_trade_offer, launch_steam_and_login
from email_functions import establish_connection_to_mailserver, imap_login_into_mail, get_trade_acceptance_URL
from url_functions import load_url, parse_make_offer_with_url_output
from mouse_functions import scroll, click_only, hover_only
from inventory_functions import check_available_inventory_size, add_count_to_inventory_log, filter_tradable_inventory_items
from dynamic_data_functions import get_account_database, check_accounts_in_account_trade_history, load_account_trade_history_object, \
    save_account_trade_history_object, get_accounts_above_pr_rank_19, get_accounts_logged_in_15_days_ago, get_accounts_with_trade_url, \
        add_username_to_list_of_usernames_with_error
from cleaner import cleaner
# exclude_already_traded_accounts

print("Loading Account Data")
account_data = get_account_database()

print("Loading snippets")
snippets_dict = load_image_snippets()

above_pr_rank_19_accounts = get_accounts_above_pr_rank_19()
print("Found PR Rank >= 19 accounts: %d"%(len(above_pr_rank_19_accounts)))

accounts_logged_in_15_days_ago = get_accounts_logged_in_15_days_ago(above_pr_rank_19_accounts)
print("After filtering 15 days logged in accounts: %d"%(len(accounts_logged_in_15_days_ago)))

accounts_with_trade_url = get_accounts_with_trade_url(accounts_logged_in_15_days_ago)
print("After filtering accounts with trade URL: %d"%(len(accounts_with_trade_url)))

accounts_not_traded_yet = check_accounts_in_account_trade_history(accounts_with_trade_url)
print("After filtering already traded accounts: %d"%(len(accounts_not_traded_yet)))

print("Checking account history objects for filtered accounts.")
check_and_create_account_trade_history_objects(accounts_not_traded_yet)

if len(accounts_not_traded_yet) == 0:
    print("------------No accounts Found------------")
    sys.exit(0)

print("Checking if inventory space is available for current session.")
check_available_inventory_size(raise_exception = True)

print("Establishing connection to Steam Account")
steam_client = SteamClient(api_key = cfg.MY_API_KEY)
steam_client.login(username = cfg.ACCOUNT_NAME, password = cfg.PASSWORD, steam_guard = cfg.PATH_TO_STEAMGUARD_FILE)
print("Connection to Steam Account: %s Successful"%(cfg.ACCOUNT_NAME))

#%%
for username in accounts_not_traded_yet.keys(): # username = list(accounts_not_traded_yet.keys())[0]
    print("Checking if inventory space is available for current session.")
    check_available_inventory_size(raise_exception = True)

    print("Selected Username: %s"%(username))
    
    password = account_data[username]['Password']
    email_address = account_data[username]['Email_Address']
    email_password= account_data[username]['Email_Password']
    steamid = account_data[username]['SteamID']
    steam64id = account_data[username]['Steam64ID']
    domain = account_data[username]['Domain']
    trade_url = accounts_not_traded_yet[username]
    
    print("Loading Account_Trade data for selected account")
    account_trade = load_account_trade_history_object(username)
    
    try:
        print("Establishing connection to the mail server")
        imap = establish_connection_to_mailserver(domain = domain)
    except:
        print("Error while establishing connection to mail server.")
        add_username_to_list_of_usernames_with_error(username, "mail_server_connection")
        sys.exit(0)
    
    try:
        print("Logging in into the mail server")
        imap = imap_login_into_mail(imap, email_address, email_password)
    except:
        print("Error while logging in into mail server.")
        add_username_to_list_of_usernames_with_error(username, "mail_server_login")
        continue
    
    print("Fetching partner's inventory items")
    try:
        partner_items = steam_client.get_partner_inventory(str(steam64id), cfg.GAMEOPTIONS)
    except Exception as e:
        print("Failed to fetch inventory for the account.")
        print(e)
        partner_items = None
    if partner_items == None:
        print("Error with account %s while fetching inventory items."%(username))
        add_username_to_list_of_usernames_with_error(username, "fetching_inventory_items")
        continue
    print("Found %d items in inventory of %s"%(len(partner_items), username))
    account_trade.add_items_to_inventory(partner_items)
    save_account_trade_history_object(account_trade)
    
    print("Filtering tradable inventory items.")
    tradable_partner_items = filter_tradable_inventory_items(partner_items)
    tradable_partner_item_ids = [str(i['id']) for i in tradable_partner_items.values()]
    tradable_partner_assets = [Asset(asset_id = str(i), game = cfg.GAMEOPTIONS) for i in tradable_partner_item_ids]
    
    print("Sending a trade offer of %d inventory items"%(len(tradable_partner_items)))
    trade_offer_data = steam_client.make_offer_with_url(items_from_me = [], items_from_them = tradable_partner_assets, trade_offer_url = trade_url, message = "")
    
    if not parse_make_offer_with_url_output(trade_offer_data):
        print("Error with account %s while making trade offer."%(username))
        add_username_to_list_of_usernames_with_error(username, 'making_trade_offer')
        continue
    print("Trade offer created.")
    print("Updating database.")
    account_trade.add_trade_details_into_history(datetime.now(), tradable_partner_item_ids, trade_offer_data['tradeofferid'])
    save_account_trade_history_object(account_trade)

    print("Cleaning Earlier steam instances.")
    cleaner()
    
    print("Launching Steam")
    launch_steam_and_login(username = username, password = password)
    
    print("Confirming Steam launch")
    output = confirm_steam_client(snippets_dict)
    if output == False:
        print("Error while launching steam")
        add_username_to_list_of_usernames_with_error(username, "steam_launch")
        cleanup_after_error(imap, steam_client, trade_offer_data['tradeofferid'])
        continue # TODO add function to decline trade offer
    
    print("Opening Steam Trade Offer")
    open_trade_offers_page(steam64id)
    
    print("Confirming Trade Offers page.")
    output = confirm_steam_trade_offers(snippets_dict)
    if output == False:
        print("Error while confirming trade offers page")
        add_username_to_list_of_usernames_with_error(username, "trade_offers_page")
        cleanup_after_error(imap, steam_client, trade_offer_data['tradeofferid'])
        continue # TODO add function to decline trade offer
    
    print("Opening Trade offer sent by main account")
    open_trade_offer(trade_offer_data['tradeofferid'])
    
    print("Confirming current trade offer page.")
    output = confirm_current_steam_trade_offer(snippets_dict)
    if output == False:
        print("Error while confirming trade offer window")
        add_username_to_list_of_usernames_with_error(username, "trade_offer_window")
        cleanup_after_error(imap, steam_client, trade_offer_data['tradeofferid'])
        continue # TODO add function to decline trade offer
    
    print("Scrolling down on this page")
    hover_only(110, 453, 0.5, 0.5)
    click_only(None, None, 0.1, 1)
    scroll(3000, scroll_movement = 'down')
    print("Confirming 'confirm trade contents button'")
    
    # output = confirm_confirm_trade_contents_button(snippets_dict)
    # if output == False:
    #     print("Error while confirming 'confirm trade contents' button")
    #     add_username_to_list_of_usernames_with_error(username, 'confirm_trade_contents')
    #     cleanup_after_error(imap, steam_client, trade_offer_data['tradeofferid'])
    #     continue # TODO add function to decline trade offer
    
    # x, y = get_confirm_trade_contents_button_pixels(output[0], output[1])
    x, y = 995, 356
    print("Clicking on 'confirm trade contents' button")
    hover_only(x, y, 0.5, 0.5)
    click_only(None, None, 0.2, 1)
    
    print("Confirming trade suspicious window")
    output = confirm_suspicious_trade_dialog_box()
    if output == False:
        print("Error while confirming suspicious trade dialog box")
        add_username_to_list_of_usernames_with_error(username, 'suspicious_trade')
        cleanup_after_error(imap, steam_client, trade_offer_data['tradeofferid'])
        continue # TODO add function to decline trade offer
    
    print("Clicking on 'Yes, this is a gift' button")
    x, y = get_yes_this_is_a_gift_button(output[0], output[1])
    hover_only(x, y, 0.5, 0.5)
    click_only(None, None, 0.2, 1)
    
    print("Confirming accept trade button")
    output = confirm_accept_trade()
    if output == False:
        print("Error while confirming accept trade button")
        add_username_to_list_of_usernames_with_error(username, 'accept_trade')
        cleanup_after_error(imap, steam_client, trade_offer_data['tradeofferid'])
        continue # TODO add function to decline trade offer
    
    print("Clicking on 'Accept Trade' button")
    x, y = get_accept_trade_button(output[0], output[1])
    hover_only(x, y, 0.5, 0.5)
    click_only(None, None, 0.2, 1)
    
    print("Confirming additional confirmation needed OK button")
    output = confirm_email_authentication(snippets_dict)
    if output == False:
        print("Error while confirming additional email confirmation needed dialog box")
        add_username_to_list_of_usernames_with_error(username, 'email_confirmation_needed')
        cleanup_after_error(imap, steam_client, trade_offer_data['tradeofferid'])
        continue # TODO add function to decline trade offer
    
    print("Clicking on 'OK' button")
    x, y = get_email_authorization_needed_button(output[0], output[1])
    hover_only(x, y, 0.5, 0.5)
    click_only(None, None, 0.2, 1)
    
    print("Accepting trade offer PART Completed")
    print("Waiting 15 seconds for email to arrive into the mail server")
    time.sleep(15)
    
    print("Fetching Trade Acceptance link from email.")
    confirmation_rcvd, trade_acceptance_link = False, None
    for i in range(cfg.max_trade_acceptance_url_fetch_count):
        output = get_trade_acceptance_URL(imap, trade_offer_data['tradeofferid'], steamid)
        print(output)
        if len(output) == 2:
            print("Not Found")
            time.sleep(5)
        else:
            trade_acceptance_link = output
            break
    if trade_acceptance_link == None:
        print("Error fetching trade confirmation email")
        add_username_to_list_of_usernames_with_error(username, 'email_not_found')
        cleanup_after_error(imap, steam_client, trade_offer_data['tradeofferid'])
        continue # TODO add function to decline trade offer
    
    print("Opening URL")
    status_code = load_url(trade_acceptance_link)
    print(status_code)
    
    print("Getting Trade Status")
    trade_status = steam_client.get_trade_offer(trade_offer_data['tradeofferid'])
    if trade_status['response']['offer']['trade_offer_state'] not in [11, 3]:
        print("Error fetching trade confirmation email")
        add_username_to_list_of_usernames_with_error(username, trade_status['response']['offer']['trade_offer_state'])
    else:
        print("Steam Trade is now in ESCROW or ACCEPTED.")
        print("Trade ID: %s"%(trade_status['response']['offer']['tradeid']))
        print("Updating database")
        account_trade.Account_Covered = True
        account_trade.Trade_History[trade_offer_data['tradeofferid']].Trade_Status = True
        account_trade.Trade_History[trade_offer_data['tradeofferid']].TradeID = trade_status['response']['offer']['tradeid']
        save_account_trade_history_object(account_trade)    
        add_count_to_inventory_log(len(tradable_partner_assets))
        print("Username %s: COMPLETED"%(username))