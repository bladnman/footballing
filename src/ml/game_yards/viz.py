#%%
import sys
sys.path.insert(0, '..')
sys.path.insert(0, '../..')
import utils.game_utils as gu

import math
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
data_path = '../../../data'
nfld = gu.NFL_Data(data_path)


# %%
nfl_df = nfld.data_by_game()
samp_df = nfl_df[['year', 'win']]
win_perc_year_df = samp_df.groupby('year').sum() / samp_df.groupby('year').count() * 100
win_perc_year_df

fig, ax = plt.subplots(figsize=(10,5),dpi=100)
win_perc_year_df.plot(kind='bar', ax=ax, legend=None)

for p in ax.patches:                 
  ax.annotate(np.round(p.get_height(),decimals=2), 
              (p.get_x()+p.get_width()/2., p.get_height()),                              
              ha='center',                              
              va='center',                              
              xytext=(0, 10),                               
              textcoords='offset points')
  
plt.axhline(y=50, color='gray', linestyle='-', lw=1, alpha=0.6)
plt.ylim(bottom=40)
plt.ylabel('Home Win %');
plt.title('Home Field Advantage?', fontsize=17)
plt.suptitle('Is being at home a predictor of victory? : 2010-2021')
# %%

def get_win_with_more_points_per_for_week(week):
  week_df = home_df[home_df['week'] == week]
  game_count = len(week_df)
  wins_with_more_points = len(week_df[(
      (week_df['win'] == 1)&(week_df['team_points_cml_before'] > week_df['opponent_points_cml_before']) |
      (week_df['win'] == 0)&(week_df['team_points_cml_before'] <= week_df['opponent_points_cml_before'])
    )])
  
  return (wins_with_more_points / game_count * 100, wins_with_more_points)



nfl_df = nfld.data_by_team()
samp_df = nfl_df[['year', 'win', 'team_total_yards_cml_before','opponent_total_yards_cml_before']]

win_perc_year_df = samp_df.groupby('year').sum() / samp_df.groupby('year').count() * 100
win_perc_year_df

# -- charting
fig, ax = plt.subplots(figsize=(10,5),dpi=100)
win_perc_year_df.plot(kind='bar', ax=ax, legend=None)
for p in ax.patches:                 
  ax.annotate(np.round(p.get_height(),decimals=2), 
              (p.get_x()+p.get_width()/2., p.get_height()),                              
              ha='center',                              
              va='center',                              
              xytext=(0, 10),                               
              textcoords='offset points')
plt.axhline(y=50, color='gray', linestyle='-', lw=1, alpha=0.6)
plt.ylim(bottom=40)
plt.ylabel('Home Win %');
plt.title('Most Accumulated Yards', fontsize=17)
plt.suptitle('Is having the most yards previously a predictor? : 2010-2021')

# %%
df = gu.get_year_week(nfld.data_by_game(), 2018, 6)
count = len(df)
df[
    (df['win'] == 1)&(df['team_total_yards_cml_before'] > df['opponent_total_yards_cml_before']) |
    (df['win'] == 0)&(df['opponent_total_yards_cml_before'] <= df['team_total_yards_cml_before'])
  ]

# %%

def add_did_gt_win(df, new_fieldname, root_test_field_name):
  df[new_fieldname] = ((df['win']) & (df[f'team_{root_test_field_name}'] > df[f'opponent_{root_test_field_name}'])) | ((df['win'] == 0) & (df[f'team_{root_test_field_name}'] <= df[f'opponent_{root_test_field_name}']))

# need to copy as we will be adding these new results as fields
# df = nfld.data_by_game().copy()
df = nfld.data_by_game()
# df = df[df['year'] > 2015]
df = df.copy()

conf_list = [
  ('top_pass_won', 'pass_yards', 'Game Passing Yds'),
  ('top_rush_won', 'rush_yards', 'Game Rushing Yds'),
  ('top_total_won', 'total_yards', 'Game Total Yds'),
  ('top_rush_cml_b4_won', 'rush_yards_cml_before', 'Most Cuml Rush Yds'),
  ('top_total_cml_b4_won', 'total_yards_cml_before', 'Most Cuml Yds'),
  ('top_total_pass_comp_perf_won', 'week_pass_comp_perf', 'Passing Perf'),
  ('top_total_rush_comp_perf_won', 'week_rush_comp_perf', 'Rushing Perf'),
  ('top_total_comb_comp_perf_won', 'week_comb_comp_perf', 'Combined Perf'),
  ('top_third_dwn_ratio_won', 'third_down_ratio', '3rd Down Ratio'),
  ('top_record_normal_before_won', 'record_normal_before', 'Record Entering Week'),
]

columns = []
fields = []
for conf_item in conf_list:
  new_fieldname, root_test_field_name, col_label = conf_item
  add_did_gt_win(df, new_fieldname, root_test_field_name)
  columns.append(col_label)
  fields.append(new_fieldname)

data_df = df[['year'] + fields]

### NOW PLOT
count = len(data_df)

c_data = data_df.drop('year', axis=1)
c_data.columns = columns
c_data = (c_data.sum() / count * 100).sort_values()

mmin = c_data.min() - 5
mmax = c_data.max() + 5
min_year = df['year'].min()
max_year = df['year'].max()

