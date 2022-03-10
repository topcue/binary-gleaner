#!/bin/bash

echo "[*] build_binar_pair.sh info"
echo "  [*] PARENT_HASH:" $PARENT_HASH
echo "  [*] PATCHED_HASH :" $PATCHED_HASH
echo "  [*] BASE_PATH  :" $BASE_PATH
echo "  [*] BIN_PATH   :" $BIN_PATH
echo "  [*] CONFIG_OPT :" $CONFIG_OPT

mkdir -p $BIN_PATH

cd $BASE_PATH && git checkout $PARENT_HASH -q
rm -rf $BASE_PATH/build && mkdir -p $BASE_PATH/build
rm -rf $BASE_PATH/install && mkdir -p $BASE_PATH/install
cd $BASE_PATH/build && $BASE_PATH/configure $CONFIG_OPT -q 2>/dev/null
cd $BASE_PATH/build && make -j 8 >/dev/null 2>&1 && make install >/dev/null
cp -r $BASE_PATH/install $BIN_PATH/tmp_parent

cd $BASE_PATH && git checkout $PATCHED_HASH -q
rm -rf $BASE_PATH/install && mkdir -p $BASE_PATH/install
cd $BASE_PATH/build && make -j 8 >/dev/null 2>&1 && make install >/dev/null
cp -r $BASE_PATH/install $BIN_PATH/tmp_patched

# EOF
