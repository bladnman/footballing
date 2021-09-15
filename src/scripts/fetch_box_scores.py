# CONFIG
START_YEAR = 2010
END_YEAR = 2020
DATA_PATH = '../data/box_scores'
_is_dev_mode = True

import numpy as np
import pandas as pd
from dateutil import parser


def main():
    print('okay then')


def _dev_main():
    print('dev time')


# do the work
if _is_dev_mode:
    _dev_main()
else:
    main()
