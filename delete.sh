#!/bin/bash

ORG_NAME="reL4team2"

# 获取组织下的所有仓库
repos=$(gh repo list $ORG_NAME --json name -q '.[].name')

gh auth refresh -h github.com -s delete_repo

for repo in $repos; do
  echo "Deleting repository: $ORG_NAME/$repo"
  gh repo delete $ORG_NAME/$repo --yes
done