import pandas as pd

def get_weathers(weather_str):
    ''' 
    Given a weather string will return the following
    - temperature
    - wind
    - humidity
    '''
    def weather_pieces(weather_parts):
        temp_bit = None
        wind_bit = None
        humid_bit = None

        def to_int(in_str):
            numeric_filter = filter(str.isdigit, in_str)
            return int("".join(numeric_filter))

        for part in weather_parts:
            if 'degrees' in part:
                temp_bit = to_int(part)
            elif 'humidity' in part:
                humid_bit = to_int(part)
            elif 'mph' in part:
                wind_bit = to_int(part)
        return (temp_bit, wind_bit, humid_bit)

    if weather_str is None: return (None, None, None)

    weather_parts = weather_str.split(', ')
    temperature, wind_speed, humidity = weather_pieces(weather_parts)
    return (temperature, wind_speed, humidity)

def get_is_indoors(weather_str):
    ''' 
    Given a weather string will return the following
    - temperature
    - wind
    - humidity
    '''
    def weather_pieces(weather_parts):
        temp_bit = None
        wind_bit = None
        humid_bit = None

        def to_int(in_str):
            numeric_filter = filter(str.isdigit, in_str)
            return int("".join(numeric_filter))

        for part in weather_parts:
            if 'degrees' in part:
                temp_bit = to_int(part)
            elif 'humidity' in part:
                humid_bit = to_int(part)
            elif 'mph' in part:
                wind_bit = to_int(part)
        return (temp_bit, wind_bit, humid_bit)

    if weather_str is None: return (None, None, None)

    weather_parts = weather_str.split(', ')
    temperature, wind_speed, humidity = weather_pieces(weather_parts)
    return (temperature, wind_speed, humidity)

def get_game_filename(game):
    '''
    Given a game df (series) this function will return
    the unique portion of info and stats filenames
    '''
    # year = game['year']
    (y, month, day) = game['date'].split('-')
    team_name = game['team'] if game['home'] == 1 else game['opponent']
    return f"{y}{month}{day}0{TEAM_DICT[team_name]}"

def get_stat_value(stat_df, field):
    '''
    We need to be safe when getting values from the stat
    file. This function will do that
    '''
    if stat_df.index.name != 'stat':
        stat_df = stat_df.set_index('stat')
    try:
        return stat_df.loc[field]['value']
    except:
        return None

def get_game_with_info(game_df, info_df):
    '''
    Given a game_df and info_df
    and source the values out of it returning a new game_df
    which includes these new features
    '''
    game_df = game_df.copy()
    (temperature, wind,
     humidity) = get_weathers(get_stat_value(info_df, STAT_FIELDS['WEATHER']))
    game_df['temperature'] = temperature
    game_df['wind'] = wind
    game_df['humidity'] = humidity

    roof_type = get_stat_value(info_df, STAT_FIELDS['ROOF'])
    game_df['roof'] = roof_type
    game_df['is_outdoors'] = 1 if roof_type == 'outdoors' else 0
    surface_type = get_stat_value(info_df, STAT_FIELDS['SURFACE'])
    game_df['surface'] = surface_type
    game_df['is_grass'] = 1 if surface_type == 'grass' else 0

    return game_df

def get_game_teams(game):
    '''
    given a game will return (home,away)
    '''
    if game['home'] == 1:
        return (game['team'], game['opponent'])
    else:
        return (game['opponent'], game['team'])

