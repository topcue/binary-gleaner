from xml.etree.ElementTree import Element, SubElement, ElementTree

from util import *

def _pretty_print(current, parent=None, index=-1, depth=0):
  for i, node in enumerate(current):
    _pretty_print(node, current, i, depth + 1)
  if parent is not None:
    if index == 0:
      parent.text = '\n' + ('\t' * depth)
    else:
      parent[index - 1].tail = '\n' + ('\t' * depth)
    if index == len(parent) - 1:
      current.tail = '\n' + ('\t' * (depth - 1))


def store_xml(root, path):
  _pretty_print(root)
  tree = ElementTree(root)
  with open(path, "wb") as file:
    tree.write(file, encoding='utf-8', xml_declaration=True)


def build_xml_commit_info(root, curr_comm:Commit, prev_comm:Commit, files_info):
  e_commit = Element("Commit")
  root.append(e_commit)

  e_hexsha = SubElement(e_commit, "hexsha")
  e_hexsha.text = curr_comm.hexsha

  e_parent = SubElement(e_commit, "parent")
  e_parent.text = prev_comm.hexsha

  e_datetime = SubElement(e_commit, "committed_datetime")
  e_datetime.text = str(curr_comm.committed_datetime)

  e_num_files = SubElement(e_commit, "num_files")
  e_num_files.text = str(len(files_info))

  e_files = Element("diff_files")
  e_commit.append(e_files)

  for file_info in files_info:
    e_file = SubElement(e_files, "file")
    e_file.text = file_info["path"]
  
  e_commit_message = SubElement(e_commit, "message")
  # e_commit_message.text = curr_comm.message

  return root


def build_xml_files_info(root, repo, curr_comm:Commit, prev_comm:Commit, files_info):
  e_files = Element("Files")
  root.append(e_files)

  for file_info in files_info:
    e_file = Element("File")
    e_files.append(e_file)

    e_path = SubElement(e_file, "path")
    e_path.text = file_info["path"]

    e_type = SubElement(e_file, "type")
    e_type.text = file_info["type"]

    ## stats
    e_stats = Element("stats")
    e_file.append(e_stats)

    e_i = SubElement(e_stats, "insertions")
    e_i.text = str(file_info["stats"]["insertions"])
    e_d = SubElement(e_stats, "deletions")
    e_d.text = str(file_info["stats"]["deletions"])
    e_l = SubElement(e_stats, "lines")
    e_l.text = str(file_info["stats"]["lines"])
    
    if file_info["type"] == "M":
      e_curr_contents = SubElement(e_file, "curr_contents")
      e_curr_contents.text = repo.git.show("{}:{}".format(curr_comm.hexsha, file_info["path"]))
    
      e_prev_contents = SubElement(e_file, "prev_contents")
      e_prev_contents.text = repo.git.show("{}:{}".format(prev_comm.hexsha, file_info["path"]))
  
  return root
  

def build_xml_info(repo, curr_comm:Commit, prev_comm:Commit, files_info):
  root = Element("Info")
  root = build_xml_commit_info(root, curr_comm, prev_comm, files_info)
  root = build_xml_files_info(root, repo, curr_comm, prev_comm, files_info)
  
  return root


# EOF
