import os
import config as cfg
import pandas as pd
import pickle
from datetime import datetime, timedelta

def get_account_database(account_sheet_path = cfg.PATH_TO_ACCOUNT_DATA):
    data = pd.read_excel(account_sheet_path)
    print("Found a database of %d accounts"%(len(data)))
    steamIDs = data['SteamID']
    usernames = data['Username']
    passwords = data['Password']
    email_addresses = data['Email_Address']
    email_passwords = data['Email_Password']
    domains = data['Domain']
    data_dict = {}
    for i in range(len(usernames)):
        data_dict[usernames[i]] = {}
        data_dict[usernames[i]]['Password'] = passwords[i]
        data_dict[usernames[i]]['Email_Address'] = email_addresses[i]
        data_dict[usernames[i]]['Email_Password'] = email_passwords[i]
        data_dict[usernames[i]]['SteamID'] = steamIDs[i]
        data_dict[usernames[i]]['Steam64ID'] = Convert(str(steamIDs[i])).steam_id64_converter()
        data_dict[usernames[i]]['Domain'] = domains[i]
    return data_dict

#%%
def check_accounts_in_account_trade_history(usernames):
    l = {}
    for username in usernames.keys():
        if os.path.isfile(os.path.join(cfg.PATH_TO_ACCOUNT_HISTORY, username + ".pkl")):
            file = open(os.path.join(cfg.PATH_TO_ACCOUNT_HISTORY, username + ".pkl"), 'rb')
            account_data = pickle.load(file)
            file.close()
            if account_data.Account_Covered == True:
                continue
            else:
                l[username] = usernames[username]
        else:
            l[username] = usernames[username]
    return l

def load_account_trade_history_object(username):
    with open(os.path.join(cfg.PATH_TO_ACCOUNT_HISTORY, username + ".pkl"), 'rb') as file:
        account_trade = pickle.load(file)
    return account_trade

def save_account_trade_history_object(account_trade):
    with open(os.path.join(cfg.PATH_TO_ACCOUNT_HISTORY, account_trade.Username + ".pkl"), 'wb') as file:
        pickle.dump(account_trade, file)


#%%
def get_accounts_above_pr_rank_19():
    usernames, pr_ranks = [], []
    files = os.listdir(cfg.PATH_TO_PR_RANK_SHEET)
    for file_name in files: #file_name = files[0]
        data = pd.read_excel(os.path.join(cfg.PATH_TO_PR_RANK_SHEET, file_name))
        usernames += data['Username'].tolist()
        pr_ranks += data['PR_Rank'].tolist()
    l = []
    for i in range(len(usernames)):
        username = usernames[i]
        pr_rank = pr_ranks[i]
        if pr_rank in list(map(str, range(19, 40))) + list(range(19, 40)):
            l.append(username)
    return l

#%%
def get_accounts_logged_in_15_days_ago(usernames):
    l = []
    for username in usernames:
        if not os.path.isfile(os.path.join(cfg.PATH_TO_ACCOUNT_LOGIN_TIMESTAMP, username + ".txt")):
            continue
        login_timestamp = open(os.path.join(cfg.PATH_TO_ACCOUNT_LOGIN_TIMESTAMP, username + ".txt"), 'r').read()
        login_timestamp = datetime.strptime(login_timestamp, "%Y-%m-%d %H:%M:%S.%f")
        if datetime.now() > login_timestamp + timedelta(days = 15):
            l.append(username)
    return l

def get_accounts_with_trade_url(usernames):
    d = {}
    for username in usernames:
        if not os.path.isfile(os.path.join(cfg.PATH_TO_ACCOUNT_TRADE_URL, username + ".txt")):
            continue
        trade_url = open(os.path.join(cfg.PATH_TO_ACCOUNT_TRADE_URL, username + ".txt"), 'r').read()
        if 'steamcommunity.com/tradeoffer' in trade_url and 'token' in trade_url and 'partner=' in trade_url:
            d[username] = trade_url
    return d

#%%
def load_list_of_usernames_with_error():
    try:
        with open(cfg.PATH_TO_ACCOUNTS_WITH_ERROR_FILE, 'rb') as file:
            error_data = pickle.load(file)
        return error_data
    except:
        return {}

def add_username_to_list_of_usernames_with_error(username, error = "NA"):
    error_data = load_list_of_usernames_with_error()
    if error in error_data.keys():
        error_data[error].append(username)
    else:
        error_data[error] = [username]
    save_list_of_usernames_with_error(error_data)

def save_list_of_usernames_with_error(error_data):
    file = open(cfg.PATH_TO_ACCOUNTS_WITH_ERROR_FILE, 'wb')
    pickle.dump(error_data, file)
    file.close()