def add_stats_to_game(game_df, stats_df, field_prefix, is_home):
    index_key = 'home' if is_home == True else 'away'
    game_df[f'{field_prefix}_first_downs'] = stats_df.loc['First Downs'].loc[
        index_key]
    # will rely on pass yards in the passing stat line
    # game_df[f'{field_prefix}_pass_yards'] = stats_df.loc['Net Pass Yards'].loc[
    #     index_key]
    game_df[f'{field_prefix}_total_yards'] = stats_df.loc['Total Yards'].loc[
        index_key]
    game_df[f'{field_prefix}_turnovers_lost'] = stats_df.loc['Turnovers'].loc[
        index_key]
    game_df[f'{field_prefix}_time_of_possession'] = stats_df.loc[
        'Time of Possession'].loc[index_key]

    # rushing
    (rush_count, rush_yards,
     rush_td) = stats_df.loc['Rush-Yds-TDs'].loc[index_key].split('-')
    game_df[f'{field_prefix}_rush_count'] = rush_count
    game_df[f'{field_prefix}_rush_yards'] = rush_yards
    game_df[f'{field_prefix}_rush_td'] = rush_td

    # passing
    (pass_completions, pass_count, pass_yards, pass_td, interceptions_lost
     ) = stats_df.loc['Cmp-Att-Yd-TD-INT'].loc[index_key].split('-')
    game_df[f'{field_prefix}_pass_completions'] = pass_completions
    game_df[f'{field_prefix}_pass_count'] = pass_count
    game_df[f'{field_prefix}_pass_yards'] = pass_yards
    game_df[f'{field_prefix}_pass_td'] = pass_td
    game_df[f'{field_prefix}_interceptions_lost'] = interceptions_lost

    # sacks
    (sack_count,
     sack_yards) = stats_df.loc['Sacked-Yards'].loc[index_key].split('-')
    game_df[f'{field_prefix}_sack_count'] = sack_count
    game_df[f'{field_prefix}_sack_yards'] = sack_yards

    # fumbles
    (fumble_count,
     fumble_lost) = stats_df.loc['Fumbles-Lost'].loc[index_key].split('-')
    game_df[f'{field_prefix}_fumble_count'] = fumble_count
    game_df[f'{field_prefix}_fumble_lost'] = fumble_lost

    # penalties
    (penalty_count,
     penalty_yards) = stats_df.loc['Penalties-Yards'].loc[index_key].split('-')
    game_df[f'{field_prefix}_penalty_count'] = penalty_count
    game_df[f'{field_prefix}_penalty_yards'] = penalty_yards

    def get_ratio(part, whole):
        try:
            return round(int(part) / int(whole), 2)
        except:
            return 0.0

    # 3rd downs
    (third_down_conversions, third_down_count
     ) = stats_df.loc['Third Down Conv.'].loc[index_key].split('-')
    game_df[f'{field_prefix}_third_down_count'] = third_down_count
    game_df[f'{field_prefix}_third_down_conversions'] = third_down_conversions
    game_df[f'{field_prefix}_third_down_ratio'] = get_ratio(
        third_down_conversions, third_down_count)

    # 4th downs
    (fourth_down_conversions, fourth_down_count
     ) = stats_df.loc['Fourth Down Conv.'].loc[index_key].split('-')
    game_df[f'{field_prefix}_fourth_down_count'] = fourth_down_count
    game_df[
        f'{field_prefix}_fourth_down_conversions'] = fourth_down_conversions
    game_df[f'{field_prefix}_fourth_down_ratio'] = get_ratio(
        fourth_down_conversions, fourth_down_count)

def get_game_with_stats(game_df, stats_df):
    '''
  Given a game_df and stats_df
  and source the values out of it returning a new game_df
  which includes these new features
  '''
    game_copy_df = game_df.copy()
    add_stats_to_game(game_copy_df,
                      stats_df,
                      field_prefix='team',
                      is_home=game_copy_df['home'] == True)
    add_stats_to_game(game_copy_df,
                      stats_df,
                      field_prefix='opponent',
                      is_home=game_copy_df['home'] == False)
    return game_copy_df

def get_team_name(team):
  team_name = team
        
  # if there are no spaces, they sent us a nickname
  if team_name.count(' ') < 1:
    team_name = TEAM_NAME[team_name]
  
  return team_name

def get_nfl_df(data_path = '../../data'):
  return pd.read_csv(f'{data_path}/nfl.csv')

def get_year(df, year):
  return df[df['year'] == year]

def get_year_week(df, year, week):
  return df[(df['year'] == year) & (df['week'] == week)]

def get_team(df, team):
  team_name = get_team_name(team)
  return df[df['team'] == team_name]

