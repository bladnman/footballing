# import utils.add_aggregates as add_aggregates
# import utils.fetch_games as fetch_games
# import utils.fetch_info_and_stats as fetch_info_and_stats
# import utils.game_utils as game_utils
# import utils.env_utils as env_utils
# import utils.plot as plot


import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "utils"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