#%% CONVERT
class Convert(object):
    """Class for converting SteamID between different versions of it"""

    def __init__(self, steamid):
        """Init"""
        self.sid = steamid
        self.change_val = 76561197960265728
        self.alert()

    def set_steam_id(self, steamid):
        """Sets new steam ID"""
        self.sid = steamid
        self.recognize_sid()
        self.alert()

    def get_steam_id(self):
        """Returns given Steam ID"""
        return self.sid

    def recognize_sid(self, choice=0):
        """Recognized inputted steamID
        SteamID code = 1
        SteamID3 code = 2
        SteamID32 code = 3
        SteamID64 code = 4
        Not found = 0
        Choice int 1 or 0
        1- prints recognized steam ID and returns code
        0- Returns only code"""
        if choice != 0 and choice != 1:
            print('Assuming choice is 1')
            choice = 1
        if self.sid[0] == 'S':  # SteamID
            if choice == 1:
                print('Recognized ', self.sid, ' as SteamID')
            return 1
        elif self.sid[0] in ['U', 'I', 'M', 'G', 'A', 'P', 'C', 'g', 'T', 'L', 'C', 'a']:  # SteamID3
            if choice == 1:
                print('Recognized ', self.sid, ' as SteamID3')
            return 2
        elif self.sid[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and len(self.sid) < 17:  # SteamID32
            if choice == 1:
                print('Recognized ', self.sid, ' as SteamID32')
            return 3
        elif self.sid[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and len(self.sid) == 17:  # SteamID64
            if choice == 1:
                print('Recognized ', self.sid, ' as SteamID64')
            return 4
        else:
            if choice == 1:
                print(self.sid, 'is not recognized as any SteamID')
            return 0

    def alert(self):
        """Prints alert when user tries to convert one of special accounts"""
        recognized = self.recognize_sid(0)
        if recognized == 1:
            if self.sid[6] != '0':
                print('Result of converting:', self.sid, 'steam ID may not be correct')
        elif recognized == 2:
            if self.sid[0] != 'U':
                print('Result of converting:', self.sid, 'steam ID may not be correct')

    def steam_id_converter(self):
        """Converts other SteamID versions to steamID"""
        recognized = self.recognize_sid(0)
        if recognized == 1:  # Returns steamID
            return self.sid
        elif recognized == 2:  # Converts SteamID3 to SteamID
            steam3 = int(self.sid[4:])
            return 'STEAM_0:' + str(self.oddity(steam3)) + ':' + str(steam3 // 2)
        elif recognized == 3:  # Converts SteamID32 to SteamID
            steam3 = int(self.sid)
            return 'STEAM_0:' + str(self.oddity(steam3)) + ':' + str(steam3 // 2)
        elif recognized == 4:  # Converts SteamID64 SteamID64
            steam3 = int(self.steam_id32_converter())
            return 'STEAM_0:' + str(self.oddity(steam3)) + ':' + str(steam3 // 2)

    @staticmethod
    def oddity(number):
        """Checks oddity of given number"""
        if number % 2 == 0:
            return 0
        else:
            return 1

    def steam_id3_converter(self):
        """Converts other SteamID versions to SteamID3"""
        recognized = self.recognize_sid(0)
        if recognized == 1:  # Converts SteamID to SteamID3
            return 'U:1:' + str(self.steam_id32_converter())
        elif recognized == 2:  # returns SteamID3
            return self.sid
        elif recognized == 3:  # Converts SteamID32 to SteamID3
            return 'U:1:' + str(self.sid)
        elif recognized == 4:  # Converts SteamID64 to SteamID3
            return 'U:1:' + str(int(self.sid) - self.change_val)

    def steam_id32_converter(self):
        """Converts other steamID versions to steamID32"""
        recognized = self.recognize_sid(0)
        if recognized == 1:  # Converts from steamID to SteamID32
            y = self.sid[8:9]  # STEAM_0:y:zzzzzz
            z = self.sid[10:]  # STEAM_0:y:zzzzzz
            return int(z) * int(2) + int(y)
        elif recognized == 2:  # Converts from steamID3 to SteamID32
            return int(self.sid[4:])
        elif recognized == 3:  # Returns steamID32
            return int(self.sid)
        elif recognized == 4:  # Converts from steamID64 to SteamID32
            return int(self.sid) - self.change_val

    def steam_id64_converter(self):
        """Converts other SteamID versions to SteamID64"""
        recognized = self.recognize_sid(0)
        if recognized == 1:  # Converts from steamID to SteamID64
            y = self.sid[8:9]  # STEAM_0:y:zzzzzz
            z = self.sid[10:]  # STEAM_0:y:zzzzzz
            return int(z) * int(2) + int(y) + self.change_val
        elif recognized == 2:  # Converts steamID3 to SteamID64
            return int(self.sid[4:]) + self.change_val
        elif recognized == 3:  # Converts steamID32 to SteamID64
            return int(self.sid) + self.change_val
        elif recognized == 4:  # Returns steamID64
            return int(self.sid)

