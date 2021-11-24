def get_name():
  '''
  This function returns a name. This is intended to be updated
  multiple times while a notebook is running. I am attempting to
  see if the reloader works as desired
  
      import test_module_updates as tmu
      import importlib
      importlib.reload(tmu) # every run
  
  '''
  return "my name 3"
