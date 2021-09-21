# -*- coding: utf-8 -*-
"""
1110262126	coronagraphseaton	dG];2Dj50Bde	coronagraphseaton@mgomailcs.xyz	coronagraphseaton	mail.mgomailcs.xyz
1111776084	criticquirky	12345@Water	criticquirky@mgomailcs.xyz	criticquirky	mail.mgomailcs.xyz
1111754951	deemzabra	Ba2Qw9tVGzYuDNM5	deemzabra@mgomailcs.xyz	deemzabra	mail.mgomailcs.xyz
1110202888	unveiledflavored	12345@Water	unveiledflavored@mgomailcs.xyz	unveiledflavored	mail.mgomailcs.xyz
"""

import os
from steampy.utils import GameOptions

# API Key
MY_API_KEY = ''

# Main Account details
ACCOUNT_NAME = ''
PASSWORD = ''
PATH_TO_STEAMGUARD_FILE = os.path.join('data', 'steam_guard_file', 'Steamguard.txt')

# Game Options
GAMEOPTIONS = GameOptions.CS

# Path to Pr rank sheet
# PATH_TO_PR_RANK_SHEET = os.path.join(r"\\DESKTOP-RNJHKP1\C Drive\Users\Aman Agarwal\Desktop\auto_boosting_script_4k", "database", "pr_rank_sheet.xlsx")
PATH_TO_PR_RANK_SHEET = os.path.join('data', 'pr_rank_sheet')

# Path to account trade history
PATH_TO_ACCOUNT_HISTORY = os.path.join("data", "account_trade_history")

# Path to account data
PATH_TO_ACCOUNT_DATA = os.path.join("data", "aman_batch_2.xlsx")

# path to account login timestamps
PATH_TO_ACCOUNT_LOGIN_TIMESTAMP = os.path.join('data', 'account_completion_date')

# path to account trade urls
PATH_TO_ACCOUNT_TRADE_URL = os.path.join('data', 'account_trade_url')

# path to accounts with error text file
PATH_TO_ACCOUNTS_WITH_ERROR_FILE = os.path.join('data', 'accounts_with_error.pkl')

# Path to inventory count logger
PATH_TO_INVENTORY_COUNT_LOGGER = os.path.join('data', 'inventory_count_time_logger.pkl')

# Target account inventory size
MAX_INVENTORY_SIZE = 1000

# Steam path
STEAM_PATH = os.path.join('C:\\', 'Program Files (x86)', 'Steam', 'Steam.exe')

# Windows resolution
w, h = 1920, 1080

# Threshold value to consider for checking data around.
nearby_snippet_check_threshold = 100

# Trade acceptance check on mail server
max_trade_acceptance_url_fetch_count = 10