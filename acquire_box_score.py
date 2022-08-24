import basketball_reference_web_scraper 
from basketball_reference_web_scraper import client
import pandas as pd
import datetime
import os 

def scrape_data(start_year, start_month, start_day, end_year, end_month, end_day):  

    # convert individual values to dates
    start_date = datetime.date(start_year, start_month, start_day)
    end_date = datetime.date(end_year, end_month, end_day)
    delta = datetime.timedelta(days=1)

    # initialize dataframe to store every box score from selected range
    box_scores = pd.DataFrame()

    # iterate from start date to end date
    while start_date <= end_date:
        year = int(str(start_date).split("-")[0])
        month = int(str(start_date).split("-")[1])
        day = int(str(start_date).split("-")[2])

        # pull selected day box scores from basketballreference.com
        today = client.team_box_scores(day=day, month=month, year=year)

        # iterate through all games of the day and add their values to box_scored dataframe
        for game in today:
            temp = pd.DataFrame([game])
            temp['date'] = start_date
            box_scores = pd.concat([box_scores, temp], ignore_index=True)

        start_date += delta

    return box_scores

def revise_box_scores(box_scores):    

    # initialize new columns of box_scores dataframe
    box_scores['opponent'] = ' '
    box_scores['against_made_field_goals'] = 0
    box_scores['against_attempted_field_goals'] = 0
    box_scores['against_made_three_point_field_goals'] = 0
    box_scores['against_attempted_three_point_field_goals'] = 0
    box_scores['against_made_free_throws'] = 0
    box_scores['against_attempted_free_throws'] = 0
    box_scores['against_offensive_rebounds'] = 0
    box_scores['against_defensive_rebounds'] = 0
    box_scores['against_assists'] = 0
    box_scores['against_steals'] = 0
    box_scores['against_blocks'] = 0
    box_scores['against_turnovers'] = 0
    box_scores['against_personal_fouls'] = 0
    box_scores['against_points'] = 0
    box_scores['game_ID'] = 0

    # create new dataframe that will contain revised box_score data
    revised_box_scores = pd.DataFrame()

    # number of games = length of box score values
    nGames = len(box_scores.index)

    i = 0
    game_ID = 1

    # iterate through all games
    # opponent pairs are next to each other so i and i+1 are from the same  game
    # thus, against stats can be taken from the neighboring rows
    while i < nGames:

        box_scores.at[i, 'opponent'] = box_scores.at[i+1, 'team']
        box_scores.at[i, 'against_made_field_goals'] = box_scores.at[i+1, 'made_field_goals']
        box_scores.at[i, 'against_attempted_field_goals'] = box_scores.at[i+1, 'attempted_field_goals']
        box_scores.at[i, 'against_made_three_point_field_goals'] = box_scores.at[i+1, 'made_three_point_field_goals']
        box_scores.at[i, 'against_attempted_three_point_field_goals'] = box_scores.at[i+1, 'attempted_three_point_field_goals']
        box_scores.at[i, 'against_made_free_throws'] = box_scores.at[i+1, 'made_free_throws']
        box_scores.at[i, 'against_attempted_free_throws'] = box_scores.at[i+1, 'attempted_free_throws']
        box_scores.at[i, 'against_offensive_rebounds'] = box_scores.at[i+1, 'offensive_rebounds']
        box_scores.at[i,'against_defensive_rebounds'] = box_scores.at[i+1,'defensive_rebounds']
        box_scores.at[i,'against_assists'] = box_scores.at[i+1, 'assists']
        box_scores.at[i,'against_steals'] = box_scores.at[i+1, 'steals']
        box_scores.at[i,'against_blocks'] = box_scores.at[i+1, 'blocks']
        box_scores.at[i,'against_turnovers'] = box_scores.at[i+1, 'turnovers']
        box_scores.at[i,'against_personal_fouls'] = box_scores.at[i+1, 'personal_fouls']
        box_scores.at[i,'against_points'] = box_scores.at[i+1, 'points']

        box_scores.at[i+1, 'opponent'] = box_scores.at[i, 'team']
        box_scores.at[i+1, 'against_made_field_goals'] = box_scores.at[i, 'made_field_goals']
        box_scores.at[i+1, 'against_attempted_field_goals'] = box_scores.at[i, 'attempted_field_goals']
        box_scores.at[i+1, 'against_made_three_point_field_goals'] = box_scores.at[i, 'made_three_point_field_goals']
        box_scores.at[i+1, 'against_attempted_three_point_field_goals'] = box_scores.at[i, 'attempted_three_point_field_goals']
        box_scores.at[i+1, 'against_made_free_throws'] = box_scores.at[i, 'made_free_throws']
        box_scores.at[i+1, 'against_attempted_free_throws'] = box_scores.at[i, 'attempted_free_throws']
        box_scores.at[i+1, 'against_offensive_rebounds'] = box_scores.at[i, 'offensive_rebounds']
        box_scores.at[i+1,'against_defensive_rebounds'] = box_scores.at[i,'defensive_rebounds']
        box_scores.at[i+1,'against_assists'] = box_scores.at[i,'assists']
        box_scores.at[i+1,'against_steals'] = box_scores.at[i,'steals']
        box_scores.at[i+1,'against_blocks'] = box_scores.at[i,'blocks']
        box_scores.at[i+1,'against_turnovers'] = box_scores.at[i,'turnovers']
        box_scores.at[i+1,'against_personal_fouls'] = box_scores.at[i,'personal_fouls']
        box_scores.at[i+1,'against_points'] = box_scores.at[i,'points']

        box_scores.at[i, 'game_ID'] = game_ID
        box_scores.at[i+1, 'game_ID'] = game_ID

        # append both games to revised_box_scores data
        entry1 = box_scores.loc[i]
        entry2 = box_scores.loc[i+1]
        revised_box_scores = revised_box_scores.append([entry1, entry2])

        i += 2
        game_ID += 1

    return revised_box_scores

