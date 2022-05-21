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

def get_changed_files_name(files_info):
  ret = []
  for file_info in files_info:
    ret.append(file_info["filename"])

  return ret

# EOF
