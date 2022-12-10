# osu!scraper
Automate mass downloads of beatmaps based on search query or friend's beatmaps.  There are two modes: search and friends.


The search mode downloads all ranked/approved and loved beatmaps based on search query.  For example, if you make your query 'touhou' then the scraper will download all beatmaps that appear as a search result from the query touhou.  The scraper will not download maps that you already own.

The friend's list mode downloads all the beatmaps that your friend has and you don't.

## Requirements
Python, argparse, selenium, time, getpass, tqdm

## Setup
Clone this repo, cd into the repo, and install requirements.

```sh
git clone
cd
pip install -r requirements.txt
```

Edit config.py with your desired preferences.  There are some options without any value currently (such as your username), so make sure you add yours.
Make sure you have downloaded the geckodriver and pointed to its location in config.py.
You can get the geckodriver from here: https://github.com/mozilla/geckodriver/releases

## Usage
```
usage: main.py [-h] -m MODE [-q QUERY] [-fl FRIENDSLIST]

options:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  Mode to run osuscraper. [friends/search]
  -q QUERY, --query QUERY
                        Search query if using search mode.
  -fl FRIENDSLIST, --friendslist FRIENDSLIST
                        Friend's beatmap list location.
```
Run the program with the mode you want (-m) and then either the search query or friend's list location based on the mode.

When running the program, the program will first ask for your osu password.  Enter your password.

Then after the program logs in to the website for you, the website may or may give you a captcha for you to solve.  After solving the captcha (if there is one), press enter and the program will start the download of beatmaps.

### Search Mode
Run main.py with search mode and the search query.  For example:

`python main.py -m search -q 'sword art online'`

will make the scraper with download all beatmaps from or related to Sword Art Online.

### Friend's List Mode
This mode will download all the beatmaps that your friend has.
First tell your friend to cd into his osu song directory.  Then do:


Linux:

`ls > friendslist.txt`

Windows:

`dir /B > friendslist.txt`


You can copy that text file to somewhere more convenient.
Run main.py with friend's list mode and the location of the friend's list.  For example:

`python main.py -m friends -fl friendslist.txt`

will make the scraper look in friendslist.txt (located in the same location as main.py) and download all the songs in there that you do not have.





