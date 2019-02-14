# Kiva Dataset

https://www.kaggle.com/kiva/data-science-for-good-kiva-crowdfunding

# Contributing

## tl;dr (the magic version)**
make sure you have push permissions to the repository (message naitian
if you're not sure)

To set up (only do this once):
- `git clone https://github.com/MichiganDataScienceTeam/kiva`
- `./setup.sh`

To version control your own code, run:
- `git add <files you want to commit>`
- `./push.sh`

To make a pull request to `master`, run:
- `git add <files you want to commit>`
- `./pr.sh`

## Under the hood version
**Clone the github repository**

`git clone https://github.com/MichiganDataScienceTeam/kiva`

**Create your own branch**

`git checkout -b <branch name>`

**Do your data science** in the `analysis/` directory
You can use Python, R, Microsoft Excel, anything you want.
Just try to commit frequently and

**Push your branch to Github**

`git push -u origin <branch name>`

**Pushing things to master**
If you generate any visualizations, insights, or useful code,
put those in the appropriate `visualizations/` or `code/`
directories, then commit *only* those directories and make a pull
request to the `master` branch.

e.g.
```
git add visualizations/
git commit

git fetch --all
git checkout -b <pull request name> upstream/master
git cherry-pick <hash of the most recent commit (e.g. b50b2e7)>
git push -u origin <pull request name>
```

Then make a pull request from the `<pull request name>` branch.

The idea here is that, with a little bit of overhead, we can keep
everyone's personal workflows relatively intact, while still sharing
the important things.
