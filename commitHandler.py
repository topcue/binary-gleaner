from info import *
from commit_util import *

class CommitHandler:

  def __init__(self, commit: Commit):
    self.curr_comm = commit
    self.prev_comm = commit.parents[0] if commit.parents else EMPTY_TREE_SHA
    self.files_info = []

  def show_brief(self):
    print("\n" + "=" * 100)
    print("[*] current commit:", self.curr_comm.hexsha)
    print("[*] parent commit: ", self.prev_comm.hexsha)

    if self.files_info:
      print("[*] Num of diff files:", len(self.files_info))
  

  def get_diff_fils(self):
    # diffs = prev_comm.diff(curr_comm)
    # fileA = diff.a_blob.data_stream.read().decode('utf-8')
    # fileB = diff.b_blob.data_stream.read().decode('utf-8')

    diffs  = {
      diff.a_path: diff for diff in self.curr_comm.diff(self.prev_comm, create_patch=True)    
    }
    
    for objpath, stats in self.curr_comm.stats.files.items(): 
      diff = diffs.get(objpath)
      if not diff:
        for diff in diffs.values():
          if diff.renamed: break
      
      if diff_type(diff) == 'M':
        path_A = diff.a_blob.path if diff.a_blob else None
        path_B = diff.b_blob.path if diff.b_blob else None
        assert path_A == path_B

      self.files_info.append({
        'path'     : objpath,
        'type'     : diff_type(diff),
        'stats'    : stats
      })
    
    return self.files_info
  

  def save_info(self, repo: Repo):
    root = build_xml_info(repo, self.curr_comm, self.prev_comm, self.files_info)
    file_path = "dataset/info-" + get_committed_datetime(self.curr_comm) + "-" + self.curr_comm.hexsha
    store_xml(root, file_path)


# EOF
