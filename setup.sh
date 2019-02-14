#!/bin/bash

# You should run this script once to get started

git stash
git pull
read -p "Enter branch name: " branch_name
git checkout -b $branch_name || git checkout $branch_name
