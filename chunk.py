from util import *
from commit_util import *
from difflib import *

def get_chunk_size(chunks):
  if (len(chunks) == 0):
    return 0
  sz = 0
  chunks = chunks[1:]
  # find next chunks header
  while(len(chunks) > 0):
    if(chunks[0][:2] == "@@"):
      break
    sz = sz + 1
    chunks = chunks[1:]
  return sz


def parse_chunk_info(data):
  chunk_info = {}
  data = data.split(' ')
  assert(data[0] == data[3] == "@@")
  line_A = data[1].split(',')
  line_B = data[2].split(',')
  
  chunk_info["start_A"] = int(line_A[0].replace('-', ''))
  chunk_info["offset_A"] = int(line_A[1]) if (len(line_A) > 1)  else -1
  chunk_info["start_B"] = int(line_B[0].replace('+', ''))
  chunk_info["offset_B"] = int(line_B[1]) if (len(line_B) > 1)  else -1
  chunk_info["func_sig"] = " ".join(data[4:])
  
  return chunk_info


def get_diff_tag(ch):
  if ch == '+':
    return 'a'
  elif ch == '-':
    return 'd'
  else:
    return 'e'


## Not needed yet.
def parse_chunk_body(chunks):
  lines = []
  tags = []
  for line in chunks:
    tag = get_diff_tag(line[0])
    tags.append(tag)
    lines.append(line[1:])
  
  return [lines, tags]


def parse_chunks(data):
  chunks_data = []
  while(len(data) > 0):
    sz = get_chunk_size(data)
    header = parse_chunk_info(data[0])
    # body = parse_chunk_body(chunks[1:sz+1])
    body = []
    chunks_data.append({"header":header, "body":body})
    data = data[sz+1:]
  
  return chunks_data


def parse_delta(delta):
  delta = delta.split('\n')

  if (len(delta) < 4):
    ## binary files
    return None
  elif(delta[4][:2] == "@@"):
    targets_info, metadata = delta[0], delta[1]
    old_file, new_file = delta[2], delta[3]
    chunks_data = parse_chunks(delta[4:])
  else:
    ## Such as deleted files, num of header line can be different.
    targets_info, msg, metadata = delta[0], delta[1], delta[2]
    old_file, new_file = delta[3], delta[4]  
    chunks_data = parse_chunks(delta[5:])
  
  return chunks_data


def build_index_A(A):
  dic_A, index_A = {}, []
  cnt = 1
  for line in A:
    if line in dic_A:
      num = dic_A[line]
      index_A.append(str(num))
    else:
      dic_A[line] = str(cnt)
      index_A.append(str(cnt))
      cnt += 1

  return index_A, dic_A


def build_index_B(B, dic_A):
  index_B = []
  cnt = len(dic_A) + 1
  for line in B:
    if line in dic_A:
      num = dic_A[line]
      index_B.append(num)
    else:
      index_B.append(str(cnt))
      cnt += 1
  return index_B


def build_index(A, B):
  index_A, dic_A = build_index_A(A)
  index_B = build_index_B(B, dic_A)

  ## diff
  datas = list(unified_diff(index_A, index_B))[3:]
  # print_json(datas)

  # p1 = ["1", "1", "1"]
  # p1 = "".join(['[' + sub + ']' for sub in p1])
  
  # for i in range(0, len(index_A) - len(p1) + 1):
  #   tmp_index, _ = build_index_A(index_A[i:])
  #   tmp = "".join(['[' + sub + ']' for sub in tmp_index])
  #   if(p1 in tmp):
  #     print_json(A)
  #     input()
  #     break

  return index_A, index_B


# comb = list(combinations(pat, 2))
# v = []
# for item in comb:
#   if item[0] == item[1]:
#     v.append(True)
#   else:
#     v.append(False)
# print(v)

def valid(l):
  ## pat: "ABA"
  if not(l[0] != l[1]):
    return False
  if not(l[0] == l[2]):
    return False
  return True

from itertools import combinations