def set_team_values(box_scores):
    
    teams = set()

    # stores all unique team names in teams set
    for row in box_scores.index:
        teams.add(box_scores.at[row, 'team'])

    # initialize dictionary for teams data
    teams_data = {}

    # initialize each value of the dictionary as a dataframe
    for team in teams:
        teams_data[team] = pd.DataFrame()

    # iterate through all rows of box_scores and append that box score to the corresponding team dataframe in the teams_data dictionary
    for row in box_scores.index:
        teams_data[box_scores.at[row, 'team']] = teams_data[box_scores.at[row, 'team']].append(box_scores.loc[row], ignore_index=True)

    return teams_data

def find_averages(teams_data, nGames):

    # initialize dataframe for final data
    final_data = pd.DataFrame()

    # initialize number of games to take averages data from
    last_n_games = 20

    # iterate through all team data
    for team in teams_data:

        # iterate through all games that team played
        row = 0
        while row < nGames:
            
            # create dictionary of team essential value and average values leading up to the current game 
            prediction_vals = {'game_ID': [teams_data[team].at[row, 'game_ID']],
                                'team': team,
                                'game_number': row + 1, 
                                'outcome': [teams_data[team].at[row, 'outcome']],
                                'opponent': [teams_data[team].at[row, 'opponent']],
                                'points': [teams_data[team].at[row, 'points']],
                                'date': [teams_data[team].at[row, 'date']],
                                'avg_points': [sum(teams_data[team].loc[row-last_n_games:row-1, 'points'])/last_n_games],
                                'avg_FG_made': [sum(teams_data[team].loc[row-last_n_games:row-1, 'made_field_goals'])/last_n_games],
                                'avg_FG_attempted': [sum(teams_data[team].loc[row-last_n_games:row-1, 'attempted_field_goals'])/last_n_games],
                                'avg_3pt_made': [sum(teams_data[team].loc[row-last_n_games:row-1, 'made_three_point_field_goals'])/last_n_games],
                                'avg_3pt_attempted': [sum(teams_data[team].loc[row-last_n_games:row-1, 'attempted_three_point_field_goals'])/last_n_games],
                                'avg_FT_made': [sum(teams_data[team].loc[row-last_n_games:row-1, 'made_free_throws'])/last_n_games],
                                'avg_FT_attempted': [sum(teams_data[team].loc[row-last_n_games:row-1, 'attempted_free_throws'])/last_n_games],
                                'avg_ORB': [sum(teams_data[team].loc[row-last_n_games:row-1, 'offensive_rebounds'])/last_n_games],
                                'avg_DRB': [sum(teams_data[team].loc[row-last_n_games:row-1, 'defensive_rebounds'])/last_n_games],
                                'avg_assists': [sum(teams_data[team].loc[row-last_n_games:row-1, 'assists'])/last_n_games],
                                'avg_steals': [sum(teams_data[team].loc[row-last_n_games:row-1, 'steals'])/last_n_games],
                                'avg_blocks': [sum(teams_data[team].loc[row-last_n_games:row-1, 'blocks'])/last_n_games],
                                'avg_turnovers': [sum(teams_data[team].loc[row-last_n_games:row-1, 'turnovers'])/last_n_games],
                                'avg_PF': [sum(teams_data[team].loc[row-last_n_games:row-1, 'personal_fouls'])/last_n_games],
                                'avg_points_against': [sum(teams_data[team].loc[row-last_n_games:row-1, 'against_points'])/last_n_games],
                                'avg_FG_made_against': [sum(teams_data[team].loc[row-last_n_games:row-1, 'against_made_field_goals'])/last_n_games],
                                'avg_FG_attempted_against': [sum(teams_data[team].loc[row-last_n_games:row-1, 'against_attempted_field_goals'])/last_n_games],
                                'avg_3pt_made_against': [sum(teams_data[team].loc[row-last_n_games:row-1, 'against_made_three_point_field_goals'])/last_n_games],
                                'avg_3pt_attempted_against': [sum(teams_data[team].loc[row-last_n_games:row-1, 'against_attempted_three_point_field_goals'])/last_n_games],
                                'avg_FT_made_against': [sum(teams_data[team].loc[row-last_n_games:row-1, 'against_made_free_throws'])/last_n_games],
                                'avg_FT_attempted_against': [sum(teams_data[team].loc[row-last_n_games:row-1, 'against_attempted_free_throws'])/last_n_games],
                                'avg_ORB_against': [sum(teams_data[team].loc[row-last_n_games:row-1, 'against_offensive_rebounds'])/last_n_games],
                                'avg_DRB_against': [sum(teams_data[team].loc[row-last_n_games:row-1, 'against_defensive_rebounds'])/last_n_games],
                                'avg_assists_against': [sum(teams_data[team].loc[row-last_n_games:row-1, 'against_assists'])/last_n_games], 
                                'avg_blocks_against': [sum(teams_data[team].loc[row-last_n_games:row-1, 'against_blocks'])/last_n_games],
                                'avg_PF_against': [sum(teams_data[team].loc[row-last_n_games:row-1, 'against_personal_fouls'])/last_n_games]
                                }

            # append dictionary to final_data
            temp = pd.DataFrame.from_dict(prediction_vals)
            final_data = pd.concat([final_data, temp])
            
            row += 1

    final_data = final_data.reset_index(drop=True)

    return final_data

