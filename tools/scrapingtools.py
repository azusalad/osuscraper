from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from config import *

def create_driver():
    """Create webdriver"""
    options = webdriver.firefox.options.Options()
    #options.add_argument('--headless')
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference("browser.download.downloadDir", download_dir)
    options.set_preference("browser.download.defaultFolder", download_dir)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-osu-beatmap-archive")
    driver = webdriver.Firefox(executable_path=path, options=options)
    return driver

def login(driver, password):
    """Logs in to osu homepage"""
    driver.get("https://osu.ppy.sh/home")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.js-nav-toggle')))
    driver.find_element(By.CSS_SELECTOR,'.js-nav-toggle').click()
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("password").send_keys(Keys.RETURN)
    input("Press enter once you have completed the captcha (if there is one) and loaded to the next page")

def download(driver, song):
    """Download a song given the song id"""
    driver.get("https://osu.ppy.sh/beatmapsets/" + song)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME,'header-v4__title')))
    existence = driver.find_element(By.CSS_SELECTOR,'a.btn-osu-big:nth-child(2) > span:nth-child(1)') # download button
    if existence:
        # check if graveyard
        graveyard = driver.find_element(By.CLASS_NAME,"beatmapset-header__status").text
        if graveyard == 'GRAVEYARD' or graveyard == 'WIP':
            graveyard = True
        else:
            graveyard = False

        # download song, skip if graveyard
        if (graveyard and download_graveyards) or not graveyard:
            # download video
            if download_videos:
                print('Downloading: ' + str(song))
                driver.find_element(By.CSS_SELECTOR,'a.btn-osu-big:nth-child(2) > span:nth-child(1)').click()

            # download without video
            else:
                print('Downloading: ' + str(song))
                try:
                    driver.find_element(By.CSS_SELECTOR,'a.btn-osu-big:nth-child(3) > span:nth-child(1) > span:nth-child(1) > span:nth-child(2)').click()
                except:
                    driver.find_element(By.CSS_SELECTOR,'a.btn-osu-big:nth-child(2) > span:nth-child(1)').click()
    else:
        print('Song does not exist: ' + str(song))

def get_song_id(url):
    """Finds song id based on url"""
    return url.split('#')[0].split('/')[-1]

def ls_song_ids(f):
    """Gets a list of song ids given a ls file"""
    ls_id = []
    for x in f:
        try:
            x.split(' ')
        except:
            pass
        else:
            ls_id.append(x.split(' ')[0])
    return ls_id