def build_histogram(A, B):
  try:
    if(len(A) < 1 or len(B) < 1): return
    # A = "l m n o x z y z x x y x z o z l x y".split(" ")
    # B = "l m n o x y z y x z y l x y".split(" ")
    index_A, _ = build_index(A, B)

    # pat = "12331"
    # pat2 = "132"
    pat = "121"
    pat2 = "212"
    l = index_A
    for i in range(0, len(l) - len(pat) + 1):
      tmp_index, _ = build_index_A(l[i:])
      tmp_index = [ "[" + ch + "]" for ch in tmp_index]
      tmp_index = "".join(tmp_index)

      tmp_pat = [ "[" + ch + "]" for ch in pat]
      tmp_pat = "".join(tmp_pat)

      if tmp_pat in tmp_index:
        ## build d(symbolic pat -> concrete pat2)
        idx = tmp_index.find(tmp_pat)
        index = A[idx + i:]
        d = {}
        for j in range(0, len(pat)):
          if pat[j] not in d:
            d[pat[j]] = index[j]
        
        con = []
        for p in pat2:
          con.append(d[p])
        
        tmp_con = [ "[" + ch + "]" for ch in con]
        tmp_con = "".join(tmp_con)

        tmp_B = [ "[" + ch + "]" for ch in B]
        tmp_B = "".join(tmp_B)

        if tmp_con in tmp_B:
          print("[*] found!")
          print_json(A)
          print_json(B)
          input()
  except:
    print("except")   
    # v = valid(tmp_index)
    # if v:
    #   p1 = A[i]
    #   p2 = A[i+1]
    #   p3 = A[i+2]
    #   assert p1 == p3
    #   for j in range(0, len(B) - 3 + 1):
    #     if (B[j] == B[j + 2] == p2) and (B[j + 1] == p1):
    #       print_json(A)
    #       print_json(B)
    #       print("[*] found!")
    #       input()
    #       i = len(l) - len(pat) + 1
    #       break

  pass


def build_histogram2(A, B):
  index_A, _ = build_index(A, B)

  pat = "ABA"
  l = index_A
  for i in range(0, len(l) - len(pat) + 1):
    tmp_index, _ = build_index_A(l[i:])
    v = valid(tmp_index)
    if v:
      p1 = A[i]
      p2 = A[i+1]
      p3 = A[i+2]
      assert p1 == p3
      for j in range(0, len(B) - 3 + 1):
        if (B[j] == B[j + 2] == p2) and (B[j + 1] == p1):
          print_json(A)
          print_json(B)
          print("[*] found!")
          input()
          i = len(l) - len(pat) + 1
          break

  pass

def pattern_mathcing(currComm: Commit, prevComm: Commit, repo: Repo):
  diffs = prevComm.diff(currComm)

  for diff in diffs:
    if diffType(diff) != 'M':
      continue

    pathA = diff.a_blob.path if diff.a_blob else None
    pathB = diff.b_blob.path if diff.b_blob else None
    
    if not pathA or not pathB:
      continue
    
    assert pathA == pathB

    path = pathA

    
    try:
      delta = repo.git.diff(prevComm, currComm, path)
    except:
      print("[-] repo.git.diff() Error!")
      return
    
    chunks_data = parse_delta(delta)
    if not chunks_data:
      return
    file_data_A = repo.git.show('{}:{}'.format(prevComm.hexsha, path))
    file_data_B = repo.git.show('{}:{}'.format(currComm.hexsha, path))

    try:
      for chunk in chunks_data:
        start_A = chunk["header"]["start_A"]
        offset_A = chunk["header"]["offset_A"]
        start_B = chunk["header"]["start_B"]
        offset_B = chunk["header"]["offset_B"]

        data_A = file_data_A.split("\n")[start_A - 1 : start_A + offset_A - 1]
        data_B = file_data_B.split("\n")[start_B - 1 : start_B + offset_B - 1]

        build_histogram(data_A, data_B)
        
    except UnicodeEncodeError:
      print("[-] UnicodeEncodeError!")

  pass


# EOF
