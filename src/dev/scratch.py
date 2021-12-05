# %%
import utils.game_utils as gu

import math
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

DATA_PATH = '../../data'
nfld = gu.NFL_Data(DATA_PATH)

### ### ### ### ### ### ### ### ###
###      SCRATCH WORK BELOW     ###
### ### ### ### ### ### ### ### ###


df = gu.get_year_week(nfld.data_by_game(), 2018, 6)
count = len(df)

# games where winners had most cml_yards_before
df[
    (df['win'] == 1)&(df['team_cml_total_yards_before'] > df['opponent_cml_total_yards_before']) |
    (df['win'] == 0)&(df['opponent_cml_total_yards_before'] <= df['team_cml_total_yards_before'])
  ]


# %%
