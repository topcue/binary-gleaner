import os
import json

from git import *

PACKAGES = {
  "binutils": "bminor/binutils-gdb"
  # coreutils..
  # etc.
}

DATETIME_FORMAT = "%Y%m%dT%H%M%S"
EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

# ================================================

def print_json(json_data):
  print(json.dumps(json_data, indent=2))

# ================================================

def get_repo_url(package: str):
  return "https://github.com/" + PACKAGES[package]

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
  assert cloned_repo.__class__ is Repo
  assert Repo.init(os.path.join(src_path, dst_path)).__class__ is Repo
  return cloned_repo

## reflect base paths checkout
def try_clone_repo(src_path, dst_path):
  if is_pure_repo(dst_path):
    repo = Repo(dst_path)
  else:
    repo = clone_repo(src_path, dst_path)
  
  ## TODO: Fix me
  cmd = "cd {path}; git checkout origin/master".format(path=dst_path)
  os.system(cmd)

  return repo

# EOF
