import pandas as pd
import numpy as np
import glob
import re

def get_previous_record(year, week, team, all_games_df):
    records = all_games_df[(all_games_df['year'] == year)
                           & (all_games_df['week'] < week) &
                           (all_games_df['team'] == team)]
    if len(records) < 1:
        return None

    return records[-1:]

def get_all_previous_records(year, week, team, all_games_df):
    records = all_games_df[(all_games_df['year'] == year)
                           & (all_games_df['week'] < week) &
                           (all_games_df['team'] == team)]
    if len(records) < 1:
        return None

    return records
  
def data_from_previous_records(year, week, team, all_games_df, include_last_record=False):
  records = get_all_previous_records(year, week, team, all_games_df)
    
  count = 0
  rush_off_total = 0
  rush_off_mean = 0
  rush_off_std = 0
  rush_def_total = 0
  rush_def_mean = 0
  rush_def_std = 0
  pass_off_total = 0
  pass_off_mean = 0
  pass_off_std = 0
  pass_def_total = 0
  pass_def_mean = 0
  pass_def_std = 0
  last_record = None
  
  if records is not None:
    count = len(records)
    
    rush_off_total = np.sum(records['team_rush_yards'])
    rush_off_mean = np.mean(records['team_rush_yards'])
    rush_off_std = np.std(records['team_rush_yards'])
    
    rush_def_total = np.sum(records['opponent_rush_yards'])
    rush_def_mean = np.mean(records['opponent_rush_yards'])
    rush_def_std = np.std(records['opponent_rush_yards'])
    
    pass_off_total = np.sum(records['team_pass_yards'])
    pass_off_mean = np.mean(records['team_pass_yards'])
    pass_off_std = np.std(records['team_pass_yards'])
    
    pass_def_total = np.sum(records['opponent_pass_yards'])
    pass_def_mean = np.mean(records['opponent_pass_yards'])
    pass_def_std = np.std(records['opponent_pass_yards'])
    
    # we may not want the last record returned all the time
    if include_last_record == True:
      last_record = records[-1:]    
  
  return {
    'count': count,
    'rush_off_total': rush_off_total,
    'rush_off_mean': rush_off_mean,
    'rush_off_std': rush_off_std,
    'rush_def_total': rush_def_total,
    'rush_def_mean': rush_def_mean,
    'rush_def_std': rush_def_std,
    'pass_off_total': pass_off_total,
    'pass_off_mean': pass_off_mean,
    'pass_off_std': pass_off_std,
    'pass_def_total': pass_def_total,
    'pass_def_mean': pass_def_mean,
    'pass_def_std': pass_def_std,
    'last_record': last_record,
  }
  
def get_team_df(team, year, all_df):
    return all_df[(all_df['team'] == team) & (all_df['year'] == year)]

def get_year_df(year, all_df):
    return all_df[all_df['year'] == year]

def get_year_up_to_week_df(year, week, all_df):
    return all_df[(all_df['year'] == year) & (all_df['week'] <= week)]

def get_new_field_roots():
  return [
    'tie',                    'loss',
    'wins_before',            'losses_before',            'ties_before',
    'record_total_before',    'record_normal_before',
    'opp_strength_before',    'opp_trn_before',
    
    'wins_after',             'losses_after',             'ties_after', 
    'record_total_after',     'record_normal_after',  
    'opp_strength_after',     'opp_trn_after',

    # week performance values (week is always after)
    'week_rush_off_perf',        'week_rush_def_perf',        'week_rush_comp_perf',
    'week_pass_off_perf',        'week_pass_def_perf',        'week_pass_comp_perf',
    'week_comb_off_perf',        'week_comb_def_perf',        'week_comb_comp_perf',
        
    # cumulative performance values
    'cml_rush_off_perf_before',    'cml_rush_def_perf_before',    'cml_rush_comp_perf_before',
    'cml_pass_off_perf_before',    'cml_pass_def_perf_before',    'cml_pass_comp_perf_before',
    'cml_comb_off_perf_before',    'cml_comb_def_perf_before',    'cml_comb_comp_perf_before',
    
    'cml_rush_off_perf_after',    'cml_rush_def_perf_after',    'cml_rush_comp_perf_after',
    'cml_pass_off_perf_after',    'cml_pass_def_perf_after',    'cml_pass_comp_perf_after',
    'cml_comb_off_perf_after',    'cml_comb_def_perf_after',    'cml_comb_comp_perf_after',
        
    'points_cml_before',         'points_cml_after',
    'rush_yards_cml_before',     'pass_yards_cml_before',      'total_yards_cml_before',
    'rush_yards_cml_after',      'pass_yards_cml_after',       'total_yards_cml_after',
    
    'opp_trn',
    ]

