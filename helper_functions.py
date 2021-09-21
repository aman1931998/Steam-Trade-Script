from datetime import datetime
import pickle
import os
import config as cfg

def cleanup_after_error(imap, steam_client, trade_offer_id):
    steam_client.cancel_trade_offer(trade_offer_id = trade_offer_id)
    imap.logout()
    return imap, steam_client

def clean_timestamp(timestamp):
    if type(timestamp) == datetime:
        return timestamp
    elif type(timestamp) == str:
        return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    else:
        raise Exception("Invalid timestamp value.")

def check_and_create_account_trade_history_objects(usernames_data):
    for username in usernames_data.keys():
        if not os.path.isfile(os.path.join(cfg.PATH_TO_ACCOUNT_HISTORY, username + ".pkl")):
            account_trade_object = Account_Trade()
            account_trade_object.Username = username
            account_trade_object.Trade_URL = usernames_data[username]
            with open(os.path.join(cfg.PATH_TO_ACCOUNT_HISTORY, username + ".pkl"), 'wb') as file:
                pickle.dump(account_trade_object, file)

#%%
#%% 
class Account_Trade_Trade_History_Value():
    _Trade_Status = False
    TradeID = None

    def __init__(self, timestamp, asset_ids):
        self.Timestamp = clean_timestamp(timestamp)
        self.Asset_IDs = asset_ids
    
    @property
    def Trade_Status(self):
        return self._Trade_Status
    
    @Trade_Status.setter
    def Trade_Status(self, trade_status):
        self._Trade_Status = bool(trade_status)

class Account_Trade():
    def __init__(self):
        self.Account_Covered = False
        self._Username = None
        self._Trade_URL = None
        self._Total_Inventory_Count = 0
        self.Inventory_Items = {}
        self.Trade_History = {}
    
    def add_items_to_inventory(self, items):
        for item_id, data in items.items():
            if item_id in self.Inventory_Items.keys():
                continue
            self.Inventory_Items[item_id] = data
            self.increment_total_inventory_count(count = 1)
    
    def add_trade_details_into_history(self, timestamp, asset_ids, tradeofferid):
        obj = Account_Trade_Trade_History_Value(timestamp, asset_ids)
        self.Trade_History[str(tradeofferid)] = obj
    
    @property
    def Username(self):
        return str(self._Username)
    
    @Username.setter
    def Username(self, username):
        self._Username = str(username)
    
    @property
    def Trade_URL(self):
        if self._Trade_URL == None:
            return None
        return str(self._Trade_URL)
    
    @Trade_URL.setter
    def Trade_URL(self, trade_url):
        self._Trade_URL = str(trade_url)
    
    @property
    def Total_Inventory_Count(self):
        return int(self._Total_Inventory_Count)
    
    @Total_Inventory_Count.setter
    def Total_Inventory_Count(self, total_inventory_count):
        self._Total_Inventory_Count = int(total_inventory_count)
    
    def increment_total_inventory_count(self, count = 1):
        self.Total_Inventory_Count += int(count)