def find_opp_averages(final_data):   

    # initialize all opponent avg values to -1000.2 to recognize errors in data
    final_data['opp_avg_points'] = -1000.2
    final_data['opp_avg_FG_made'] = -1000.2
    final_data['opp_avg_FG_attempted'] = -1000.2
    final_data['opp_avg_3pt_made'] = -1000.2
    final_data['opp_avg_3pt_attempted'] = -1000.2
    final_data['opp_avg_FT_made'] = -1000.2
    final_data['opp_avg_FT_attempted'] = -1000.2
    final_data['opp_avg_ORB'] = -1000.2
    final_data['opp_avg_DRB'] = -1000.2
    final_data['opp_avg_assists'] = -1000.2
    final_data['opp_avg_steals'] = -1000.2
    final_data['opp_avg_blocks'] = -1000.2
    final_data['opp_avg_turnovers'] = -1000.2
    final_data['opp_avg_PF'] = -1000.2
    final_data['opp_avg_points_against'] = -1000.2
    final_data['opp_avg_FG_made_against'] = -1000.2
    final_data['opp_avg_FG_attempted_against'] = -1000.2
    final_data['opp_avg_3pt_attempted_against'] = -1000.2
    final_data['opp_avg_FT_made_against'] = -1000.2
    final_data['opp_avg_FT_attempted_against'] = -1000.2
    final_data['opp_avg_ORB_against'] = -1000.2
    final_data['opp_avg_DRB_against'] = -1000.2
    final_data['opp_avg_assists_against'] = -1000.2
    final_data['opp_avg_blocks_against'] = -1000.2
    final_data['opp_avg_PF_against'] = -1000.2
    final_data['opponents_points'] = -1000.2

    # iterate through rows of final_data
    for row1 in final_data.index:
        # iterate through rows of final_data to find when game_ID matches row1
        for row2 in final_data.index:
            if final_data.at[row1, 'game_ID'] == final_data.at[row2, 'game_ID']:
                # fill in row1 with their opponents avg values 
                final_data.at[row1,'opp_avg_points'] = final_data.at[row2,'avg_points']
                final_data.at[row1,'opp_avg_FG_made'] = final_data.at[row2,'avg_FG_made']
                final_data.at[row1,'opp_avg_FG_attempted'] = final_data.at[row2,'avg_FG_attempted']
                final_data.at[row1,'opp_avg_3pt_made'] = final_data.at[row2,'avg_3pt_made']
                final_data.at[row1,'opp_avg_3pt_attempted'] = final_data.at[row2,'avg_3pt_attempted']
                final_data.at[row1,'opp_avg_FT_made'] = final_data.at[row2,'avg_FT_made']
                final_data.at[row1,'opp_avg_FT_attempted'] = final_data.at[row2,'avg_FT_attempted']
                final_data.at[row1,'opp_avg_ORB'] = final_data.at[row2,'avg_ORB']
                final_data.at[row1,'opp_avg_DRB'] = final_data.at[row2,'avg_DRB']
                final_data.at[row1,'opp_avg_assists'] = final_data.at[row2,'avg_assists']
                final_data.at[row1,'opp_avg_steals'] = final_data.at[row2,'avg_steals']
                final_data.at[row1,'opp_avg_blocks'] = final_data.at[row2,'avg_blocks']
                final_data.at[row1,'opp_avg_turnovers'] = final_data.at[row2,'avg_turnovers']
                final_data.at[row1,'opp_avg_PF'] = final_data.at[row2,'avg_PF']
                final_data.at[row1,'opp_avg_points_against'] = final_data.at[row2,'avg_points_against']
                final_data.at[row1,'opp_avg_FG_made_against'] = final_data.at[row2,'avg_FG_made_against']
                final_data.at[row1,'opp_avg_FG_attempted_against'] = final_data.at[row2,'avg_FG_attempted_against']
                final_data.at[row1,'opp_avg_3pt_made_against'] = final_data.at[row2,'avg_3pt_made_against']
                final_data.at[row1,'opp_avg_3pt_attempted_against'] = final_data.at[row2,'avg_3pt_attempted_against']
                final_data.at[row1,'opp_avg_FT_made_against'] = final_data.at[row2,'avg_FT_made_against']
                final_data.at[row1,'opp_avg_FT_attempted_against'] = final_data.at[row2,'avg_FT_attempted_against']
                final_data.at[row1,'opp_avg_ORB_against'] = final_data.at[row2,'avg_ORB_against']
                final_data.at[row1,'opp_avg_DRB_against'] = final_data.at[row2,'avg_DRB_against']
                final_data.at[row1,'opp_avg_assists_against'] = final_data.at[row2,'avg_assists_against']
                final_data.at[row1,'opp_avg_blocks_against'] = final_data.at[row2,'avg_blocks_against']
                final_data.at[row1,'opp_avg_PF_against'] = final_data.at[row2,'avg_PF_against']
                final_data.at[row1, 'opponents_points'] = final_data.at[row2, 'points']

    return final_data

