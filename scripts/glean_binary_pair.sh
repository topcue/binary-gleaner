#!/bin/bash

echo "[*] glean_binar_pair.sh info"
echo "  [*] BIN_PATH:" $BIN_PATH

if ls $BIN_PATH/tmp_parent 1> /dev/null 2>&1; then
  mkdir -p $BIN_PATH/parent
  mkdir -p $BIN_PATH/patched
  for file in `find $BIN_PATH/tmp_parent -type f -printf '%P\n' $1`; do
    parent_hash=`md5sum $BIN_PATH/tmp_parent/$file $1 | awk '{print $1}'`
    patched_hash=`md5sum $BIN_PATH/tmp_patched/$file $1 | awk '{print $1}'`
    if test $parent_hash != $patched_hash; then
      ## parent
      src=$BIN_PATH/tmp_parent/$file
      dst=$BIN_PATH/parent/$file
      path=`dirname "$dst"`
      if [ ! -d "$path" ]; then
        mkdir -p "$path"
      fi
      cp -R "$src" "$path"

      ## patched
      src=$BIN_PATH/tmp_patched/$file
      dst=$BIN_PATH/patched/$file
      path=`dirname "$dst"`
      if [ ! -d "$path" ]; then
        mkdir -p "$path"
      fi
      cp -R "$src" "$path"
    fi
  done
  rm -rf $BIN_PATH/tmp_parent
  rm -rf $BIN_PATH/tmp_patched
fi

# EOF