STAT_FIELDS = {
    'TOSS': 'Won Toss',
    'ROOF': 'Roof',
    'SURFACE': 'Surface',
    'DURATION': 'Duration',
    'ATTENDANCE': 'Attendance',
    'LINE': 'Vegas Line',
    'OVUN': 'Over/Under',
    'WEATHER': 'Weather'
}
TEAM_DICT = {
    'Arizona Cardinals': 'crd',
    # 'Arizona Cardinals': 'ari',
    'Atlanta Falcons': 'atl',
    'Baltimore Ravens': 'rav',
    # 'Baltimore Ravens': 'bal',
    'Buffalo Bills': 'buf',
    'Carolina Panthers': 'car',
    'Chicago Bears': 'chi',
    'Cincinnati Bengals': 'cin',
    'Cleveland Browns': 'cle',
    'Dallas Cowboys': 'dal',
    'Denver Broncos': 'den',
    'Detroit Lions': 'det',
    'Green Bay Packers': 'gnb',
    'Houston Texans': 'htx',
    # 'Houston Texans': 'hou',
    'Indianapolis Colts': 'clt',
    # 'Indianapolis Colts': 'ind',
    'Jacksonville Jaguars': 'jax',
    'Kansas City Chiefs': 'kan',
    'Las Vegas Raiders': 'rai',
    'Los Angeles Chargers': 'sdg',
    'Los Angeles Rams': 'ram',
    # 'Los Angeles Rams': 'lar',
    'Miami Dolphins': 'mia',
    'Minnesota Vikings': 'min',
    'New England Patriots': 'nwe',
    'New Orleans Saints': 'nor',
    'New York Giants': 'nyg',
    'New York Jets': 'nyj',
    'Oakland Raiders': 'rai',
    # 'Oakland Raiders': 'oak',
    'Philadelphia Eagles': 'phi',
    'Pittsburgh Steelers': 'pit',
    'San Diego Chargers': 'sdg',
    'San Francisco 49ers': 'sfo',
    'Seattle Seahawks': 'sea',
    'St. Louis Rams': 'ram',
    'St. Louis Cardinals': 'crd',
    'Tampa Bay Buccaneers': 'tam',
    'Tennessee Titans': 'oti',
    # 'Tennessee Titans': 'ten',
    'Washington Football Team': 'was',
    'Washington Redskins': 'was'
}
TEAM_NAME = {
    'Cardinals': 'Arizona Cardinals',
    'Falcons': 'Atlanta Falcons',
    'Ravens': 'Baltimore Ravens',
    'Bills': 'Buffalo Bills',
    'Panthers': 'Carolina Panthers',
    'Bears': 'Chicago Bears',
    'Bengals': 'Cincinnati Bengals',
    'Browns': 'Cleveland Browns',
    'Cowboys': 'Dallas Cowboys',
    'Broncos': 'Denver Broncos',
    'Lions': 'Detroit Lions',
    'Packers': 'Green Bay Packers',
    'Texans': 'Houston Texans',
    'Colts': 'Indianapolis Colts',
    'Jaguars': 'Jacksonville Jaguars',
    'Chiefs': 'Kansas City Chiefs',
    'Raiders': 'Las Vegas Raiders',
    'Chargers': 'Los Angeles Chargers',
    'Rams': 'Los Angeles Rams',
    'Dolphins': 'Miami Dolphins',
    'Vikings': 'Minnesota Vikings',
    'Patriots': 'New England Patriots',
    'Saints': 'New Orleans Saints',
    'Giants': 'New York Giants',
    'Jets': 'New York Jets',
    'Raiders': 'Oakland Raiders',
    'Eagles': 'Philadelphia Eagles',
    'Steelers': 'Pittsburgh Steelers',
    'SDChargers': 'San Diego Chargers',
    '49ers': 'San Francisco 49ers',
    'Seahawks': 'Seattle Seahawks',
    'StlRams': 'St. Louis Rams',
    'Rams': 'Los Angeles Rams',
    'Cardinals': 'St. Louis Cardinals',
    'Buccaneers': 'Tampa Bay Buccaneers',
    'Titans': 'Tennessee Titans',
    'Team': 'Washington Football Team',
    'Redskins': 'Washington Redskins',
    'Washington': 'Washington Redskins'
}



class NFL_Data:
  data_path = '../../data'
  nfl_df = None
    
  def __init__(self, data_path = '../../data'):
    self.data_path = data_path
    self.nfl_df = get_nfl_df(data_path)

  def data(self):
    return self.nfl_df
  
  def data_by_team(self):
    return self.nfl_df
  
  def data_by_game(self):
    return self.nfl_df[self.nfl_df['home'] == 1]
    
  def year(self, year):
    return get_year(self.nfl_df, year)
    
  def team(self, team):
    return get_team(self.nfl_df, team)

  def team_year(self, team, year):
    return get_team(self.year(year), team)
