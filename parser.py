import datetime
from util import *
from commit_util import *

binutils_binaries = [
  "addr2line", "ar", "as", "c++filt", "elfedit", "gprof", "ld", "nm", \
  "objcopy", "objdump", "ranlib", "readelf", "size", "strings", "strip"
]

def get_changed_files_name(files_info):
  ret = []
  for file_info in files_info:
    ret.append(file_info["filename"])
  return ret


def build_pair(commit: Commit):
  commit_info = get_commit_info(commit)
  files_info = get_files_info(commit)

  changed_files_name = get_changed_files_name(files_info)
  patched_hash = commit_info["hash"]
  parent_hash = commit_info["parent_hash"]
  timestamp = commit_info["timestamp"]

  print("[*] file_name   :", changed_files_name)
  print("[*] timestamp   :", timestamp)
  print("[*] parent_hash :", parent_hash)
  print("[*] patched_hash:", patched_hash)
  print()

  curr_path = os.getcwd()
  base_path = curr_path + "/" + "base"
  scripts_path = curr_path + "/" + "scripts"
  bin_path = "/ext/bins/bin-" + timestamp + "-" + patched_hash
  config_opt = "--prefix={}"
 
  ## call builder
  os.environ["PARENT_HASH"] = parent_hash
  os.environ["PATCHED_HASH"] = patched_hash
  os.environ["BASE_PATH"] = base_path
  os.environ["BIN_PATH"] = bin_path
  os.environ["CONFIG_OPT"] = config_opt.format(base_path + "/install")

  cmd = scripts_path + "/build_binary_pair.sh"
  print("\n[*] build_binary_pair.sh")
  os.system(cmd)

  ## call gleaner  
  os.environ["BIN_PATH"] = bin_path
  cmd = scripts_path + "/glean_binary_pair.sh"
  print("\n[*] glean_binary_pair.sh")
  os.system(cmd)
  
  ## save files
  store_json(bin_path + "/commit_info", commit_info)
  store_json(bin_path + "/files_info", files_info)

  pass


def main():
  # project_path = os.getcwd()
  project_path = "/home/topcue/binary-gleaner"
  pure_base_path = project_path + "/pure_base"
  
  ## creat pure_base dir
  binutils_url = get_repo_url("binutils")
  pure_base_repo = git_clone_with_url(binutils_url, pure_base_path)
  print("[*] Base repo status:", get_status(pure_base_repo, pure_base_path))

  ## create base dir
  base_path = project_path + "/base"
  print("\n[*] base_path:", base_path)
  base_repo = try_clone_repo(pure_base_path, base_path)
  repo = base_repo

  ## get commits
  commits = get_commits_with_cnt(repo, 5000)
  start = datetime.datetime(2022, 1, 1)
  end = datetime.datetime.now()
  commits = get_commits_with_datetime_range(commits, start, end)
  
  ## TODO: Remove me after debugging!
  return

  ## build every pairs
  for commit in commits:
    build_pair(commit)


if __name__ == "__main__":
  main()


# EOF
