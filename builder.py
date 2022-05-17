from util import *
from commit_util import *
from commitHandler import *

class Builder:
  def __init__(self, comm_hdl: CommitHandler):
    commit = comm_hdl.curr_comm
    self.curr_comm = commit
    self.prev_comm = commit.parents[0] if commit.parents else EMPTY_TREE_SHA
  
  def build_binary_pair(self):
    patched_hash = self.curr_comm.hexsha
    parent_hash = self.prev_comm.hexsha
    timestamp = get_committed_datetime(self.curr_comm)

    curr_path = os.getcwd()
    base_path = curr_path + "/" + "base"
    scripts_path = curr_path + "/" + "scripts"
    # bin_path = "/ext/bins/bin-" + timestamp + "-" + patched_hash
    bin_path = "/home/topcue/binary-gleaner/tmp/bin-" + timestamp + "-" + patched_hash
    config_opt = "--prefix={}"
    ## TODO: Rremove this options
    config_opt += " --disable-gdb --disable-gdbserver --disable-sim"

    ## call builder
    os.environ["PARENT_HASH"] = parent_hash
    os.environ["PATCHED_HASH"] = patched_hash
    os.environ["BASE_PATH"] = base_path
    os.environ["BIN_PATH"] = bin_path
    os.environ["CONFIG_OPT"] = config_opt.format(base_path + "/install")

    cmd = scripts_path + "/build_binary_pair.sh"
    print("\n[*] run build_binary_pair.sh")
    os.system(cmd)

    ## call gleaner 
    os.environ["BIN_PATH"] = bin_path
    cmd = scripts_path + "/glean_binary_pair.sh"
    print("\n[*] run glean_binary_pair.sh")
    os.system(cmd)

    pass


# EOF