def get_both_fields_list(field_roots):
  final_fields = []
  for root in field_roots:
    final_fields.append(f'team_{root}')
    final_fields.append(f'opponent_{root}')
  return final_fields
  
def get_df_with_new_columns(all_games_df):
  ## ADD NEW COLUMNS TO ALL GAMES AND CREATE NEW ALL_GAMES_PLUS_DF (agp_df)
  new_field_list = get_both_fields_list(get_new_field_roots())
  new_col_df = pd.DataFrame(columns=new_field_list)
  agp_df = all_games_df.join(new_col_df, how="outer")
  return agp_df
  
## MAIN WORKER
# def update_df_with_aggregates(game_df, all_games_df, side='team'):
def update_df_with_aggregates(index, all_games_df, side='team'):
    SIDE = side # can be opponent
    OTHER_SIDE = 'opponent' if SIDE == 'team' else 'team'
    WEEK_1_TRN = 0.5
    
    game_df = all_games_df.iloc[index]
    
    year = int(game_df['year'])
    week = int(game_df['week'])
    team = game_df[SIDE]
    opp_team = game_df[OTHER_SIDE]

    previous_df = get_previous_record(year, week, team, all_games_df)
    this_prev = data_from_previous_records(year, week, team, all_games_df, include_last_record=False)
    opp_prev_data = data_from_previous_records(year, week, opp_team, all_games_df, include_last_record=True)
    opp_previous_df = opp_prev_data['last_record']

    wins_before = 0
    losses_before = 0
    ties_before = 0

    wins_after = 0
    losses_after = 0
    ties_after = 0
    
    ## Accumulate some stat data for every record
    points_cml_before = 0
    rush_yards_cml_before = 0
    pass_yards_cml_before = 0
    total_yards_cml_before = 0
    points_cml_after = 0
    rush_yards_cml_after = 0
    pass_yards_cml_after = 0
    total_yards_cml_after = 0

    record_total_before = 0
    record_total_after = 0
    record_normal_before = 0
    record_normal_after = 0
    opp_strength_before = 0
    opp_strength_after = WEEK_1_TRN  # first week everyone is a 50/50 team
    # accumulated normalized records of all opponents
    opp_trn_before = 0
    opp_trn_after = 1.0
    opp_trn = WEEK_1_TRN

    '''
    ##  TEAM PERFORMANCE NUMBERS
        PERFOMANCE AGAINST STANDARD
        The numbers show how the team performed against the mean of the 
        opponent. These are not evaluative. They do not describe the
        "strength" of a team of performance -- only how this data
        compares to the "norm" or average at that time of the opponent.
        
        Recall that performance numbers are +/- STD numbers. This means
        they will mostly be found around +/- 0 but to describe outliers
        they can be +/- anywhere. These are not the same as the NORMAL
        values we calculate which all reside between 0 and 1
    '''
    week_rush_off_perf = 0
    week_rush_def_perf = 0
    week_rush_comp_perf = 0   # comp = composite: offense & defense
    
    week_pass_off_perf = 0
    week_pass_def_perf = 0
    week_pass_comp_perf = 0   # comp = composite: offense & defense
    
    week_comb_off_perf = 0
    week_comb_def_perf = 0
    week_comb_comp_perf = 0   # comp = composite: offense & defense
        
    cml_rush_off_perf_before = 0
    cml_rush_def_perf_before = 0
    cml_rush_comp_perf_before = 0
    
    cml_pass_off_perf_before = 0
    cml_pass_def_perf_before = 0
    cml_pass_comp_perf_before = 0
    
    cml_comb_off_perf_before = 0
    cml_comb_def_perf_before = 0
    cml_comb_comp_perf_before = 0
    
    cml_rush_off_perf_after = 0
    cml_rush_def_perf_after = 0
    cml_rush_comp_perf_after = 0
    
    cml_pass_off_perf_after = 0
    cml_pass_def_perf_after = 0
    cml_pass_comp_perf_after = 0
    
    cml_comb_off_perf_after = 0
    cml_comb_def_perf_after = 0
    cml_comb_comp_perf_after = 0
        
        
        
    ## INFO FROM THIS GAME
    win = bool(game_df[f'{SIDE}_win'])
    tie = game_df['team_score'] == game_df['opponent_score'] # no need for SIDE, just see if both scores are the same
    loss = win == False and tie == False
    
    def get_val_or(df, field):
      try:
        val = df.iloc[0][field]
        if np.isnan(val):
            return 0
        return val
      except:
        print('[get_val_or] EXCEPTION ----------------')
        print(f'{team} - team')
        print(f'{week} - week')
        print(f'{year} - year')
        print(f'{field} - field')
        # print(df.iloc[0])
        print(df)
        raise Exception('get_val_or failed')
    def get_normalized(x, min, max):
        return (x-min) / (max-min)
    def get_relative_to_std(val, mean, std, min_val=0, max_val=0):
        MAX = 3.0
        MIN = -3.0
        if std == 0:
          return 0.0
        real_res = (val - mean) / std
        ''' 
        to prevent very large differences found in the early week -- 
        when there are very few data points -- we want to clamp values
        to within a "reasonable" range
        '''
        if min_val < max_val:
          return max(min(real_res, max_val), min_val)
          
        return real_res
        
    def get_opp_trn_after(opp_previous_df, record_normal_after):
        if opp_previous_df is None:
            return 1.0

        pre_opprec_after = get_val_or(opp_previous_df, f'{SIDE}_opp_trn_after')
        pre_trn_after = get_val_or(opp_previous_df, f'{SIDE}_record_normal_after')

        new_opprec = (pre_opprec_after + pre_trn_after) / 2
        final_new_opprec = (new_opprec + record_normal_after) / 2

        return final_new_opprec
    def get_opp_strength_after(opp_previous_df, opp_strength_before):
        '''
        Opponent Strength is essentially the TRN value
        (record_normal) or the wins/losses of a team.
        We want to accumulate the opp_strength from week to
        week to see how strong all opponents have been.
        '''
        if opp_previous_df is None:
            return 1.0

        opp_prev_trn = get_val_or(opp_previous_df, f'{SIDE}_record_normal_after')
        # normalized (/2)
        return (opp_strength_before + opp_prev_trn) / 2
    def add_to_avg(prev_avg, prev_count, new_value):
        ar = [prev_avg] * prev_count
        ar.append(new_value)
        return np.mean(ar)

    ## DATA FROM PREVIOUS GAME
    if previous_df is not None:
        wins_before = get_val_or(previous_df, f'{SIDE}_wins_after')
        losses_before = get_val_or(previous_df, f'{SIDE}_losses_after')
        ties_before = get_val_or(previous_df, f'{SIDE}_ties_after')
        record_total_before = get_val_or(previous_df, f'{SIDE}_record_total_after')
        record_normal_before = get_val_or(previous_df, f'{SIDE}_record_normal_after')
        opp_trn_before = get_val_or(previous_df, f'{SIDE}_opp_trn_after')
        opp_strength_before = get_val_or(previous_df, f'{SIDE}_opp_strength_after')

        points_cml_before = get_val_or(previous_df, f'{SIDE}_points_cml_after')
        rush_yards_cml_before = get_val_or(previous_df, f'{SIDE}_rush_yards_cml_after')
        pass_yards_cml_before = get_val_or(previous_df, f'{SIDE}_pass_yards_cml_after')
        total_yards_cml_before = get_val_or(previous_df, f'{SIDE}_total_yards_cml_after')
        
        points_cml_after = points_cml_before
        rush_yards_cml_after = rush_yards_cml_before
        pass_yards_cml_after = pass_yards_cml_before
        total_yards_cml_after = total_yards_cml_before

        wins_after = wins_before
        losses_after = losses_before
        ties_after = ties_before
        record_total_after = record_total_before
        record_normal_after = record_normal_before


    # must perform this work before the performance calculations
    if opp_previous_df is not None:
        opp_trn_after = get_opp_trn_after(opp_previous_df, record_normal_after)
        opp_strength_after = get_opp_strength_after(opp_previous_df, opp_strength_before)
        opp_trn = get_val_or(opp_previous_df, f'{SIDE}_record_normal_after')
            
        # bounce previous performance values to before
        cml_rush_off_perf_before = get_val_or(opp_previous_df, f'{SIDE}_cml_rush_off_perf_before')
        cml_rush_def_perf_before = get_val_or(opp_previous_df, f'{SIDE}_cml_rush_def_perf_before')
        cml_rush_comp_perf_before = get_val_or(opp_previous_df, f'{SIDE}_cml_rush_comp_perf_before')
            
        cml_pass_off_perf_before = get_val_or(opp_previous_df, f'{SIDE}_cml_pass_off_perf_before')
        cml_pass_def_perf_before = get_val_or(opp_previous_df, f'{SIDE}_cml_pass_def_perf_before')
        cml_pass_comp_perf_before = get_val_or(opp_previous_df, f'{SIDE}_cml_pass_comp_perf_before')
            
        cml_comb_off_perf_before = get_val_or(opp_previous_df, f'{SIDE}_cml_comb_off_perf_before')
        cml_comb_def_perf_before = get_val_or(opp_previous_df, f'{SIDE}_cml_comb_def_perf_before')
        cml_comb_comp_perf_before = get_val_or(opp_previous_df, f'{SIDE}_cml_comb_comp_perf_before')
            
            
    MIN_PERF = -3.0
    MAX_PERF = 3.0
    if opp_prev_data is not None:
        week_rush_off_perf = get_relative_to_std(game_df[f'{SIDE}_rush_yards'], 
                                            opp_prev_data['rush_def_mean'], 
                                            opp_prev_data['rush_def_std'],
                                            min_val=MIN_PERF, max_val=MAX_PERF)
        week_rush_def_perf = -1 * get_relative_to_std(game_df[f'{OTHER_SIDE}_rush_yards'], 
                                            this_prev['rush_def_mean'], 
                                            this_prev['rush_def_std'],
                                            min_val=MIN_PERF, max_val=MAX_PERF)
        week_rush_comp_perf = (week_rush_off_perf + week_rush_def_perf) / 2

        week_pass_off_perf = get_relative_to_std(game_df[f'{SIDE}_pass_yards'], 
                                            opp_prev_data['pass_def_mean'], 
                                            opp_prev_data['pass_def_std'],
                                            min_val=MIN_PERF, max_val=MAX_PERF)
        week_pass_def_perf = -1 * get_relative_to_std(game_df[f'{OTHER_SIDE}_pass_yards'], 
                                            this_prev['pass_def_mean'], 
                                            this_prev['pass_def_std'],
                                            min_val=MIN_PERF, max_val=MAX_PERF)            
        week_pass_comp_perf = (week_pass_off_perf + week_pass_def_perf) / 2

        week_comb_off_perf = (week_rush_off_perf + week_pass_off_perf) / 2
        week_comb_def_perf = (week_rush_def_perf + week_pass_def_perf) / 2    
        week_comb_comp_perf = (week_comb_off_perf + week_comb_def_perf) / 2
        
        cml_rush_off_perf_after = add_to_avg(cml_rush_off_perf_before, week - 1, week_rush_off_perf)
        cml_rush_def_perf_after = add_to_avg(cml_rush_def_perf_before, week - 1, week_rush_def_perf)
        cml_rush_comp_perf_after = add_to_avg(cml_rush_comp_perf_before, week - 1, week_rush_comp_perf)
                
        cml_pass_off_perf_after = add_to_avg(cml_pass_off_perf_before, week - 1, week_pass_off_perf)
        cml_pass_def_perf_after = add_to_avg(cml_pass_def_perf_before, week - 1, week_pass_def_perf)
        cml_pass_comp_perf_after = add_to_avg(cml_pass_comp_perf_before, week - 1, week_pass_comp_perf)
                
        cml_comb_off_perf_after = add_to_avg(cml_comb_off_perf_before, week - 1, week_comb_off_perf)
        cml_comb_def_perf_after = add_to_avg(cml_comb_def_perf_before, week - 1, week_comb_def_perf)
        cml_comb_comp_perf_after = add_to_avg(cml_comb_comp_perf_before, week - 1, week_comb_comp_perf)
        

    ## CALCULATE NEW DATA (after)
    if win:
        wins_after += 1
    if tie:
        ties_after += 1
    if loss:
        losses_after += 1
        
    ## CALCULATE CUMULATIVE DATA
    points_cml_after += game_df[f'{SIDE}_score']
    rush_yards_cml_after += game_df[f'{SIDE}_rush_yards']
    pass_yards_cml_after += game_df[f'{SIDE}_pass_yards']
    total_yards_cml_after += game_df[f'{SIDE}_total_yards']

    ## CALCULATE RECORD NORMAL
    record_total_after = wins_after - losses_after # eg: +2 or -7 etc.
    record_normal_after = get_normalized(record_total_after, week * -1, week)

    ## WRITE THE RECORD
    col_arr = all_games_df.columns.values
    def update_df(col_name, value):
      ''' 
      heavily using globals! warned
      
      Had big problems updating with `at` and arrays so
      moved to looking up the position of the field in the
      column list and using iloc[row_idx,col_idx] to do updates
      '''
      col_idx = np.argmax(col_arr == col_name)
      all_games_df.iloc[[index],[col_idx]] = value
    
    update_df(f'{SIDE}_tie', (1 if tie else 0))
    update_df(f'{SIDE}_loss', (1 if loss else 0))
    update_df(f'{SIDE}_opp_trn', float(opp_trn))
    update_df(f'{SIDE}_wins_before',int(wins_before))
    update_df(f'{SIDE}_wins_after', int(wins_after))
    update_df(f'{SIDE}_losses_before', int(losses_before))
    update_df(f'{SIDE}_losses_after', int(losses_after))
    update_df(f'{SIDE}_ties_before',int(ties_before))
    update_df(f'{SIDE}_ties_after', int(ties_after))
    update_df(f'{SIDE}_record_total_before', int(record_total_before))
    update_df(f'{SIDE}_record_total_after', int(record_total_after))
    update_df(f'{SIDE}_record_normal_before', float(record_normal_before))
    update_df(f'{SIDE}_record_normal_after', float(record_normal_after))
    update_df(f'{SIDE}_opp_strength_before', float(opp_strength_before))
    update_df(f'{SIDE}_opp_strength_after', float(opp_strength_after))
    update_df(f'{SIDE}_opp_trn_before', float(opp_trn_before))
    update_df(f'{SIDE}_opp_trn_after', float(opp_trn_after))
    update_df(f'{SIDE}_points_cml_before', int(points_cml_before))
    update_df(f'{SIDE}_points_cml_after', int(points_cml_after))
    update_df(f'{SIDE}_week_rush_off_perf', float(week_rush_off_perf))
    update_df(f'{SIDE}_week_rush_def_perf', float(week_rush_def_perf))
    update_df(f'{SIDE}_week_rush_comp_perf', float(week_rush_comp_perf))
    update_df(f'{SIDE}_week_pass_off_perf', float(week_pass_off_perf))
    update_df(f'{SIDE}_week_pass_def_perf', float(week_pass_def_perf))
    update_df(f'{SIDE}_week_pass_comp_perf', float(week_pass_comp_perf))
    update_df(f'{SIDE}_week_comb_off_perf', float(week_comb_off_perf))
    update_df(f'{SIDE}_week_comb_def_perf', float(week_comb_def_perf))
    update_df(f'{SIDE}_week_comb_comp_perf', float(week_comb_comp_perf))
    update_df(f'{SIDE}_rush_yards_cml_before', int(rush_yards_cml_before))
    update_df(f'{SIDE}_pass_yards_cml_before', int(pass_yards_cml_before))
    update_df(f'{SIDE}_total_yards_cml_before', int(total_yards_cml_before))
    update_df(f'{SIDE}_rush_yards_cml_after', int(rush_yards_cml_after))
    update_df(f'{SIDE}_pass_yards_cml_after', int(pass_yards_cml_after))
    update_df(f'{SIDE}_total_yards_cml_after', int(total_yards_cml_after))
    update_df(f'{SIDE}_cml_rush_off_perf_before', float(cml_rush_off_perf_before))
    update_df(f'{SIDE}_cml_rush_def_perf_before', float(cml_rush_def_perf_before))
    update_df(f'{SIDE}_cml_rush_comp_perf_before', float(cml_rush_comp_perf_before))
    update_df(f'{SIDE}_cml_pass_off_perf_before', float(cml_pass_off_perf_before))
    update_df(f'{SIDE}_cml_pass_def_perf_before', float(cml_pass_def_perf_before))
    update_df(f'{SIDE}_cml_pass_comp_perf_before', float(cml_pass_comp_perf_before))
    update_df(f'{SIDE}_cml_comb_off_perf_before', float(cml_comb_off_perf_before))
    update_df(f'{SIDE}_cml_comb_def_perf_before', float(cml_comb_def_perf_before))
    update_df(f'{SIDE}_cml_comb_comp_perf_before', float(cml_comb_comp_perf_before))
    update_df(f'{SIDE}_cml_rush_off_perf_after', float(cml_rush_off_perf_after))
    update_df(f'{SIDE}_cml_rush_def_perf_after', float(cml_rush_def_perf_after))
    update_df(f'{SIDE}_cml_rush_comp_perf_after', float(cml_rush_comp_perf_after))
    update_df(f'{SIDE}_cml_pass_off_perf_after', float(cml_pass_off_perf_after))
    update_df(f'{SIDE}_cml_pass_def_perf_after', float(cml_pass_def_perf_after))
    update_df(f'{SIDE}_cml_pass_comp_perf_after', float(cml_pass_comp_perf_after))
    update_df(f'{SIDE}_cml_comb_off_perf_after', float(cml_comb_off_perf_after))
    update_df(f'{SIDE}_cml_comb_def_perf_after', float(cml_comb_def_perf_after))
    update_df(f'{SIDE}_cml_comb_comp_perf_after', float(cml_comb_comp_perf_after))
    
    return game_df