fig, ax = plt.subplots(figsize=(10,5),dpi=100)
c_data.plot(kind="bar")
plt.ylim(mmin,mmax)
plt.axhline(y=50, color='gray', linestyle='-', lw=1, alpha=0.6)
plt.title('Win Predictors', fontsize=17)
plt.suptitle(f'% stat was won by victor : {min_year}-{max_year}')

for p in ax.patches:                 
  ax.annotate(np.round(p.get_height(),decimals=2), 
              (p.get_x()+p.get_width()/2., p.get_height()),                              
              ha='center',                              
              va='center',                              
              xytext=(0, 10),                               
              textcoords='offset points')

# %%
df = nfld.data_by_game()
df = df[df['year'] == 2018]
# df = df[df['week'] == 14]

fields = [
  'record_normal_before', 
  'third_down_ratio', 
  'points_cml_before',
  'rush_yards_cml_before',
  'cml_rush_off_perf_before',
  'fourth_down_conversions',
  'opp_trn_before',
  'rush_yards',
  'pass_yards',
  'total_yards',
]
data = {}
for field in fields:
  perc, total = gu.get_wins_with_more_in_field(df, field)
  data[field] = perc


for item in data: data[item] = [data[item]]
pdf = pd.DataFrame(data)
# sort the columns
pdf = pdf.T.sort_values(by=0).T
plt.figure(figsize=(10,6), dpi=150)
sns.barplot(data=pdf)
plt.ylim(pdf.T.min()[0] - 5, pdf.T.max()[0] + 5)
plt.xticks(rotation=90);

# %%
def get_perc(df, field):
  '''
  Given a df and a field, return the number of time the 
  winning team lead in that field.
  
  If there is a '!' in the field name the invert the 
  logic
  '''
  if field.startswith('!'):
    field = field.replace('!','')
    wins_df = df[
      ((df['win'] == 0) & (df[f'team_{field}'] > df[f'opponent_{field}']))|
      ((df['win'] == 1) & (df[f'team_{field}'] <= df[f'opponent_{field}']))
    ]
  else:
    wins_df = df[
        ((df['win'] == 1) & (df[f'team_{field}'] > df[f'opponent_{field}']))|
        ((df['win'] == 0) & (df[f'team_{field}'] <= df[f'opponent_{field}']))
      ]

  return (len(wins_df) / len(df)) * 100
def work_fields_by_year(df, fields):
  for field in fields:
    data = {}
    
    for year in df['year'].unique():
      data[year] = get_perc(df[df['year'] == year], field)

    for item in data: data[item] = [data[item]]
    pdf = pd.DataFrame(data)
    # sort the columns
    # pdf = pdf.T.sort_values(by=0).T
    ymin = min(45, pdf.T.min()[0] - 5)
    ymax = max(55, pdf.T.max()[0] + 5)
    plt.figure(figsize=(10,6), dpi=150)
    sns.barplot(data=pdf)
    plt.ylim(ymin, ymax)
    plt.xticks(rotation=90);
    plt.suptitle(f'Win % When Leading In: {field}', fontsize=16)
    plt.axhline(y=50, color='gray', linestyle='-', lw=1, alpha=0.6)
    plt.axhline(y=75, color='red', linestyle='-', lw=1, alpha=0.6)
    plt.axhline(y=25, color='red', linestyle='-', lw=1, alpha=0.6)
def work_fields(df, fields):
  data = {}
  for field in fields:
    data[field] = get_perc(df, field)

  for item in data: data[item] = [data[item]]
  pdf = pd.DataFrame(data)
  # sort the columns
  # pdf = pdf.T.sort_values(by=0).T
  ymin = min(45, pdf.T.min()[0] - 5)
  ymax = max(55, pdf.T.max()[0] + 5)
  min_year = df['year'].min()
  max_year = df['year'].max()
  
  fig, ax = plt.subplots(figsize=(10,5),dpi=100)
  # plt.figure(figsize=(10,6), dpi=150)
  sns.barplot(data=pdf, ax=ax)
  # plt.ylim(ymin, ymax)
  plt.xticks(rotation=90);
  plt.suptitle('Win % when leading in a stat:', fontsize=16)
  if min_year == max_year:
    plt.title(f'{min_year}')
  else:
    plt.title(f'{min_year} - {max_year}')
  plt.axhline(y=50, color='gray', linestyle='-', lw=1, alpha=0.3)
  # plt.axhline(y=75, color='gray', linestyle='-', lw=1, alpha=0.3)
  # plt.axhline(y=25, color='gray', linestyle='-', lw=1, alpha=0.3)
  for p in ax.patches:                 
    ax.annotate(np.round(p.get_height(),decimals=2), 
                (p.get_x()+p.get_width()/2., p.get_height()),                              
                ha='center',                              
                va='center',                              
                xytext=(0, 10),                               
                textcoords='offset points')


fields = [
    'score',
    'rush_yards',
    'pass_yards', 
    'total_yards', 
    'rush_count',
    '!turnovers_lost',
    '!sack_count',
    'penalty_count',
    'penalty_yards',
  ]
games_df = nfld.data_by_game()
work_fields(gu.get_year(games_df, 2021), fields)
work_fields_by_year(games_df, fields)


# %%
df['year'].unique().values
# %%
