import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import pickle
def scrape_player_season(url):
    driver = webdriver.Chrome()
    driver.get(url)
    link_text = ['Defensive','Offensive','Passing']
    for link in link_text:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, link))
        )
        link_element = driver.find_element(By.LINK_TEXT, link)
        link_element.click()
        case = ""
        if link == "Defensive":
            case = 'td.foulsPerGame'
        elif link == 'Offensive':
            case = 'td.dribbleWonPerGame'
        else:
            case = 'td.accurateLongPassPerGame'
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, case)))
        except:
            return
        html_code = driver.page_source
        soup = BeautifulSoup(html_code, 'html.parser')
        player_name = soup.find('h1', class_='header-name').text
        if link == 'Passing':
            df = pd.read_html(html_code)
            for d in df:
                d.drop(columns=['Season.1', 'Team.1'], inplace=True)
            merged_df = pd.merge(df[0], df[1], on=['Season', 'Team', 'Tournament', 'Apps', 'Mins', 'Rating'], how='outer')
            merged_df = pd.merge(merged_df, df[2], on=['Season', 'Team', 'Tournament', 'Apps', 'Mins', 'Rating', 'Assists', 'Goals', 'SpG'], how='outer')
            merged_df = pd.merge(merged_df, df[3],
                                 on=['Season', 'Team', 'Tournament', 'Apps', 'Mins', 'Rating', 'Assists', 'KeyP', 'PS%'],
                                 how='outer')
            merged_df.rename(columns={'Yel': 'Yellow Cards', 'Red': 'Red Cards', 'SpG': 'Shots Per Goal', 'PS%': 'Passing Accuracy', 'AerialsWon':'Aerial Duels Won', 'Tackles': 'Tackles Per Game',
                                      'Inter': 'Interceptions Per Game', 'Fouls': 'Fouls Per Game', 'Offsides': 'Offsides Won Per Game', 'Clear': 'Clearances Per Game', 'Drb_x': 'Times Dribbled Past Per Game',
                                      'Blocks': 'Blocks Per Game', 'OwnG': 'Own Goals', 'KeyP': 'Key Passes Per Game', 'Drb_y': 'Dribbles Per Game', 'Fouled': 'Fouled Per Game', 'Off': 'Offsides Per Game',
                                      'Disp': 'Times Dispossessed Per Game', 'UnsTch': 'Poor Touches Per Game', 'AvgP': 'Key Passes Per Game', 'Crosses': 'Successful Crosses Per Game', 'LongB': 'Successful Long Balls Per Game', 'ThrB': 'Successful Through Balls Per Game'}, inplace=True)
            merged_df['Player Name'] = player_name.strip()
            merged_df = merged_df[:-4]
            return merged_df
def scrape_league_season(driver, season, data):
    print(data)
    season_dropdown = Select(WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'seasons'))
    ))
    driver.set_page_load_timeout(30)
    try:
        season_dropdown.select_by_visible_text(season)
    except:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.team-link'))
        )
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a.team-link'))
    )
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('tbody', class_='standings')
    links = table.find_all('a', class_='team-link')
    for link in links:
        team = link.text
        url = 'https://whoscored.com' + link['href']
        url = url.replace('Show', 'Archive')
        if team not in data:
            data[team] = url
def scrape_links():
    with open('whoscored_teams.pkl', 'rb') as file:
        index = pickle.load(file)
        data = pickle.load(file)
    urls = ['https://www.whoscored.com/Regions/252/Tournaments/2/England-Premier-League',
            'https://www.whoscored.com/Regions/81/Tournaments/3/Germany-Bundesliga',
            'https://www.whoscored.com/Regions/206/Tournaments/4/Spain-LaLiga',
            'https://www.whoscored.com/Regions/108/Tournaments/5/Italy-Serie-A',
            'https://www.whoscored.com/Regions/74/Tournaments/22/France-Ligue-1']
    for i in range(index, len(urls)):
        driver = webdriver.Chrome()
        driver.set_page_load_timeout(30)
        try:
            driver.get(urls[i])
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            s = soup.find('select', id='seasons')
            options = s.find_all('option')
            seasons = [j.text for j in options]
            for season in seasons:
                if i == 3 and (season == '2022/2023' or season == '2004/2005' or season == '2002/2003' or season == '2000/2001' or season == '1999/2000'):
                    continue
                scrape_league_season(driver, season, data)
        except:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            s = soup.find('select', id='seasons')
            options = s.find_all('option')
            seasons = [j.text for j in options]
            for season in seasons:
                if i == 3 and (season == '2022/2023' or season == '2004/2005' or season == '2002/2003' or season == '2000/2001' or season == '1999/2000'):
                    continue
                scrape_league_season(driver, season, data)
        with open('whoscored_teams.pkl', 'wb') as file:
            pickle.dump(i+1, file)
            pickle.dump(data, file)
    return data
def extract_player_links(team_link, data):
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(40)
    print(team_link)
    try:
        driver.get(team_link)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    except:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    stage = soup.find('select', id='stageId')
    options = stage.find_all('option')
    seasons = [s['value'] for s in options]
    for season in seasons:
        url = team_link + '?stageId=' + season
        print(url)
        driver = webdriver.Chrome()
        driver.set_page_load_timeout(40)
        try:
            driver.get(url)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td.manOfTheMatch')))
        except:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td.manOfTheMatch')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links = soup.find_all('a', class_='player-link')
        driver.quit()
        for i in range(len(links)):
            player_url = 'https://www.whoscored.com' + links[i]['href']
            player_name = player_url.split('/')[-1]
            print(player_name, player_url)
            if player_name not in data:
                data[player_name] = player_url

with open('player_data.pkl', 'rb') as file:
    index = pickle.load(file)
    dfs = pickle.load(file)
player_season_data = pd.concat(dfs)
player_season_data.to_csv('player_seasons.csv')

