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
                     ylimit=(0, 100)):
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


def get_bar_color_25_50_75(height):
    if height >= 75: return 'green'
    if height >= 50: return '#69d'
    if height >= 25: return 'orange'
    return 'red'


def bar_percent_plot_v2(data: pd.DataFrame,
                        suptitle: str = None,
                        title: str = None,
                        x: str = None,
                        y: str = None,
                        show_quarters: bool = True,
                        color_fn=get_bar_color_25_50_75,
                        ylimit=(0, 100)):
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

    sns.barplot(data=data, x=x, y=y)

    plt.ylim(ylimit[0], ylimit[1])

    plt.xticks(rotation=90)
    plt.suptitle(suptitle, fontsize=16)
    plt.title(title)

    for p in ax.patches:
        height = p.get_height()
        width = p.get_width()
        x_pos = p.get_x()
        ax.annotate(np.round(height, decimals=2), (x_pos + width / 2., height),
                    ha='center',
                    va='center',
                    xytext=(0, 10),
                    textcoords='offset points')

        if color_fn is not None:
            p.set_color(color_fn(height))
