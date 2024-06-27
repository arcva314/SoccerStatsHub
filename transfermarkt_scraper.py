import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import pickle
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}
def scrape_player_links():
    df = pd.read_csv('team_links.csv')
    data = df.iloc[0]
    links = []
    for thing in data:
        if thing != 0:
            links.append(thing)
    players = {}
    for link in links:
        for year in range(1992, 2024):
            url = link + str(year)
            print(url)
            data = requests.get(url, headers=headers)
            soup = BeautifulSoup(data.content, 'html.parser')
            player_elements = soup.find_all('table', class_="inline-table")
            for player_element in player_elements:
                try:
                    player_name = player_element.find('a').text.strip()
                    player_link = player_element.find('a')['href']
                    if player_name not in players:
                        players[player_name] = 'https://www.transfermarkt.us' + player_link
                    print(player_name, players[player_name])
                except:
                    continue
            time.sleep(2)
    return players
def dict_to_df(dick, path):
    names = dick.keys()
    links = [dick[name] for name in names]
    df = pd.DataFrame({"Player Names": names, "Links": links})
    df.to_csv(path)
def scrape_teams():
    la_liga_link = 'https://www.transfermarkt.us/laliga/tabelle/wettbewerb/ES1/saison_id/'
    prem_link = 'https://www.transfermarkt.us/premier-league/startseite/wettbewerb/GB1/saison_id/'
    serie_a_link = 'https://www.transfermarkt.us/serie-a/startseite/wettbewerb/IT1/saison_id/'
    bundesliga_link = 'https://www.transfermarkt.us/bundesliga/startseite/wettbewerb/L1/saison_id/'
    ligue_1_link = 'https://www.transfermarkt.us/ligue-1/startseite/wettbewerb/FR1/saison_id/'
    leagues = [la_liga_link, prem_link, serie_a_link, bundesliga_link, ligue_1_link]
    teams = {}
    for year in range(1992, 2024):
        for league in leagues:
            url = league + str(year)
            data = requests.get(url, headers=headers)
            soup = BeautifulSoup(data.content, "html.parser")
            team_elements = soup.find_all('td', class_='zentriert no-border-rechts')
            for team_element in team_elements:
                team_name = team_element.find('a')['title']
                team_link = team_element.find('a')['href']
                if team_name not in teams:
                    teams[team_name] = 'https://www.transfermarkt.us' + str(team_link).replace('spielplan', 'startseite')[:-4]
            time.sleep(3)
            print(year, league)
    return teams
def scrape(url, player_name):
    data=requests.get(url, headers=headers)
    soup = BeautifulSoup(data.content, "html.parser")

    name_pattern = "Name in home country:</span>\s*<span class=\"info-table__content info-table__content--bold\">(.*?)</span>"
    dob_pattern = "Date of birth/Age:</span>\s*<span class=\"info-table__content info-table__content--bold\">\s*<a.*\">(.*?)</a>"
    h_pattern = "Height:.*\s*.*\">(.*?)</span>"
    pos_pattern = "Position:.*\s*.*\s*(.*?)\s*</span>"
    foot_pattern = "Foot:.*\s*.*\">(.*?)</span>"

    #name = re.search(name_pattern, str(soup)).group(1)
    name = player_name
    try:
        dob = re.search(dob_pattern, str(soup)).group(1)
    except:
        dob = "Unknown"
    try:
        height = re.search(h_pattern, str(soup)).group(1)
        height = height[:4].replace(',', '.')
    except:
        height = "Unknown"
    try:
        pos = re.search(pos_pattern, str(soup)).group(1)
    except:
        pos = "Unknown"
    try:
        foot = re.search(foot_pattern, str(soup)).group(1)
    except:
        foot = "Unknown"
    return {"Player Name": name, "Date of Birth (Age)": dob, "Height (m)": height, "Position": pos, "Preferred Foot": foot}
