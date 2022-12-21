import os, json, re, pdb, importlib.util
from os import path, listdir
from .utils import printer
from .threads import ThreadManager

class Config:

  def __init__(self, config_dir_path):
    self.config_dir_path = path.abspath(path.expanduser(config_dir_path))
    self.config_file_path = path.join(self.config_dir_path, "config.json")
    self.prompt_history_path = path.join(self.config_dir_path, "prompt_history")
    self.threads_dir_path = path.join(self.config_dir_path, "threads")
    self.plugins_dir_path = path.join(self.config_dir_path, "plugins")

    if not path.exists(self.config_dir_path):
      os.makedirs(self.config_dir_path)

    if not path.exists(self.threads_dir_path):
      os.mkdir(self.threads_dir_path)

    if not path.exists(self.plugins_dir_path):
      os.mkdir(self.plugins_dir_path)

    self.reload()

  def save(self):
      with open(self.config_file_path, "w") as config_file:
        json.dump(self.config or {}, config_file, indent=2)

  def reload(self):
    self.config = {}

    if not path.exists(self.config_file_path):
      self.save()

    with open(self.config_file_path, "r") as config_file:
      self.config = json.load(config_file)

    return self.config

  def threads(self):
    return ThreadManager(self)

  def load_plugins(self):
    files = os.listdir(self.plugins_dir_path)
    for file in files:
      file_path = path.join(self.plugins_dir_path, file)
      if not file_path.endswith('.py'):
        continue
      try:
        spec = importlib.util.spec_from_file_location('plugins', file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
      except Exception as e:
        printer.exception(e)
        continue
