import os
import subprocess
import config as cfg

def launch_steam_and_login(username, password, steam_path = cfg.STEAM_PATH):
    if steam_path == None:
        raise Exception("Steam path not given.")
    if not steam_path.endswith('Steam.exe'):
        raise Exception("Steam path Invalid.")
    if not os.path.isfile(steam_path):
        raise Exception("Steam path not found.")
    
    proc = subprocess.Popen(steam_path + " -login %s %s"%(str(username), str(password)))
    return proc


def open_trade_offers_page(steam64id):
    url = "steam://openurl/https://steamcommunity.com/profiles/%s/tradeoffers/"%(str(steam64id))
    os.startfile(url)

def open_trade_offer(tradeofferid):
    url = "steam://openurl/https://steamcommunity.com/tradeoffer/%s/"%(str(tradeofferid))
    os.startfile(url)