def setup_players():
    with open('data.pkl', 'rb') as file:
        index = pickle.load(file)
        result = pickle.load(file)
    #index = 0
    df = pd.read_csv('player_links.csv')
    names = df['Player Names']
    links = df['Links']
    #result = {"Player ID": [], "Player Name": [], "Date of Birth (Age)": [], "Height (m)": [], "Position": [], "Preferred Foot": []}
    for i in range(index, len(names)):
        data = scrape(links[i], names[i])
        result["Player ID"].append(i)
        for key in data:
            result[key].append(data[key])
        print(i, names[i])
        if i % 500 == 0:
            with open('data.pkl', 'wb') as file:
                pickle.dump(i, file)
                pickle.dump(result, file)
    return result
def scrape_manager(name, url, season):
    url = url + '/plus/0?saison_id=' + str(season)
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.content, 'html.parser')
    result = soup.find_all('div', class_='box')[1]
    heads = result.find_all_next('th', class_='zentriert')
    info = result.find_all_next('td', class_='zentriert')
    manager_season_info = {"Name": name, "Season": str(season) + '/' + str(season+1)[-2:]}
    for i in range(len(heads)):
        manager_season_info[heads[i].text] = info[i].text
    return manager_season_info
def setup_manager():
    with open('manager_data.pkl', 'rb') as file:
        index = pickle.load(file)
        manager_data = pickle.load(file)
    links = ['https://www.transfermarkt.us/premier-league/erfolgreicheTrainer/pokalwettbewerb/GB1/plus//galerie/0?aktiveTrainer=&saisonIdVon=1992&saisonIdBis=2024&anzahl=50&group=',
             'https://www.transfermarkt.com/laliga/erfolgreicheTrainer/pokalwettbewerb/ES1/plus//galerie/0?aktiveTrainer=&saisonIdVon=1992&saisonIdBis=2024&anzahl=50&group=',
             'https://www.transfermarkt.us/bundesliga/erfolgreichetrainer/wettbewerb/L1/plus/?aktiveTrainer=&saisonIdVon=1992&saisonIdBis=2023&anzahl=50&group=',
             'https://www.transfermarkt.us/serie-a/erfolgreichetrainer/wettbewerb/IT1/plus/?aktiveTrainer=&saisonIdVon=1992&saisonIdBis=2023&anzahl=50&group=',
             'https://www.transfermarkt.us/ligue-1/erfolgreichetrainer/wettbewerb/FR1/plus/?aktiveTrainer=&saisonIdVon=1992&saisonIdBis=2024&anzahl=50&group=',
             'https://www.transfermarkt.us/premier-league/erfolgreicheTrainer/pokalwettbewerb/GB1/aktiveTrainer//saisonIdVon/1992/saisonIdBis/2024/anzahl/50/group//plus//galerie/0/page/2',
             'https://www.transfermarkt.us/premier-league/erfolgreicheTrainer/pokalwettbewerb/GB1/aktiveTrainer//saisonIdVon/1992/saisonIdBis/2024/anzahl/50/group//plus//galerie/0/page/3',
             'https://www.transfermarkt.us/premier-league/erfolgreicheTrainer/pokalwettbewerb/GB1/aktiveTrainer//saisonIdVon/1992/saisonIdBis/2024/anzahl/50/group//plus//galerie/0/page/4',
             'https://www.transfermarkt.us/premier-league/erfolgreicheTrainer/pokalwettbewerb/GB1/aktiveTrainer//saisonIdVon/1992/saisonIdBis/2024/anzahl/50/group//plus//galerie/0/page/5',
             'https://www.transfermarkt.us/laliga/erfolgreicheTrainer/pokalwettbewerb/ES1/aktiveTrainer//saisonIdVon/1992/saisonIdBis/2024/anzahl/50/group//plus//galerie/0/page/2',
             'https://www.transfermarkt.us/laliga/erfolgreicheTrainer/pokalwettbewerb/ES1/aktiveTrainer//saisonIdVon/1992/saisonIdBis/2024/anzahl/50/group//plus//galerie/0/page/3',
             'https://www.transfermarkt.us/laliga/erfolgreicheTrainer/pokalwettbewerb/ES1/aktiveTrainer//saisonIdVon/1992/saisonIdBis/2024/anzahl/50/group//plus//galerie/0/page/4',
             'https://www.transfermarkt.us/laliga/erfolgreicheTrainer/pokalwettbewerb/GB1/aktiveTrainer//saisonIdVon/1992/saisonIdBis/2024/anzahl/50/group//plus//galerie/0/page/5',
             'https://www.transfermarkt.us/bundesliga/erfolgreicheTrainer/pokalwettbewerb/L1/aktiveTrainer//saisonIdVon/1992/saisonIdBis/2024/anzahl/50/group//plus//galerie/0/page/2',
             'https://www.transfermarkt.us/bundesliga/erfolgreicheTrainer/pokalwettbewerb/L1/aktiveTrainer//saisonIdVon/1992/saisonIdBis/2024/anzahl/50/group//plus//galerie/0/page/3',
             'https://www.transfermarkt.us/bundesliga/erfolgreicheTrainer/pokalwettbewerb/L1/aktiveTrainer//saisonIdVon/1992/saisonIdBis/2024/anzahl/50/group//plus//galerie/0/page/4',
             'https://www.transfermarkt.us/bundesliga/erfolgreicheTrainer/pokalwettbewerb/L1/aktiveTrainer//saisonIdVon/1992/saisonIdBis/2024/anzahl/50/group//plus//galerie/0/page/5',
             'https://www.transfermarkt.us/serie-a/erfolgreicheTrainer/pokalwettbewerb/IT1/aktiveTrainer//saisonIdVon/1992/saisonIdBis/2024/anzahl/50/group//plus//galerie/0/page/2',
             'https://www.transfermarkt.us/serie-a/erfolgreicheTrainer/pokalwettbewerb/IT1/aktiveTrainer//saisonIdVon/1992/saisonIdBis/2024/anzahl/50/group//plus//galerie/0/page/3',
             'https://www.transfermarkt.us/serie-a/erfolgreicheTrainer/pokalwettbewerb/IT1/aktiveTrainer//saisonIdVon/1992/saisonIdBis/2024/anzahl/50/group//plus//galerie/0/page/4',
             'https://www.transfermarkt.us/serie-a/erfolgreicheTrainer/pokalwettbewerb/IT1/aktiveTrainer//saisonIdVon/1992/saisonIdBis/2024/anzahl/50/group//plus//galerie/0/page/5',
             'https://www.transfermarkt.us/ligue-1/erfolgreicheTrainer/pokalwettbewerb/FR1/aktiveTrainer//saisonIdVon/1992/saisonIdBis/2024/anzahl/50/group//plus//galerie/0/page/2',
             'https://www.transfermarkt.us/ligue-1/erfolgreicheTrainer/pokalwettbewerb/FR1/aktiveTrainer//saisonIdVon/1992/saisonIdBis/2024/anzahl/50/group//plus//galerie/0/page/3',
             'https://www.transfermarkt.us/ligue-1/erfolgreicheTrainer/pokalwettbewerb/FR1/aktiveTrainer//saisonIdVon/1992/saisonIdBis/2024/anzahl/50/group//plus//galerie/0/page/4',
             'https://www.transfermarkt.us/ligue-1/erfolgreicheTrainer/pokalwettbewerb/FR1/aktiveTrainer//saisonIdVon/1992/saisonIdBis/2024/anzahl/50/group//plus//galerie/0/page/5']
    for i in range(index, len(links)):
        print(links[i])
        data = requests.get(links[i], headers=headers)
        soup = BeautifulSoup(data.content, 'html.parser')
        elements = soup.find_all('td', class_='hauptlink')
        for elements in elements:
            try:
                name = elements.find('a')['title']
                url = 'https://www.transfermarkt.us' + elements.find('a')['href']
                url = url.replace('profil', 'leistungsdatenDetail')
                for year in range(1992, 2024):
                    x = scrape_manager(name, url, year)
                    print(x)
                    if x['Matches'] != '0':
                        for key in x:
                            if key in manager_data:
                                manager_data[key].append(x[key])
                            else:
                                manager_data[key] = [x[key]]
            except:
                continue
        with open('manager_data.pkl', 'wb') as file:
            pickle.dump(i+1, file)
            pickle.dump(manager_data, file)
    return manager_data

data = setup_manager()
df = pd.DataFrame(data)
df.to_csv('manager_seasons.csv')

