#!/usr/bin/env python3

from nba_api.stats.endpoints import teamdashboardbylastngames
import datetime
from basketball_reference_scraper.seasons import get_schedule, get_standings
from pandas.core.arrays.integer import Int8Dtype
from nba_api.stats.endpoints import leaguestandingsv3


class pair:
    def __init__(self, home, away, teams):
        self.homeID = teams[home]
        self.awayID = teams[away]
        self.homename = home
        self.awayname = away


def make_team_to_ID(season):    
    
    raw = leaguestandingsv3.LeagueStandingsV3(season = season) # this pulls out all standings data for 2021

    # get dictionary from raw
    Standings = raw.standings.get_dict()

    for n, i in enumerate(Standings['headers']):
        if i == 'TeamID':
            ID = n
        if i == 'TeamName':
            i_team = n
    
    teams = {}

    for team in Standings['data']:
        name = team[i_team]
        teams[name] = team[ID]

    return teams
    
def get_nba_schedule(game_date, team_to_ID):

    slate = []
    season = game_date.split("-")[0]

    year = get_schedule(season)
    day = year[year['DATE'] == game_date]

    for game in day.index:
        tempaway = day.at[game, 'VISITOR']
        if tempaway.split()[-1] == "Blazers":
            away = "Trail Blazers"
        else:
            away = tempaway.split()[-1]

        temphome = day.at[game, 'HOME']
        home = temphome.split()[-1]
        if temphome.split()[-1] == "Blazers":
            home = "Trail Blazers"
        else:
            home = temphome.split()[-1]

        slate.append(pair(home, away, team_to_ID))

    return slate

def get_stats(team_ID, end_date):

    temp_end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    temp_start = temp_end - datetime.timedelta(days = 50)
    start_date = str(temp_start)

    raw = teamdashboardbylastngames.TeamDashboardByLastNGames(team_id = team_ID, date_from_nullable = start_date, date_to_nullable = end_date)
    team_dashboard = raw.game_number_team_dashboard.get_dict()

    aggregate_data = {}

    for stat in team_dashboard['headers']:
        if 'PCT' in stat:
            continue
        elif 'RANK' in stat:
            continue
        elif 'GROUP' in stat:
            continue
        elif 'CF' in stat:
            continue
        else:
            aggregate_data[stat] = 0

    n_ten_game_spans = len(team_dashboard['data'])

    for i in range(n_ten_game_spans):   
        for j, header in enumerate(team_dashboard['headers']):
            if header in aggregate_data.keys():
                if type(team_dashboard['data'][i][j]) != str:   
                    aggregate_data[header] += team_dashboard['data'][i][j]
                else:
                    aggregate_data[header] = team_dashboard['data'][i][j]

    return aggregate_data

def main():
    game_date = "2022-03-21" #input("Enter game date in format 'Y-M-D': ")
    season = int(game_date.split("-")[0])
    month = int(game_date.split("-")[1])

    if month <= 9:
        season -= 1

    team_to_ID = make_team_to_ID(season)
    print("teams organized")

    slate = get_nba_schedule(game_date, team_to_ID)
    print("slate obtained")

    team_stats = {}

    for game in slate:
        team_stats[game.homename] = get_stats(game.homeID, game_date)
        team_stats[game.awayname] = get_stats(game.awayID, game_date)

    for key, value in team_stats.items():
        print(f"{key}'s stats:")
        for header, data in value.items():
            print(f"{header}: {data}")
        print()

if __name__ == "__main__":
    main()