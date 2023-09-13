# This script looks at the teams page and extracts data for each player
import re
import requests
from bs4 import BeautifulSoup

def extract_id_from_link(id_desc, link):
    pattern = fr'{id_desc}=(\d+)(?:&|$)'
    match = re.search(pattern, link)
    if match:
        value = match.group(1)
        return value
    else:
        return None

def extract_player_id_from_link(link):
    return extract_id_from_link('playerID', link)

def extract_team_id_from_link(link):
    return extract_id_from_link('teamID', link)

def extract_league_id_from_link(link):
    return extract_id_from_link('leagueID', link)

URL = 'https://www.hna.com/leagues/teamsV1.cfm?leagueID=6202&clientID=2296'

response = requests.get(URL)
team_list_soup = BeautifulSoup(response.content, 'html.parser')

tables = team_list_soup.find_all('table')

all_team_stats_links = []

# Links to team stats page is nested in a table. Extract all links containing "stats" in tables
for table in tables:
    for tr in table.find_all('tr'):
        for td in table.find_all('td'):
            team_stats_links = td.find_all('a', href=lambda href: (href and "stats" in href))
            for link in team_stats_links:
                all_team_stats_links.append(link['href'])

# Check each team stats link to extract player data 
all_player_stats = []
for link in all_team_stats_links:
    team_stats_url = f"https://www.hna.com/leagues/{link}"
    response = requests.get(team_stats_url)
    team_stats_soup = BeautifulSoup(response.content, 'html.parser')

    table = team_stats_soup.find('table', id='leaders')
    table.tfoot.decompose()
    for tr in table.find_all('tr')[1:]:
        columns = tr.find_all('td')
        player_stats = {
            'player_id': extract_player_id_from_link(columns[1].a.get('href')),
            'team_id': extract_team_id_from_link(link),
            'league_id': extract_league_id_from_link(link),
            'roster_num': columns[0].text.strip(),
            'player_name': columns[1].a.text,
            'player_num': columns[2].text.strip(),
            'position': columns[3].text.strip(),
            'games_played_num': columns[4].text.strip(),
            'num_goals': columns[5].text.strip(),
            'num_assists': columns[6].text.strip(),
            'num_points': columns[7].text.strip(),
            'num_pim': columns[8].text.strip()
        }
        all_player_stats.append(player_stats)

print(all_player_stats)