#!/bin/bash

echo "[*] glean_binar_pair.sh info"
echo "  [*] BIN_PATH:" $BIN_PATH

if ls $BIN_PATH/parent_tmp 1> /dev/null 2>&1; then
  mkdir -p $BIN_PATH/parent
  mkdir -p $BIN_PATH/child
  for file in `ls $BIN_PATH/parent_tmp $1`; do
    hash_parent=`md5sum $BIN_PATH/parent_tmp/$file $1 | awk '{print $1}'`
    hash_child=`md5sum $BIN_PATH/child_tmp/$file $1 | awk '{print $1}'`
    if test $hash_parent != $hash_child; then
      cp $BIN_PATH/parent_tmp/$file $BIN_PATH/parent
      cp $BIN_PATH/child_tmp/$file $BIN_PATH/child
    fi
  done
  # rm -rf $BIN_PATH/parent_tmp
  # rm -rf $BIN_PATH/child_tmp
fi

# EOF
