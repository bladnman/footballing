import requests
import sys
import pandas as pd
from os.path import exists

sys.path.insert(0, '..')
import utils.game_utils as gu

def fetch_all_info_and_stats(data_path='../../data'):
    '''
    Main call to fetch everything. This will create
    all of the `stat` and `info` files.
    '''
    
    print('Pulling any new data files')
    urls = get_all_box_score_urls(data_path)
    for url in urls:
        work_file(url)
        
    ### CREATES `all_games_with_data.csv` by appending all DATA with all_games.csv
    print('Combining all data files into game data (takes a while)')
    create_all_games_with_data(data_path)
    
    print("Done adding data to all games.")

def get_body_for_url(url):
    try:
        r = requests.get(url)
        body = r.text
        return body
    except:
        print('An exception occurred', url, sys.exc_info()[0])
    return None

def get_stripped_body(url):
    body = get_body_for_url(url)
    if body is not None:
        body = body.replace('<!--', '')
        body = body.replace('-->', '')
        return body
    return None

def save_string_to_file(file_path, str):
    text_file = open(file_path, "w")
    text_file.write(str)
    text_file.close()

def get_game_info_df(tables_df):
    df = None
    for _df in tables_df:
        text = _df.iat[0, 0]
        if type(text) is str:
            if text == "Game Info":
                df = _df.drop(0)
                df.columns = ['stat', 'value']

    return df

def get_game_stats_df(tables_df):
    df = None
    for _df in tables_df:
        text = _df.iat[0, 0]
        if type(text) is str:
            if text == "First Downs":
                df = _df
                df.columns = ['stat', 'away', 'home']

    return df

def work_file(url, data_path='../../data'):
    url_parts = url.split('/')
    file_name = url_parts[-1].split('.')[0]
    info_file_path = f'{data_path}/game_info/game_info_{file_name}.csv'
    stats_file_path = f'{data_path}/game_stats/game_stats_{file_name}.csv'

    ## ONLY WORK NEW ITEMS
    does_info_exist = exists(info_file_path)
    does_stats_exist = exists(stats_file_path)
    if does_info_exist and does_stats_exist:
        return

    ## FETCH THE DATA
    body = get_stripped_body(url)
    df = pd.read_html(body)

    ## PARSE THE RESPONSES
    game_info_df = get_game_info_df(df)
    game_stats_df = get_game_stats_df(df)

    ## WRITE THE RESULTS
    if game_info_df is not None:
        game_info_df.to_csv(info_file_path, index=False)
    if game_stats_df is not None:
        game_stats_df.to_csv(stats_file_path, index=False)

def get_box_score_url(game_ser):
    dt = game_ser['date'].replace('-', '')
    home_team = game_ser['team'] if game_ser['home'] == 1 else game_ser[
        'opponent']
    tm = gu.TEAM_DICT[home_team]
    return f"https://www.pro-football-reference.com/boxscores/{dt}0{tm}.htm"

def get_all_box_score_urls(data_path='../../data'):
    '''
    Returns an array of string of all 
    *box score urls* for all games found 
    in the `all_games.csv` file
    '''
    file_path = f'{data_path}/games/all_games.csv'
    df = pd.read_csv(file_path)
    win_df = df[df['win'] == 1]
    urls = []
    for i in range(len(win_df.index)):
        urls.append(get_box_score_url(win_df.iloc[i]))

    url_df = pd.DataFrame(urls)
    url_df.columns = ['url']
    ## return as a array of strings please
    return url_df['url'].values

def get_stat_df_for_game(game_df, data_path='../../data'):
    '''
    Given a `game_df` this method will return the `stats_df`
    by reading in and preparing the correct file.
  
    This is generally a utility for the engineering step.
    The point is to eventually get the data this method returns
    onto the complete game dataset. Look there for this data first.
    '''
    filename = gu.get_game_filename(game_df)
    stats_df = pd.read_csv(f'{data_path}/game_stats/game_stats_{filename}.csv')
    home_team, away_team = gu.get_game_teams(game_df)
    stats_df.columns = ['', away_team, home_team]
    stats_df = stats_df.set_index('')
    stats_df.columns = ['away', 'home']
    return stats_df

def get_info_df_for_game(game_df, data_path='../../data'):
    '''
    Given a `game_df` this method will return the `info_df`
    by reading in and preparing the correct file.
      
    This is generally a utility for the engineering step.
    The point is to eventually get the data this method returns
    onto the complete game dataset. Look there for this data first.
    '''
    filename = gu.get_game_filename(game_df)
    return pd.read_csv(f'{data_path}/game_info/game_info_{filename}.csv')

def create_all_games_with_data(data_path='../../data'):
    df = pd.read_csv(f'{data_path}/games/all_games.csv')
    # df = pd.read_csv(f'{data_path}/games/games_2021.csv')
    games_with_data = []

    ''' 
    this takes so long it would be nice to see some
    form of progress print out. But since there are 1000s
    of files, we want to print out ever n%
    '''

    last_perc_string = None
    try:
        total_count = len(df.index)
        for i in range(0, total_count):
            game_df = df.iloc[i]

            ## ADD INFO
            try:
                info_df = get_info_df_for_game(game_df)
                game_df = gu.get_game_with_info(game_df, info_df)
            except Exception as e:
                filename = gu.get_game_filename(game_df)
                print('INFO FILE ERROR')
                print(filename)
                print(info_df)
                print(e)
                raise Exception("INFO ERROR. CANCELING")

            ## ADD STATS
            try:
                stats_df = get_stat_df_for_game(game_df)
                game_df = gu.get_game_with_stats(game_df, stats_df)
            except Exception as e:
                filename = gu.get_game_filename(game_df)
                print('STATS FILE ERROR')
                print(filename)
                print(stats_df)
                print(e)
                raise Exception("STATS ERROR. CANCELING")

            games_with_data.append(game_df)
            
            perc_str = f'{(i / total_count)* 100:.0f} %'
            if perc_str != last_perc_string:
              last_perc_string = perc_str
              print(perc_str)

        games_with_data_df = pd.DataFrame(games_with_data)
        games_with_data_df.to_csv(f'{data_path}/games/all_games_with_data.csv',
                                  index=False)
    except Exception as e:
        print(e)
        print('Failed.')
