#!/bin/bash

echo "[*] build_binar_pair.sh info"
echo "  [*] PARENT_HASH:" $PARENT_HASH
echo "  [*] CHILD_HASH: " $CHILD_HASH
echo "  [*] BASE_PATH:  " $BASE_PATH
echo "  [*] BIN_PATH:   " $BIN_PATH
echo "  [*] CONFIG_OPT: " $CONFIG_OPT

mkdir -p $BIN_PATH

cd $BASE_PATH && git checkout $PARENT_HASH -q
rm -rf $BASE_PATH/build && mkdir -p $BASE_PATH/build/pre
cd $BASE_PATH/build && $BASE_PATH/configure $CONFIG_OPT 2>/dev/null
cd $BASE_PATH/build && make -j 8 >> make.log 2>&1 && make install >/dev/null
cp -r $BASE_PATH/build/make.log $BIN_PATH/parent_make.log
cp -r $BASE_PATH/build/pre/bin $BIN_PATH/parent_tmp

cd $BASE_PATH && git checkout $CHILD_HASH -q
cd $BASE_PATH/build && make -j 8 >> make.log 2>&1 && make install >/dev/null
cp -r $BASE_PATH/build/make.log $BIN_PATH/child_make.log
cp -r $BASE_PATH/build/pre/bin $BIN_PATH/child_tmp

# EOF
