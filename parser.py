from util import *

max_page_num = 2     # set by user

def get_commits_with_datetime_range(start_datetime, end_datetime):
  # get commit_file_names with datetime range
  file_names = os.listdir("./commits")
  commit_file_names = []
  for file_name in file_names:
    commit_file_date_time = file_name[7 : 23] # get datetime part
    if start_datetime < commit_file_date_time < end_datetime:
      commit_file_names.append(file_name)
  commit_file_names.sort()

  # get commits(json) with datetime range
  commits = []
  for commit_file_name in commit_file_names:
    commits.append(load_json("./commits/" + commit_file_name))
  
  return commits

def get_parent_url(parent):
  return parent["url"]

def get_parent_sha(parent):
  return parent["sha"]

def get_commit_message(commit_data):
  msg = commit_data["message"].split('\n')
  head = msg[0]
  body_list = msg[2:] if len(msg) >= 2 else ""
  body = ""
  for line in body_list:
    body += line + "\n"
  return [head, body]


known_binaries = [
  "addr2line", "ar", "bfdtest1", "bfdtest2", "cxxfilt", "elfedit", "nm", "objcopy", "objdump", "ranlib", "readelf", "size", "strings", "strip", "sysinfo"
]

def parse_files_change(files):
  # print("status:", file["status"])
  # print("changes:", file["changes"])
  ret = []
  for file in files:
    file_name = file["filename"]
    for known_binary in known_binaries:
      if "binutils/" + known_binary in file_name:
        # print("filename:", file_name)
        ret.append(known_binary)
  return ret

def parse_commit(json_data):
  #### get child's info
  child_sha = json_data["sha"]
  child_url = json_data["url"]
  
  #### get parent's info
  parent = json_data["parents"][0]
  parent_url = get_parent_url(parent)
  parent_sha = get_parent_sha(parent)
  
  #### get commit detail
  commit_data = json_data["commit"]
  datetime = commit_data["committer"]["date"].replace('-', '').replace(':', '')  
  # msg = commit_data["message"]
  # p = re.compile(r'secur|vuln|cve', re.I)
  # feature = p.findall(msg)
  
  #### get file detail
  files = json_data["files"]
  changed_file_names = parse_files_change(files) # select file and binary here

  
  
  if not changed_file_names:
    return 0
  else:
    print()
    print("[*] file_name:", changed_file_names)
    print("[*] child_sha: ", child_sha)
    print("[*] parent_sha:", parent_sha)

    base_path = "/home/topcue/bincollector"
    origin_path = base_path + "/" + "origin"
    bin_path = base_path + "/" + "bins/bin-" + datetime + "-" + child_sha
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

    # return 0

    cmd = "\
      mkdir -p {bin_path}                                             ;\n\
      cd {origin_path} && git checkout {child_sha}                    ;\n\
      rm -rf {origin_path}/build                                      ;\n\
      mkdir -p {origin_path}/build                                    ;\n\
      cd {origin_path}/build && {origin_path}/configure -q {config_opt} ;\n\
      cd {origin_path}/build && make > child_make.log                 ;\n\
      cp -r {origin_path}/build/binutils {bin_path}/                  ;\n\
      cp -r {origin_path}/build/child_make.log {bin_path}/                     ;\n\
      mv {bin_path}/binutils {child_path}                             ;\n\
                                                                       \n\
      cd {origin_path} && git checkout {parent_sha}                   ;\n\
      rm -rf {origin_path}/build                                      ;\n\
      mkdir -p {origin_path}/build                                    ;\n\
      cd {origin_path}/build && {origin_path}/configure -q {config_opt} ;\n\
      cd {origin_path}/build && make > parent_make.log                ;\n\
      cp -r {origin_path}/build/binutils {bin_path}/                  ;\n\
      cp -r {origin_path}/build/parent.log {bin_path}/                     ;\n\
      mv {bin_path}/binutils {parent_path}                            ;\n\
    "
    
    cmd = cmd.format( origin_path=origin_path, bin_path=bin_path,     \
                      child_sha=child_sha, parent_sha=parent_sha,     \
                      child_path=child_path, parent_path=parent_path, \
                      config_opt=config_opt)
    os.system(cmd)

    is_exist = os.path.isdir(child_path) and os.path.isdir(parent_path)
    if is_exist:
      print("[+] Success!")
      with open(bin_path + "/state", 'w') as outfile:
        outfile.write("done")
    else:
      print("[-] Failed..")
      exit(0)

def main():
  # get commits
  start_datetime = datetime.datetime(2021, 1, 1, 0, 0, 0).strftime("%Y%m%dT%H%M%SZ")
  end_datetime = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
  commits = get_commits_with_datetime_range(start_datetime, end_datetime)

  # parse commits
  for commit in commits:
    parse_commit(commit)

if __name__ == "__main__":
  main()

# EOF
