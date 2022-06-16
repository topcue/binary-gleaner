from util import *
from commit_util import *
from info import *
from packageHandler import *
# from commitHandler import *
# from builder import *

package = ""

def show_menu():
  print("[*] Menu:")
  print("  (1) Show supported packages")
  print("  (2) Select package")
  print("  (3) Collect dataset(including binary-pairs)")

def show_packages():
  print(PACKAGES, "\n")

def select_package():
  print("[*] input package name: ")
  input_pkg = input()
  if input_pkg in PACKAGES:
    global package
    package = input_pkg
  else:
    exit(0)

def is_valid_package():
  return package in PACKAGES

def foo():
  pkg_hdl = PackageHandler(package, "pure_base", "base")
  pkg_hdl.init_repo()
  pkg_hdl.collect_dataset()

def main():
  # ## TODO: Remove me
  # global package
  # package = "binutils"
  # foo()

  while(True):
    show_menu()
    
    input_num = int(input())
    if input_num == 1:
      show_packages()
    elif input_num == 2:
      select_package()
    elif input_num == 3:
      if is_valid_package():
        foo()
      else:
        exit()


if __name__ == "__main__":
  main()


# EOF
