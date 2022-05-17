import datetime

from util import *
from commit_util import *
from info import *
from commit import *
from binary import *

from chunk import *

binutils_binaries = [
  "addr2line", "ar", "as", "c++filt", "elfedit", "gprof", "ld", "nm", \
  "objcopy", "objdump", "ranlib", "readelf", "size", "strings", "strip"
]


def dump(obj):
  print_json(dir(obj))


def init_repo(package):
  ## init project path
  project_path = os.path.split(os.path.abspath(__file__))[0]
  pure_base_path = project_path + "/pure_base"
  
  ## creat pure_base dir
  binutils_url = get_repo_url(package)
  pure_base_repo = git_clone_with_url(binutils_url, pure_base_path)

  ## create base dir
  base_path = project_path + "/base"
  print("\n[*] base_path:", base_path)
  base_repo = try_clone_repo(pure_base_path, base_path)

  return base_repo


def get_commits(repo: Repo):
  commits = get_commits_with_cnt(repo, 5000)
  start = datetime.datetime(2022, 5, 10)
  end = datetime.datetime(2022, 5, 11)
  commits = get_commits_with_datetime_range(commits, start, end)
  
  return iter(commits)


def main():
  repo = init_repo("binutils")
  commits = get_commits(repo)
  # commits = repo.iter_commits()
  
  # curr_comm = next(commits)
  
  for commit in commits:
    curr_comm = commit
    prev_comm = commit.parents[0] if commit.parents else EMPTY_TREE_SHA

    files_info = get_diff_file_paths(curr_comm, prev_comm)

    print("\n" + "=" * 100)
    print("[*] current commit:", curr_comm.hexsha)
    print("[*] parent commit: ", prev_comm.hexsha)
    
    # continue
    print("[*] Num of diff files:", len(files_info))

    # save as xml file
    root = build_xml_info(repo, curr_comm, prev_comm, files_info)
    file_path = "tmp/info-" + get_committed_datetime(commit) + "-" + curr_comm.hexsha
    store_xml(root, file_path)

    ## pattern matching
    ## pattern_mathcing(curr_comm, prev_comm, repo)
  

    build_binary_pair(curr_comm, prev_comm)

    curr_comm = commit
  
  ## build binary pairs
  for commit in commits:
    pass
    


if __name__ == "__main__":
  main()


# EOF
