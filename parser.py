from datetime import date
from util import *
from commit_util import *

max_page_num = 2     # set by user

binutils_binaries = [
  "addr2line", "ar", "cxxfilt", "elfedit", "nm", "objcopy", "objdump", "ranlib", "readelf", "size", "strings", "strip", "sysinfo"
]

def get_commit_info(commit: Commit, file_info):
  parent = get_commit_parent(commit)
  # file_info = get_files_info(commit)
  commit_info = {
    "hash": get_commit_hash(commit),
    "parent_hash": get_commit_hash(parent),
    "timestamp": get_authored_datetime(commit),
    "msg": get_commit_message(commit),
    "changed_file_len": len(file_info),
    "files": file_info
  }
  
  return commit_info

def get_changed_files_name(commit_info):
  ret = []
  for file in commit_info["files"]:
    for known_binary in binutils_binaries:
      if "binutils/" + known_binary in file["filename"]:
        ret.append(file["filename"])
  return ret

def foo(commit_info):
  changed_file_names = get_changed_files_name(commit_info)
  child_hash = commit_info["hash"]
  parent_hash = commit_info["parent_hash"]
  timestamp = commit_info["timestamp"]

  print("\n[*] file_name:", changed_file_names)
  print("[*] child_hash: ", child_hash)
  print("[*] parent_hash:", parent_hash)

  


  curr_path = os.getcwd()
  base_path = curr_path + "/" + "base"
  bin_path = "/ext/bins/bin-" + timestamp + "-" + child_hash
  child_path = bin_path + "/" + "child"
  parent_path = bin_path + "/" + "parent"
  config_opt = "--disable-gdb --disable-gdbserver --disable-ld --disable-gold --disable-gas --disable-sim --disable-gprof"
  
  # todo: change state to json
  if os.path.isfile(bin_path + "/state"):
    with open(bin_path + "/state", 'r') as f:
      state = f.read()
      if "done" in state: 
        print("[+] Exist. Pass.")
        return 0
      else:
        print("[-] Not exist. Build it. (1)")
  else:
    print("[-] Not exist. Build it. (2)")

  

  cmd = "\
    mkdir -p {bin_path}                                            ;\n\
    cd {base_path} && git checkout {child_hash}                    ;\n\
    rm -rf {base_path}/build                                       ;\n\
    mkdir -p {base_path}/build                                     ;\n\
    cd {base_path}/build && {base_path}/configure -q {config_opt}  ;\n\
    cd {base_path}/build && make > child_make.log                  ;\n\
    cp -r {base_path}/build/binutils {bin_path}/                   ;\n\
    cp -r {base_path}/build/child_make.log {bin_path}/             ;\n\
    mv {bin_path}/binutils {child_path}                            ;\n\
                                                                   \n\
    cd {base_path} && git checkout {parent_hash}                   ;\n\
    rm -rf {base_path}/build                                       ;\n\
    mkdir -p {base_path}/build                                     ;\n\
    cd {base_path}/build && {base_path}/configure -q {config_opt}  ;\n\
    cd {base_path}/build && make > parent_make.log                 ;\n\
    cp -r {base_path}/build/binutils {bin_path}/                   ;\n\
    cp -r {base_path}/build/parent.log {bin_path}/                 ;\n\
    mv {bin_path}/binutils {parent_path}                           ;\n\
  "
  
  cmd = cmd.format( base_path=base_path, bin_path=bin_path,     \
                    child_hash=child_hash, parent_hash=parent_hash,     \
                    child_path=child_path, parent_path=parent_path, \
                    config_opt=config_opt)

  print(cmd)
  return 0
  os.system(cmd)

  is_exist = os.path.isdir(child_path) and os.path.isdir(parent_path)
  if is_exist:
    print("[+] Success!")
    with open(bin_path + "/state", 'w') as outfile:
      outfile.write("done")
  else:
    print("[-] Failed..")
    exit(0)


## TODO: Refactor me
def filter_binutils_binary(commit: Commit):
  file_info = get_files_info(commit)
  for file in file_info:
    for known_binary in binutils_binaries:
      if "binutils/" + known_binary in file["filename"]:
        # print("[*]", file["filename"])
        return file_info
  
  return [ ]

def main():
  home_path = "/Users/topcue"
  project_path = home_path + "/binary-gleaner"
  base_path = "/Users/topcue/binary-gleaner/base" 
  
  ## creat base dir
  binutils_url = get_git_repo_url_with_package_name("binutils")
  base_repo = create_base(binutils_url, base_path)
  print("[*] Base repo status:", get_status(base_repo, base_path))
  print()
  
  ## create test dir
  test_path = project_path + "/test"
  test_repo = try_clone_repo(base_path, test_path)
  repo = test_repo

  ## get commits
  commits = get_commits_with_cnt(repo, 15000)[::-1]  
  start_datetime = datetime.datetime(2022, 1, 1)
  end_datetime = datetime.datetime.now()
  commits = get_commits_with_datetime_range(commits, start_datetime, end_datetime)

  ## parse commits
  for commit in commits:
    ## TODO: Find better way
    ## Filter only if the source code - binary change relationship can be tracked
    file_info = filter_binutils_binary(commit)
    if not file_info:
      continue
    
    commit_info = get_commit_info(commit, file_info)
    foo(commit_info)


if __name__ == "__main__":
  main()

# EOF
