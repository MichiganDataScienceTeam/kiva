#!/bin/bash

# Run this to push to master
if [[ "$(git branch | grep \* | cut -d ' ' -f2)" == "master" ]];
then
    echo "You're on master. Run git checkout <branch_name> to switch to your own branch"
    exit 1
fi

read -p "Have you git added everything you want in the commit? (y/N)" push_all

if [[ "$push_all" == "y" ]];
then
    echo "'git add' the files you'd like to commit, then run this script again"
    exit 0
fi

if git diff --name-only --cached | grep "^analysis/"
then
    echo "You have staged files from the analysis/ directory."
    echo "Did you mean to run push.sh? Otherwise, unstage these files and try again."
    exit 1
fi

read -p "What do you want to call your PR (no spaces)? " pr_name

git commit

branch="$(git branch | grep \* | cut -d ' ' -f2)"

git fetch --all
git checkout -b $pr_name origin/master || echo "PR Name Already Exists" && exit
git cherry-pick $branch
git push -u origin $pr_name
git checkout -b $branch
git push origin $branch
