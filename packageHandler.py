from util import *
from commit_util import *

from commitHandler import *
from builder import *


import datetime

class PackageHandler:
  PACKAGES = {
    "binutils": "bminor/binutils-gdb"
    # coreutils.. etc.
  }

  def __init__(self, package, pure, base):
    print(PACKAGES)
    self.package = package
    self.pure = pure
    self.base = base
    self.dataset = "dataset"
    self.repo = None
    self.commits = []


  def get_repo_url(self):
    return "https://github.com/" + PackageHandler.PACKAGES[self.package]


  def init_repo(self):
    ## init project path
    project_path = os.path.split(os.path.abspath(__file__))[0]
    pure_base_path = project_path + "/" + self.pure
    
    ## creat pure_base dir
    binutils_url = self.get_repo_url()
    pure_base_repo = git_clone_with_url(binutils_url, pure_base_path)
    
    ## create base dir
    base_path = project_path + "/" + self.base
    print("\n[*] base_path:", base_path)
    base_repo = try_clone_repo(pure_base_path, base_path)
    self.repo = base_repo

    return self.repo
  

  def get_commits(self):
    commits = get_commits_with_cnt(self.repo, 5000)
    start = datetime.datetime(2022, 6, 15)
    end = datetime.datetime.now()
    self.commits = get_commits_with_datetime_range(commits, start, end)
    
    return iter(self.commits)

  
  def collect_dataset(self):
    commits = self.get_commits()
    
    for commit in commits:
      ## get commit info
      comm_hdl = CommitHandler(commit)
      comm_hdl.get_diff_fils()
      comm_hdl.show_brief()

      ## save as xml file
      comm_hdl.save_info(self.repo)
      
      ## build binary pair
      build_helper = BuildHelper(comm_hdl, self.base, self.dataset)
      build_helper.configure()
      build_helper.get_binary_pairs()

# EOF
