#!/bin/bash

# 引数が指定されていない場合、エラーメッセージを表示して終了
if [ $# -eq 0 ]; then
  echo "Usage: $0 <source_file1.cpp> <source_file2.cpp> ..."
  exit 1
fi

# ビルドディレクトリが存在しない場合、作成
build_dir="./build"
mkdir -p "$build_dir"

# 引数で指定されたすべてのソースファイルをビルド
g++ -I/usr/include/opencv4 "$@" -std=c++17 -o "$build_dir/output" -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_imgproc -lopencv_videoio

# 実行可能ファイルを実行
"$build_dir/output"

