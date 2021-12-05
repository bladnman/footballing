import utils.game_utils as gu

import math
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def bar_percent_plot(data: pd.DataFrame,
                     suptitle: str = None,
                     title: str = None,
                     show_quarters: bool = True,
                     ylimit = (0, 100)):
    """
    This plot will show the data from 0-100 percent. 
  
    Parameters
    --------
    show_quarters : bool, default: True
      Whether to show horiz-ax 
      lines at 25, 50, 75%
    
    ylimit : (min:int, max:int), default: (0, 100)
        Tuple describing any 
        ylimiting desired for the plot
      
    Examples
    --------
    ::

        bar_percent_plot(pdf, 
                        suptitle="Percenatage", 
                        title="2019 - 2021", 
                        ylimit=(20,80))
  """
    fig, ax = plt.subplots(figsize=(10, 5), dpi=100)

    if show_quarters:
        plt.axhline(y=75, color='red', linestyle='-', lw=1, alpha=0.1)
        plt.axhline(y=50, color='gray', linestyle='-', lw=1, alpha=0.4)
        plt.axhline(y=25, color='red', linestyle='-', lw=1, alpha=0.1)

    sns.barplot(data=data)

    plt.ylim(ylimit[0], ylimit[1])

    plt.xticks(rotation=90)
    plt.suptitle(suptitle, fontsize=16)
    plt.title(title)

    for p in ax.patches:
        ax.annotate(np.round(p.get_height(), decimals=2),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center',
                    va='center',
                    xytext=(0, 10),
                    textcoords='offset points')
