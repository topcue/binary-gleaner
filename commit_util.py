from util import *

def get_commit_parent(commit):
  return commit.parents[0] if commit.parents else EMPTY_TREE_SHA

def get_committed_datetime(commit):
  return commit.committed_datetime.strftime(DATETIME_FORMAT)

def get_authored_datetime(commit):
  return commit.authored_datetime.strftime(DATETIME_FORMAT)

## TODO: master vs origin/master
def get_all_commits(repo):
  return list(repo.iter_commits('master'))

def get_commits_with_cnt(repo, cnt):
  return list(repo.iter_commits('origin/master', max_count=cnt, skip=0)) 

def get_commits_with_datetime_range(commits, start, end):
  start_datetime = start.strftime(DATETIME_FORMAT)
  end_datetime = end.strftime(DATETIME_FORMAT)
  result = []
  for commit in commits:
    authored_datetime = get_committed_datetime(commit)
    if start_datetime < authored_datetime < end_datetime:
      result.append(commit)
  return result

def diff_type(diff: Diff):
  if diff.renamed: return 'R'
  if diff.deleted_file: return 'D'
  if diff.new_file: return 'A'
  return 'M'

def get_diff_files(diff: Diff):
  fileA = diff.a_blob.data_stream.read().decode('utf-8')
  fileB = diff.b_blob.data_stream.read().decode('utf-8')
  return fileA, fileB

# def get_diff_type(commit: Commit):
#   parent = get_commit_parent(commit)
#   diff_index = parent.diff(commit, create_patch=True)
#
#   for diff_idx in diff_index:
#     if diff_idx.new_file:
#       print("[*] Added")
#     elif diff_idx.deleted_file:
#       print("[*] Deleted")
#     elif diff_idx.renamed:
#       print("[*] Renamed")
#     elif diff_idx.a_blob and diff_idx.b_blob and diff_idx.a_blob != diff_idx.b_blob:
#       print("[*] Modified")
#     elif diff_idx.copied_file:
#       print("[*] Copied")
#     else:
#       print("[*] ???")
    
#     return diff_idx

# def get_files_info(commit: Commit):
#   parent = commit.parents[0] if commit.parents else EMPTY_TREE_SHA
#   diffs  = {
#     diff.a_path: diff for diff in commit.diff(parent, create_patch=True)    
#   }
  
#   files_info = []
#   for objpath, stats in commit.stats.files.items(): 
#     diff = diffs.get(objpath)
#     if not diff:
#       for diff in diffs.values():
#         if diff.renamed:
#           break
    
#     files_info.append({
#       'filename': objpath,
#       'type'    : diff_type(diff),
#       'stats'   : stats,
#       'patch'   : "" #str(diff)
#     })
  
#   return files_info

# def get_commit_info(commit: Commit):
#   parent = get_commit_parent(commit)
#   commit_info = {
#     "hash"       : get_commit_hash(commit),
#     "parent_hash": get_commit_hash(parent),
#     "timestamp"  : get_authored_datetime(commit),
#     "msg"        : get_commit_message(commit),
#   }
  
#   return commit_info


def get_changed_files_name(files_info):
  ret = []
  for file_info in files_info:
    ret.append(file_info["filename"])

  return ret

# EOF
