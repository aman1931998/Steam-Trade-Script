# Steam-Trade-Script
Script for Handling Steam Trading and accepting the trade automatically.

## Requirements
1. A main steam account with Steam Mobile Authenticator enabled and maFile for the account.
2. A list of accounts from which account inventory needs to be traded out to main account. Accounts must have email guard active for atleast 21 days and account must be logged in into the target machine atleast 15 days back.
3. Port 143 and 220 for IMAP.
4. 1080P Screen
5. Script needs to run on Administrator.

## Features
1. Each Account's data is recorded and maintained in /data folder.
2. Script will log in into the Main Steam Account using Steampy library.
3. It will send Trade Offer from Main steam account to target Steam account.
4. The Script will log in the target steam account into Steam Client and open the Trade Offer.
5. The Trade Offer is accepted and then, the script logs in into the Email account for the target steam account to approve the confirmation email received for the Steam Trade Offer.
6. The Trade is validated after Trade is completed.

Configuration Options:
1. API Key.
2. Max Inventory Size.
3. Trade Acceptance Check Max attempts.


Python Libraries used: steampy, os, time, sys, datetime, pandas, pickle, pandas, urllib, subprocess, PIL, numpy, math, pyautogui, keyboard, imaplib, email.

Skillsets used: Python, Computer Vision, Automation, Database Management, IMAP connectivity, Email Domain Management. 
