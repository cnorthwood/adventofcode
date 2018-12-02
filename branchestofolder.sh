#!/bin/sh

for branch in `git branch | grep -v master`; do
    git checkout $branch
    git filter-branch -f --tree-filter "mkdir -p $branch && find . -mindepth 1 -maxdepth 1 ! -name $branch -exec mv {} $branch \;" HEAD
    git checkout master
    git rebase $branch
    git branch -D $branch
    git push origin :$branch
done