def clean_data(final_data):

    # initialize all columns that could be predicted values
    final_data['points_scored'] = 0
    final_data['opponents_points_scored'] = 0
    final_data['team_win'] = 0
    final_data['differential'] = 0

    # drop game_ID
    final_data = final_data.drop_duplicates(subset=['game_ID'])

    # iterate through rows of final_data
    for row in final_data.index:
        # if team hasn't played 20 games yet or a value equals the initialized value then drop the row
        if final_data.at[row, 'opp_avg_assists_against'] == -1000.2 or final_data.at[row, 'game_number'] < 20:
            final_data = final_data.drop(index=row, axis=0)
        # assign values for possible predicted values
        else:
            final_data.at[row, 'points_scored'] = final_data.at[row, 'points']
            final_data.at[row, 'opponents_points_scored'] = final_data.at[row, 'opponents_points']
            final_data.at[row, 'differential'] = final_data.at[row, 'points_scored'] - final_data.at[row, 'opponents_points_scored']
            if final_data.at[row, 'differential'] > 0:
                final_data.at[row, 'team_win'] = 1

    # drop unneccesary columns
    final_data = final_data.drop('points', 1)
    final_data = final_data.drop('opponents_points', 1)
    final_data = final_data.drop('outcome', 1)
    final_data = final_data.drop('game_number', 1)

    return final_data

