import pandas as pd
import utils.env_utils as env_utils


class DataBoss:

    ## INTERNAL VALUES
    __data_path = None
    __all_df = None
    __teams_df = None
    __games_df = None

    def __init__(self, data_path=None, data_file="nfl.csv"):
        if data_path == None:
            self.__data_path = env_utils.get_data_path()
        else:
            self.__data_path = data_path
        self.__setup(data_file)

    def __setup(self, data_file):
        self.__all_df = pd.read_csv(f"{self.__data_path}/{data_file}")
        self.__teams_df = self.__all_df
        self.__games_df = self.__all_df[self.__all_df['home'] == 1]

    def __mode_df(self, mode='games'):
        if mode == 'games':
            return self.__games_df
        else:
            return self.__teams_df

    ### DATA GETTERS

    ## ## ## ## ## ## ## ## ## ## ## ## ## ##
    ## GETTERS / SETTERS
    def year(self, year, mode='games'):
        df = self.__mode_df(mode)
        return df[df['year'] == year]

    def year_week(self, year, week, mode='games'):
        df = self.__mode_df(mode)
        return df[((df['year'] == year) & (df['week'] == week))]

    def year_team(self, year, team, mode='games'):
        df = self.__mode_df(mode)
        return df[((df['year'] == year) & (df['team'] == team))]

    def team(self, team, mode='games'):
        df = self.__mode_df(mode)
        return df[df['team'] == team]

    def __get_data_path(self):
        return self.__data_path

    def __get_games_df(self):
        return self.__games_df

    def __get_teams_df(self):
        return self.__teams_df

    data_path = property(__get_data_path)
    games_df = property(__get_games_df)
    """Game Rows -> 1 row per game"""
    teams_df = property(__get_games_df)
    """Team Rows -> 2 rows per game"""
