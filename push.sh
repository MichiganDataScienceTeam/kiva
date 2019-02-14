#!/bin/bash

# Run this to push your analysis to github
if [[ "$(git branch | grep \* | cut -d ' ' -f2)" == "master" ]];
then
    echo "You're on master. Run git checkout <branch_name> to switch to your own branch"
    exit 1
fi

read -p "Do you want to add everything? (y/N)" push_all

if [[ "$push_all" == "y" ]];
then
    #statements
    git add analysis/
else
    echo "'git add' the files you'd like to commit, then run this script again"
fi

if git diff --name-only --cached | grep "^visualizations/" ||
   git diff --name-only --cached | grep "^code/";
then
    echo "You have staged files from the visualizations/ or code/ directories."
    echo "Unstage these files or make a pull request with pr.sh"
    exit 1
fi

git commit

git push -u origin $(git branch | grep \* | cut -d ' ' -f2)
