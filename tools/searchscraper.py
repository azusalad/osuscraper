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

def cycle(driver):
    """Cycles though the current page of songs"""
    index = 0
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.newHeader')))
    beatmap_page = driver.current_url
    songs_a = driver.find_elements(By.CLASS_NAME,'title') # just to know how many there are for index.  solution to stale elements
    if len(songs_a) > 0:
        print('Downloading page')
        for songs in tqdm(songs_a):
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.newHeader')))
            songs = driver.find_elements(By.CLASS_NAME,'title') # get all songs
            driver.execute_script("arguments[0].scrollIntoView();", songs[index]) # scroll to current song
            song_id = songs[index].get_attribute('href').split('/')[-1] # get song id
            if song_id not in ls_song_ids(song_dir):
                download(driver, song_id)
                time.sleep(cooldown)
            else:
                time.sleep(cooldown/5)
            index += 1
            driver.get(beatmap_page)

        # load next page by adding +1 to page=
        driver.get("=".join(x for x in beatmap_page.split('=')[:-1]) + '=' + str(int(beatmap_page.split('=')[-1]) + 1))
    else:
        set_finish = True

def search(query, password):
    """Search mode of osuscraper"""
    set_finish = False
    driver.get('https://old.ppy.sh/p/beatmaplist') # goes to the old site which has pagination
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.newHeader'))) # waits until site loads
    driver.find_element(By.CLASS_NAME,'login-open-button').click()
    time.sleep(1)
    driver.find_element_by_id('username-field').send_keys(username)
    driver.find_element_by_id('password-field').send_keys(password)
    driver.find_element_by_id('password-field').send_keys(Keys.RETURN) # logs in
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'header-v4__title'))) # wait for load
    driver.get('https://old.ppy.sh/p/beatmaplist?m=0&r=0&g=0&la=0') # since it redirects to the new site
    time.sleep(1)
    driver.refresh()
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.newHeader'))) # wait for page to load

    # search
    driver.find_element(By.CSS_SELECTOR,'#searchArea > dl:nth-child(1) > dd:nth-child(2) > input:nth-child(1)').send_keys(query)
    driver.find_element(By.CSS_SELECTOR,'#searchArea > dl:nth-child(1) > dd:nth-child(2) > input:nth-child(1)').send_keys(Keys.RETURN)
    driver.get(driver.current_url + '&page=1')

    # cycle until finished downloading all ranked maps
    while not set_finish:
        cycle(driver)
    driver.find_element(By.CSS_SELECTOR,'#searchArea > dl:nth-child(4) > dd > a:nth-child(4)').click() # move to loved maps
    set_finish = False
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#searchArea > dl:nth-child(4) > dd > a:nth-child(4)')))
    driver.get(driver.current_url + '&page=1')

    # cycle until finished downloading all loved maps
    while not set_finish:
        cycle(driver)


