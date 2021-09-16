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


def get_game_with_info(game, info_df):
    '''
    Given a game (df) we will read the appropriate info file
    and source the values out of it returning a new game (df)
    which includes these new features
    '''
    game = game.copy()
    (temperature, wind,
     humidity) = get_weathers(get_stat_value(info_df, STAT_FIELDS['WEATHER']))
    game['temperature'] = temperature
    game['wind'] = wind
    game['humidity'] = humidity

    game['roof'] = get_stat_value(info_df, STAT_FIELDS['ROOF'])
    game['surface'] = get_stat_value(info_df, STAT_FIELDS['SURFACE'])

    return game


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
