import config as cfg
import pickle
from datetime import datetime

def load_inventory_count_log():
    with open(cfg.PATH_TO_INVENTORY_COUNT_LOGGER, 'rb') as file:
        inventory_counter = pickle.load(file)
    return inventory_counter

def save_inventory_count_log(inventory_counter):
    with open(cfg.PATH_TO_INVENTORY_COUNT_LOGGER, 'wb') as file:
        pickle.dump(inventory_counter, file)

def check_available_inventory_size(raise_exception = True):
    inventory_counter = load_inventory_count_log()
    current_datestamp = datetime.now()
    for i in range(len(inventory_counter) - 1): #i = 0
        start_datestamp = inventory_counter[i]['Datestamp']
        end_datestamp = inventory_counter[i + 1]['Datestamp']
        if current_datestamp > start_datestamp and current_datestamp < end_datestamp:
            if raise_exception:
                if inventory_counter[i]['Items_Traded'] > cfg.MAX_INVENTORY_SIZE: raise Exception("Inventory space not available for current session")
                else: return True
            else:
                if inventory_counter[i]['Items_Traded'] > cfg.MAX_INVENTORY_SIZE: return False
                else: return True

def add_count_to_inventory_log(count = 19):
    inventory_counter = load_inventory_count_log()
    current_datestamp = datetime.now()
    for i in range(len(inventory_counter) - 1): #i = 0
        start_datestamp = inventory_counter[i]['Datestamp']
        end_datestamp = inventory_counter[i + 1]['Datestamp']
        if current_datestamp > start_datestamp and current_datestamp < end_datestamp:
            inventory_counter[i]['Items_Traded'] += int(count)
    save_inventory_count_log(inventory_counter)

def filter_tradable_inventory_items(partner_items):
    tradable_partner_items = {}
    for item_id in partner_items.keys():
        if partner_items[item_id]['tradable'] == 1:
            tradable_partner_items[item_id] = partner_items[item_id]
    return tradable_partner_items
