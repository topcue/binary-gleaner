import os
import sys
import re
import datetime
import urllib.parse
import urllib.request
import json
from git import *

commit_per_page = 30  # set by api

dict_repos = {
  "binutils": "bminor/binutils-gdb"
  # coreutils..
  # etc.
}

DATETIME_FORMAT = "%Y%m%dT%H%M%S"
EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

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

def get_git_repo_url_with_package_name(package: str):
  return "https://github.com/" + dict_repos[package]

def get_git_commit_url_with_package_name(package: str):
  return "https://api.github.com/repos/" + dict_repos[package] + "/commits"

def add_commit_url_to_page(url: str, page: int):
  return url + "?page=" + str(page)

# def read_json_from_url_with_token(url):
#   # get git_token manually
#   git_token = os.popen('cat $HOME/.git_token').read()[:-1]
#   headers = {"Authorization": "token " + git_token}
#   req = urllib.request.Request(url, headers = headers)
#   json_url = urllib.request.urlopen(req)
#   json_data = json.loads(json_url.read())
#   return json_data

# ================================================

## check if path is git repo
def is_git_repo(path):
  if os.path.exists(path) and os.path.isdir(path):
    try:
      _ = Repo(path).git_dir
      ret = True
    except InvalidGitRepositoryError:
      ret =  False
  else:
    ret = False
  return ret

## check if modified
def is_pure_repo(path: str): 
  if is_git_repo(path):
    repo = Repo(path)
    return (not repo.untracked_files and not repo.is_dirty())
  else:    
    return False

## get status w/o input check
def get_status(repo, path):
  changed = [ item.a_path for item in repo.index.diff(None) ]
  if path in repo.untracked_files:
    status = "untracked"
  elif path in changed:
    status = "modified"
  else:
    status = "pure"
  return status

## rm path and clone from git_url to path
def force_clone(git_url, path):
  print("[*] func force_clone()")
  os.system("rm -rf " + path)
  os.system("mkdir " + path)
  repo = Repo.clone_from(git_url, path)
  return repo

## create base dir
def git_clone_with_url(git_url, src_path):
  print("[DEBUG] Is '{}' pure repo?:".format(src_path), is_pure_repo(src_path))
  if is_pure_repo(src_path):
    repo = Repo(src_path)
  else:
    repo = force_clone(git_url, src_path)
  repo.remotes.origin.pull("master")
  return repo

## clone repo locally w/o input check
def clone_repo(src_path, dst_path):
  repo = Repo(src_path)
  os.system("rm -rf " + dst_path)
  os.system("mkdir " + dst_path)
  cloned_repo = repo.clone(os.path.join(src_path, dst_path))
  assert cloned_repo.__class__ is Repo     # clone an existing repository
  assert Repo.init(os.path.join(src_path, dst_path)).__class__ is Repo
  return cloned_repo

## reflect base paths checkout
def try_clone_repo(src_path, dst_path):
  if is_pure_repo(dst_path):
    repo = Repo(dst_path)
  else:
    repo = clone_repo(src_path, dst_path)
  return repo



# EOF
