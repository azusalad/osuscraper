from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import getpass
import argparse

from tools.friendscraper import download_friends
from tools.searchscraper import *
from tools.scrapingtools import *

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", required=True, help="Mode to run osuscraper.  [friends/search]")
parser.add_argument("-q", "--query", required=False, help="Search query if using search mode.")
parser.add_argument("-fl", "--friendslist", required=False, help="Friend's beatmap list location.")
args = parser.parse_args()

if args.mode == 'search' and not args.query:
    raise Exception('Search mode was specified but no query was provided')
elif args.mode == 'friends' and not args.friendslist:
    raise Exception('Search mode was specified but no query was provided')


# get user password
password = getpass.getpass("Enter your osu password (hidden): ")

# get driver
print('creating driver')
driver = create_driver()

# get main website and log in
login(driver, password)

if args.mode == 'friends':
    download_friends(driver, args.friendslist)
elif args.mode == 'search':
    search(driver, args.query, password)

input('Once all songs have finished downloading press enter to stop program')

driver.close()
