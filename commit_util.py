from util import *

def get_commit_hash(commit):
  return commit.hexsha

def get_commit_parent(commit):
  return commit.parents[0] if commit.parents else EMPTY_TREE_SHA

def get_committer(commit):
  return commit.committer

def get_committed_date(commit):
  return commit.committed_date

def get_committed_datetime(commit):
  return commit.committed_datetime.strftime(DATETIME_FORMAT)

def get_authored_datetime(commit):
  return commit.authored_datetime.strftime(DATETIME_FORMAT)

def get_commit_message(commit):
  return commit.message

def get_all_commits(repo):
  return list(repo.iter_commits('master'))

def get_commits_with_cnt(repo, cnt):
  return list(repo.iter_commits('master', max_count=cnt, skip=0)) 

def get_commits_with_datetime_range(commits, start, end):
  start_datetime = start.strftime(DATETIME_FORMAT)
  end_datetime = end.strftime(DATETIME_FORMAT)
  result = []
  for commit in commits:
    authored_datetime = get_authored_datetime(commit)
    if start_datetime < authored_datetime < end_datetime:
      result.append(commit)
  
  return result

def diff_type(diff: Diff):
  if diff.renamed: return 'Renamed'
  if diff.deleted_file: return 'Deleted'
  if diff.new_file: return 'Added'
  return 'Modified'

def get_diff_files(diff: Diff):
  fileA = diff.a_blob.data_stream.read().decode('utf-8')
  fileB = diff.b_blob.data_stream.read().decode('utf-8')
  return fileA, fileB

def get_files_info(commit: Commit):
  parent = commit.parents[0] if commit.parents else EMPTY_TREE_SHA
  diffs  = {
    diff.a_path: diff for diff in commit.diff(parent)    
  }

  files_info = []
  for objpath, stats in commit.stats.files.items(): 
    diff = diffs.get(objpath)
    if not diff:
      for diff in diffs.values():
        if diff.renamed:
          break
    files_info.append({
      'filename': objpath,
      'type': diff_type(diff),
      'stats' : stats,
    })
  
  return files_info

def test():
  ## config path params
  home_path = "/Users/topcue"
  project_path = home_path + "/binary-gleaner"
  base_path = "/Users/topcue/binary-gleaner/base"
  
  ## creat base dir
  binutils_url = get_git_repo_url_with_package_name("binutils")
  base_repo = create_base(binutils_url, base_path)
  print("[*] Base repo status:", get_status(base_repo, base_path))
  print()
  
  ## create test dir
  test_path = project_path + "/test"
  test_repo = try_clone_repo(base_path, test_path)
  repo = test_repo

  ## get commits
  commits = get_commits_with_cnt(repo, 15000)

  start_datetime = datetime.datetime(2021, 1, 1)
  end_datetime = datetime.datetime.now()
  commits = get_commits_with_datetime_range(commits, start_datetime, end_datetime)
  
if __name__ == "__main__":
  test()

# EOF
