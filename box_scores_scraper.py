# This script looks at a single day of game scores and extracts the box scores for each game

import requests
from bs4 import BeautifulSoup

URL = 'https://www.hna.com/leagues/schedules.cfm?leagueID=6202&clientID=2296&showDate=2023%2D08%2D29&today=1&printPage=0'

response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

# Extracting the links to box score pages
box_score_links = []
table = soup.find_all('table')[1] # Find second table on the page

for row in table.find_all('tr')[1:]:  # [1:] to skip header row
    link_cell = row.find('a', href=True)  # Finds the first <a> tag with an href attribute
    if link_cell:
        box_score_links.append(link_cell['href'])

all_game_stats = []

for link in box_score_links:
    box_score_url = f"https://www.hna.com/leagues/{link}"  # Add relative link to box score page
    response = requests.get(box_score_url)
    box_soup = BeautifulSoup(response.content, 'html.parser')

    #Now extract the desired box score data
    game_stats = []
    table = box_soup.find_all('table')[1]
    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        team_stats = {
            'name': columns[0].a.text,
            'first_period_goals': columns[1].text.strip(),
            'second_period_goals': columns[2].text.strip(),
            'third_period_goals': columns[3].text.strip()
        }
        num_columns = len(columns)
        if num_columns > 5:
            team_stats['overtime_goals'] = columns[4].text.strip()
            if num_columns > 6:
                team_stats['shoot_out'] = columns[5].text.strip()
                team_stats['total_goals'] = columns[6].text.strip()
            else:
                team_stats['total_goals'] = columns[5].text.strip()
        else:
            team_stats['total_goals'] = columns[4].text.strip()

        game_stats.append(team_stats)

    all_game_stats.append(game_stats)

print(all_game_stats)