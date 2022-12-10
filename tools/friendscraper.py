from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import time

from config import *
from tools.scrapingtools import *

def download_friends(driver, friendslist):
    """Download all songs in the friendslist"""
    # get friends list
    with open(friendslist, 'r') as f:
        friendsongs = f.readlines()
    friendsongs = ls_song_ids(friendsongs)

    # download songs
    for song in tqdm(friendsongs):
        if song not in ls_song_ids(song_dir):
            download(driver, song)
            time.sleep(cooldown)


