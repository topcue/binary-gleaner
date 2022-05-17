from util import *
from commit_util import *
from info import *
from packageHandler import *
from commitHandler import *
from builder import *

def main():
  pkg_hdl = PackageHandler("binutils", "pure_base", "base")
  pkg_hdl.init_repo()
  commits = pkg_hdl.get_commits()
  
  for commit in commits:
    comm_hdl = CommitHandler(commit)
    comm_hdl.get_diff_fils()
    comm_hdl.show_brief()

    ## save as xml file
    comm_hdl.save_info(pkg_hdl.repo)

    ## pattern matching
    # pattern_mathcing(curr_comm, prev_comm, repo)
    
    # comm_hdl.build_binary_pair()
    builder = Builder(comm_hdl)
    builder.build_binary_pair()

    pass
    

if __name__ == "__main__":
  main()


# EOF