def reduce_data(final_data):

    # initialize reduced data dataframe
    reduced_data = pd.DataFrame()

    # iterate through rows of final_data
    for row in final_data.index:
        # create dictionary of important stats and differentials between team and opponent averages as well as team against and opponenet against differences
        difference_vals = {'game_ID': [final_data.at[row, 'game_ID']],
                            'team': [final_data.at[row, 'team']],
                            'opponent': [final_data.at[row, 'opponent']],
                            'date': [final_data.at[row, 'date']],
                            'dif_points': [final_data.at[row, 'avg_points'] - final_data.at[row, 'opp_avg_points']],
                            'dif_FG_made': [final_data.at[row, 'avg_FG_made'] - final_data.at[row, 'opp_avg_FG_made']],
                            'dif_FG_attempted': [final_data.at[row, 'avg_FG_attempted'] - final_data.at[row, 'opp_avg_FG_attempted']],
                            'dif_3pt_made': [final_data.at[row, 'avg_3pt_made'] - final_data.at[row, 'opp_avg_3pt_made']],
                            'dif_3pt_attempted': [final_data.at[row, 'avg_3pt_attempted'] - final_data.at[row, 'opp_avg_3pt_attempted']],
                            'dif_FT_made': [final_data.at[row, 'avg_FT_made'] - final_data.at[row, 'opp_avg_FT_made']],
                            'dif_FT_attempted': [final_data.at[row, 'avg_FT_attempted'] - final_data.at[row, 'opp_avg_FT_attempted']],
                            'dif_ORB': [final_data.at[row, 'avg_ORB'] - final_data.at[row, 'opp_avg_ORB']],
                            'dif_DRB': [final_data.at[row, 'avg_DRB'] - final_data.at[row, 'opp_avg_DRB']],
                            'dif_assists': [final_data.at[row, 'avg_assists'] - final_data.at[row, 'opp_avg_assists']],
                            'dif_steals': [final_data.at[row, 'avg_steals'] - final_data.at[row, 'opp_avg_steals']],
                            'dif_blocks': [final_data.at[row, 'avg_blocks'] - final_data.at[row, 'opp_avg_blocks']],
                            'dif_turnovers': [final_data.at[row, 'avg_turnovers'] - final_data.at[row, 'opp_avg_turnovers']],
                            'dif_PF': [final_data.at[row, 'avg_PF'] - final_data.at[row, 'opp_avg_PF']],
                            'dif_points_against': [final_data.at[row, 'avg_points_against'] - final_data.at[row, 'opp_avg_points_against']],
                            'dif_FG_made_against': [final_data.at[row, 'avg_FG_made_against'] - final_data.at[row, 'opp_avg_FG_made_against']],
                            'dif_FG_attempted_against': [final_data.at[row, 'avg_FG_attempted_against'] - final_data.at[row, 'opp_avg_FG_attempted_against']],
                            'dif_3pt_made_against': [final_data.at[row, 'avg_3pt_made_against'] - final_data.at[row, 'opp_avg_3pt_made_against']],
                            'dif_3pt_attempted_against': [final_data.at[row, 'avg_3pt_attempted_against'] - final_data.at[row, 'opp_avg_3pt_attempted_against']],
                            'dif_FT_made_against': [final_data.at[row, 'avg_FT_made_against'] - final_data.at[row, 'opp_avg_FT_made_against']],
                            'dif_FT_attempted_against': [final_data.at[row, 'avg_FT_attempted_against'] - final_data.at[row, 'opp_avg_FT_attempted_against']],
                            'dif_ORB_against': [final_data.at[row, 'avg_ORB_against'] - final_data.at[row, 'opp_avg_ORB_against']],
                            'dif_DRB_against': [final_data.at[row, 'avg_DRB_against'] - final_data.at[row, 'opp_avg_DRB_against']],
                            'dif_assists_against': [final_data.at[row, 'avg_assists_against'] - final_data.at[row, 'opp_avg_assists_against']], 
                            'dif_blocks_against': [final_data.at[row, 'avg_blocks_against'] - final_data.at[row, 'opp_avg_blocks_against']],
                            'dif_PF_against': [final_data.at[row, 'avg_PF_against'] - final_data.at[row, 'opp_avg_PF_against']],
                            'points_scored': [final_data.at[row, 'points_scored']],
                            'opponents_points_scored': [final_data.at[row, 'opponents_points_scored']],
                            'team_win': [final_data.at[row, 'team_win']],
                            'differential': [final_data.at[row, 'differential']]
                            }           

        # add difference_vals dictionary to reduced_data dataframe
        temp = pd.DataFrame.from_dict(difference_vals)
        reduced_data = pd.concat([reduced_data, temp])

    reduced_data = reduced_data.reset_index(drop=True)

    return reduced_data

