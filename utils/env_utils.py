import os

def get_data_path():
  """Will search upward for first directory with a /data folder"""
  def get_dir(parts, num):
    return '/'.join(parts[:(-1*num)]) + '/data'
    
  cwd = os.getcwd()
  parts = cwd.split('/')
  for idx in range(0, len(parts)-1):
    dir_test = get_dir(parts, idx)
    exists = os.path.isdir(dir_test)
    if exists: return dir_test
    
  return None
