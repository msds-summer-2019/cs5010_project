"""

CS5010: Final Project
Names: Aditi Rajagopal, Bradley Katcher, Charlie Putnam
Computing-ID: ar5vt, bk5pu, cmp2cz
Notes: Pulls win probability data from espn game webpage, and stores it in a csv
TO DO: clean up the csv and do something with it
"""

from lxml import html
import requests, json
import pandas as pd

win_pct_marker = "espn.gamepackage.probability.data = "

def is_wins(x):
    return win_pct_marker in x

def extractGameData(url):
    # Step 1: get html data from espn game page
    page = requests.get(url)
    pageHTML = html.fromstring(page.text)

    # Step 2: grab all scripts from espn game page
    scripts = pageHTML.cssselect('script')
    print(scripts)

    # Step 3: search scripts for "espn.gamepackage.probability.data" keyword
    target_script = next(script for script in scripts if is_wins(script.text_content()))
    js = target_script.text_content()
    target_line = next(line for line in js.splitlines() if is_wins(line))
    start = target_line.find(win_pct_marker)
    data = target_line[start + len(win_pct_marker):-1]
    gameJson = json.loads(data)
    return (gameJson)


url = 'https://www.espn.com/mens-college-basketball/game?gameId=401123374'
NCAA_Finals_Game = extractGameData(url)
NCAA_Finals_Game_PD = pd.DataFrame.from_records(NCAA_Finals_Game)
print(NCAA_Finals_Game_PD)

NCAA_Finals_Game_PD.to_csv('NCAA_Finals_Game.csv') #exports results to a csv