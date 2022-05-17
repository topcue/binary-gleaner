from util import *
from commit_util import *
from difflib import *


def get_diff_file_paths(curr_comm: Commit, prev_comm: Commit):
  # diffs = prev_comm.diff(curr_comm)
  files_info = []
  diffs  = {
    diff.a_path: diff for diff in curr_comm.diff(prev_comm, create_patch=True)    
  }
  
  for objpath, stats in curr_comm.stats.files.items(): 
    diff = diffs.get(objpath)
    if not diff:
      for diff in diffs.values():
        if diff.renamed: break
    
    if diff_type(diff) == 'M':
      path_A = diff.a_blob.path if diff.a_blob else None
      path_B = diff.b_blob.path if diff.b_blob else None
      assert path_A == path_B

    files_info.append({
      'path'     : objpath,
      'type'     : diff_type(diff),
      'stats'    : stats,
      'contents' : ""
    })
  
  return files_info

# EOF
