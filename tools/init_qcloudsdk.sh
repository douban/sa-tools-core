#!/bin/bash

set -xe

project_root="$(cd "${0%/*}"; cd ..; pwd)"

mkdir -p tmp
cd tmp
if [[ ! -d qcloudcli ]]; then
  git clone https://github.com/douban/qcloudcli.git
fi
cd qcloudcli
git remote add douban-ghe https://github.com/douban/qcloudcli.git
git fetch douban-ghe douban
git checkout -b douban douban-ghe/douban
git pull douban-ghe douban

cd $project_root

rsync -a tmp/qcloudcli/qcloudsdk{bm*,cvm} sa_tools_core/libs/qcloud/
for i in `ack -l 'from qcloudsdkcore.request import Request' app/libs/qcloud/`; do
  sed -i 's|from qcloudsdkcore\.request import Request|from ..qcloudsdkcore.request import Request|' "$i"
done

for i in sa_tools_core/libs/qcloud/qcloudsdk{bm*,cvm}; do
  echo "from . import (`ls "$i"/*.py | sed -nr 's|.*\/(.*Request)\.py|\1|p' | tr '\n' ','`)" >> "$i"/__init__.py
done
