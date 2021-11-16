import numpy as np
import pandas as pd
from dateutil import parser
import glob


def get_tables_for(year, week):
    return pd.read_html(
        f'https://www.pro-football-reference.com/years/{year}/week_{week}.htm')


def get_games_list(year, week):

    table_list = get_tables_for(year, week)
    games_list = []
    i = 0
    for table_df in table_list:
        '''
    WORK GAME TABLES
    we expect 3 rows where the first row is the
    date of the game and the 3rd column having
    "Final" and NaN or OT
    '''
        if len(table_df.index) == 3:
            last_top_value = table_df[2][1]
            last_bottom_value = table_df[2][2]
            if (last_top_value == "Final") & (last_bottom_value is np.nan
                                              or last_bottom_value == 'OT'):
                i += 1
                was_overtime = 1 if last_bottom_value == 'OT' else 0
                # selecting only teams and scores from table
                df = table_df.iloc[0:3, 0:2]
                df.columns = ['team', 'score']
                df.index = ['date', 'away', 'home']
                df['score']['date'] = 0
                df['score'] = df['score'].astype('int64')
                game_date_str = df['team']['date']
                game_dt = parser.parse(game_date_str)
                game_date_ymd = game_dt.strftime("%Y-%m-%d")
                score_away = df['score']['away']
                score_home = df['score']['home']
                was_home_win = score_home > score_away
                # add home data
                home_data = {
                    'date': game_date_ymd,
                    'year': year,
                    'week': week,
                    'team': df['team']['home'],
                    'team_score': df['score']['home'],
                    'opponent': df['team']['away'],
                    'opponent_score': df['score']['away'],
                    'win': 1 if was_home_win == True else 0,
                    'home': 1,
                    'overtime': was_overtime,
                }
                away_data = {
                    'date': game_date_ymd,
                    'year': year,
                    'week': week,
                    'team': df['team']['away'],
                    'team_score': df['score']['away'],
                    'opponent': df['team']['home'],
                    'opponent_score': df['score']['home'],
                    'win': 0 if was_home_win == True else 1,
                    'home': 0,
                    'overtime': was_overtime,
                }
                games_list.append(home_data)
                games_list.append(away_data)

                # print(f'[{i}]------')
                # print(df)

    return games_list


def get_games_df_for_year_week(year, week):
    return pd.DataFrame(get_games_list(year, week))


def get_games_df_for_year(year):
    games_df_list = []
    max_week = 17
    if year <= 1989:
        max_week = 16
    elif year == 1993:
        max_week = 18
    elif year >= 2021:
        max_week = 18

    for week in range(1, max_week + 1):
        games_df_list.append(get_games_df_for_year_week(year, week))

    year_games_df = pd.concat(games_df_list)
    return year_games_df


def fetch_and_write_year(year, data_path='../../data'):
    year_df = get_games_df_for_year(year)
    year_df.to_csv(f'{data_path}/games/games_{year}.csv', index=False)


def build_all_game_files(data_path='../../data'):
    # gather all file paths
    file_paths = glob.glob(f"{data_path}/games/games_*.csv")
    file_paths.sort()
    file_paths

    all_games_df_list = []
    for file_path in file_paths:
        year_df = pd.read_csv(file_path)
        all_games_df_list.append(year_df)

    all_games_df = pd.concat(all_games_df_list, ignore_index=True)

    #* CLEAN-UPS
    ## year-week
    all_games_df['year_week'] = all_games_df['year'].map(
        str) + '-' + all_games_df['week'].map(str)
    ## team and opponent win
    all_games_df['team_win'] = all_games_df['win']
    all_games_df['opponent_win'] = all_games_df['team_win'].map({1: 0, 0: 1})

    all_games_df.to_csv(f'{data_path}/games/all_games.csv', index=False)
