from abc import *

from util import *
from commit_util import *
from commitHandler import *
# from packageHandler import *


class BuildHelper:

  def __init__(self, comm_hdl: CommitHandler, base: str, dataset: str):
    commit = comm_hdl.curr_comm
    self.curr_comm = commit
    self.prev_comm = commit.parents[0] if commit.parents else EMPTY_TREE_SHA
    self.base = base
    self.dataset = dataset
  

  def get_binary_pairs(self):
    scripts_path = os.getcwd() + "/" + "scripts"

    builder = BinaryBuilder()
    builder.set_script_path(scripts_path)
    builder.run()

    gleaner = BinaryGleaner()
    gleaner.set_script_path(scripts_path)
    gleaner.run()


  def configure(self):
    patched_hash = self.curr_comm.hexsha
    parent_hash = self.prev_comm.hexsha
    timestamp = get_committed_datetime(self.curr_comm)

    curr_path = os.getcwd()
    base_path = curr_path + "/" + "base"
    bin_path = curr_path + "/dataset/bin-" + timestamp + "-" + patched_hash
    config_opt = "--prefix={}"
    ## TODO: Rremove this options
    config_opt += " --disable-gdb --disable-gdbserver --disable-sim"

    ## env for builder    
    os.environ["PARENT_HASH"] = parent_hash
    os.environ["PATCHED_HASH"] = patched_hash
    os.environ["BASE_PATH"] = base_path
    os.environ["BIN_PATH"] = bin_path
    os.environ["CONFIG_OPT"] = config_opt.format(base_path + "/install")


class AbstractScriptRunner(metaclass=ABCMeta):
  
  @abstractmethod
  def set_script_path(self):
    pass

  
  @abstractmethod
  def run(self):
    pass


class BinaryBuilder(AbstractScriptRunner):
  
  def set_script_path(self, script_path: str):
    self.script_path = script_path

  def run(self):
    print("\n[*] run build_binary_pair.sh")
    cmd = self.script_path + "/build_binary_pair.sh"
    os.system(cmd)


class BinaryGleaner(AbstractScriptRunner):

  def set_script_path(self, script_path: str):
    self.script_path = script_path
  
  def run(self):
    print("\n[*] run glean_binary_pair.sh")
    cmd = self.script_path + "/glean_binary_pair.sh"
    os.system(cmd)


# EOF
