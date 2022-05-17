from util import *
from commit_util import *


def build_binary_pair(curr_comm: Commit, prev_comm: Commit):
  patched_hash = curr_comm.hexsha
  parent_hash = prev_comm.hexsha
  timestamp = get_committed_datetime(curr_comm)

  curr_path = os.getcwd()
  base_path = curr_path + "/" + "base"
  scripts_path = curr_path + "/" + "scripts"
  bin_path = "/ext/bins/bin-" + timestamp + "-" + patched_hash
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
  print("\n[*] build_binary_pair.sh")
  os.system(cmd)

  ## call gleaner 
  os.environ["BIN_PATH"] = bin_path
  cmd = scripts_path + "/glean_binary_pair.sh"
  print("\n[*] glean_binary_pair.sh")
  os.system(cmd)
  
  pass

# EOF
