# CONFIG
START_YEAR = 2010
END_YEAR = 2020
DATA_PATH = '../data/games'
_is_dev_mode = False

import numpy as np
import pandas as pd
from dateutil import parser


def get_tables_for(year, week):
    return pd.read_html(
        f'https://www.pro-football-reference.com/years/{year}/week_{week}.htm')


def get_games_list(table_list, year, week):
    games_list = []
    i = 0
    for table_df in table_list:
        '''
    WORK GAME TABLES
    we expect 3 rows where the first row is the
    date of the game and the 3rd column having
    "Final" and NaN
    '''
        if len(table_df.index) == 3:
            if (table_df[2][1] == "Final") & (table_df[2][2] is np.nan):
                i += 1
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
                }
                games_list.append(home_data)
                games_list.append(away_data)

                # print(f'[{i}]------')
                # print(df)

    return games_list


def get_games_df_for_year_week(year, week):
    return pd.DataFrame(get_games_list(get_tables_for(year, week), year, week))


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


def main():
    print(f"Starting to process {START_YEAR}-{END_YEAR}...")
    print(f"  data will be written to {DATA_PATH}/")

    all_games_df_list = []
    for year in range(START_YEAR, END_YEAR + 1):
        year_df = get_games_df_for_year(year)
        year_df.to_csv(f'{DATA_PATH}/games_{year}.csv', index=False)
        all_games_df_list.append(year_df)
        print(f"  completed {year}...")

    all_games_df = pd.concat(all_games_df_list, ignore_index=True)
    all_games_df.to_csv(f'{DATA_PATH}/all_games.csv', index=False)
    print("Done.")


def _dev_main():
    year = 2020
    week = 1
    lst = get_games_list(get_tables_for(year, week), year, week)
    print(lst)


# do the work
if _is_dev_mode:
    _dev_main()
else:
    main()