def main():

    # take inputs for start and end date data
    start_year = int(input('Enter start year: '))
    start_month = int(input('Enter start month: '))
    start_day = int(input('Enter start day: '))
    end_year = int(input('Enter end year: '))
    end_month = int(input('Enter end month: '))
    end_day = int(input('Enter end day: '))

    # account for the COVID years games played being shorter in 2019-2020 and 2020-2021
    if end_year == 2021:
        nGames = 72
    elif end_year == 2020:
        nGames = 60
    else:
        nGames = 82

    # scrape initial data
    box_scores = scrape_data(start_year, start_month, start_day, end_year, end_month, end_day)
    # revise data
    revised_box_scores = revise_box_scores(box_scores)
    # break box scores up by teams
    teams_data = set_team_values(revised_box_scores)
    # find team averages of last 20 games
    final_data = find_averages(teams_data, nGames)
    # find team's opponent averages their last 20 ames
    final_data = find_opp_averages(final_data)
    # clean up final_data
    final_data = clean_data(final_data)
    # create new dataset with fewer columns
    reduced_data = reduce_data(final_data)

    # create path to final and reduced datasets given cwd
    cwd = os.getcwd()
    final_data_path = cwd + '/' + str(end_year) + '_final_data'
    reduced_data_path = cwd + '/' + str(end_year) + '_reduced_data'

    # write final and reduced data to csv's 
    final_data.to_csv(final_data_path, index=False)
    reduced_data.to_csv(reduced_data_path, index=False)

if __name__ == '__main__':
    main()
