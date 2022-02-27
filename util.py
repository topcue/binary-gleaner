import os
import sys
import re
import datetime
import urllib.parse
import urllib.request
import json

commit_per_page = 30  # set by api

dict_repos = {
  "binutils": "bminor/binutils-gdb"
  # coreutils..
  # etc.
}

# ================================================

def print_json(json_data):
  print(json.dumps(json_data, indent=2))

def store_json(file_path: str, json_data):
  with open(file_path, 'w') as outfile:
    json.dump(json_data, outfile, indent=2)

def load_json(file_path: str):
  with open(file_path, "r") as json_file:
    json_data = json.load(json_file)
  return json_data

# ================================================

def get_git_commit_url_with_package_name(package: str):
  return "https://api.github.com/repos/" + dict_repos[package] + "/commits"

def add_commit_url_to_page(url: str, page: int):
  return url + "?page=" + str(page)

def read_json_from_url_with_token(url):
  # get git_token manually
  git_token = os.popen('cat $HOME/.git_token').read()[:-1]
  headers = {"Authorization": "token " + git_token}
  req = urllib.request.Request(url, headers = headers)
  json_url = urllib.request.urlopen(req)
  json_data = json.loads(json_url.read())
  return json_data

# ===========================================================