def create_final_file_from_year_files(data_path='../../data'):
  file_paths = glob.glob(f"{data_path}/games/all_with_agg_*.csv")
  file_paths.sort()
  file_paths
  
  all_games_df_list = []
  for file_path in file_paths:
      year_df = pd.read_csv(file_path)
      all_games_df_list.append(year_df)

  all_games_df = pd.concat(all_games_df_list, ignore_index=True)
  all_games_df.to_csv(f'{data_path}/games/all_games_with_data_and_agg.csv', index=False)
  home_df = all_games_df[all_games_df['home'] == 1]
  
  all_games_df.to_csv(f'{data_path}/nfl.csv', index=False)
  home_df.to_csv(f'{data_path}/nfl_home.csv', index=False)

  
### CALLED INTERFACE  
def create_single_year_file(year, data_path='../../data'):
  all_games_df = pd.read_csv(f'{data_path}/games/all_games_with_data.csv')
    
  if year is None:
    print('must include year to work. failed')
    return
    
  work_df = get_year_df(year, all_games_df)
  # work_df = work_df[work_df['week'] == 7]
  work_df = get_df_with_new_columns(work_df).copy()
  work_df.reset_index()
    
  ## Work each index in our sample
  total_count = len(work_df.index.values)
  last_perc_string = None
  for index in np.arange(0, total_count):
      update_df_with_aggregates(index, work_df, side='team')
      update_df_with_aggregates(index, work_df, side='opponent')
      perc_str = f'{(index / total_count)* 100:.0f} %'
      if perc_str != last_perc_string:
        last_perc_string = perc_str
        print(perc_str)

  ## PATCH TO NUMERIC
  # new_field_list = get_both_fields_list(get_new_field_roots())
  # work_df[new_field_list] = work_df[new_field_list].apply(pd.to_numeric)
  work_df.to_csv(f'{data_path}/games/all_with_agg_{year}.csv', index=False)

  return work_df



###  MAIN  :  CALLED INTERFACE  
def create_year_files(years, data_path='../../data'):
  
  # make a single an array
  if type(years) == str or type(years) == int:
    years = [years]
  
  if years is None or len(years) < 1:
    print('must include year to work. failed')
    return
  
  ## work each year into a file
  for year in years:
    print(f'Processing Year : {year}   -- -- -- -- -- --')
    create_single_year_file(year, data_path)

  ## write the final files
  create_final_file_from_year_files(data_path)


## TEMP DEV RUNS
# data_path='./data'
# create_all_games_with_data_and_agg(data_path)
# create_year_file(2020, data_path)
