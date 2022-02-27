from util import *

def store_new_commit(file_path, commit_overview):
  is_exist = os.path.isfile(file_path)
  if not is_exist:
    print("[+] Not exist. Store commit.")
    commit = read_json_from_url_with_token(commit_overview["url"])
    store_json(file_path, commit)

def update_commit_pool():
  # get url
  binutils_url = get_git_commit_url_with_package_name("binutils")
  
  # set page range manually
  page_range = {
    "start" : 1,
    "end"   : 10
  }
  
  for page_num in range(page_range["start"], page_range["end"]):
    # get url w/ pages num
    page_url = add_commit_url_to_page(binutils_url, page_num)
    print("[*] page_url:", page_url)
    
    # get page's data (30 commit overviews per page)
    page_data = read_json_from_url_with_token(page_url)
    
    for commit_num in range(commit_per_page):
      commit_overview = page_data[commit_num]
      sha = commit_overview["sha"]
      date = commit_overview["commit"]["committer"]["date"].replace('-', '').replace(':', '')
      file_path = "./commits/commit-" + date + '-' + str(sha)
      store_new_commit(file_path, commit_overview)
    
if __name__ == "__main__":
  update_commit_pool()

# EOF
