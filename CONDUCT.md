Contributor Code of Conduct
================

As maintainers of this project we are committed to respecting the ideas and opinions of others and fostering an open and welcoming environment for everyone interested in participating in this project.

We are committed to making participation in this project a harassment-free experience for everyone, regardless of level of experience, gender, gender identity and expression, sexual orientation, disability, personal appearance, body size, race, ethnicity, age, or religion.

Examples of unacceptable behaviour by participants include the use of sexual language or imagery, derogatory comments or personal attacks, trolling, public or private harassment, insults, or other unprofessional conduct.

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, issues, and other contributions that are not aligned to this Code of Conduct. Project maintainers who do not follow the Code of Conduct may be removed from the project team.

Instances of abusive, harassing, or otherwise unacceptable behaviour may be reported by opening an issue.


# Contributing

### How to Contribute
This project will be managed using Git branching. Branches will be task oriented and deleted as soon as the task is completed.

#### How to Create, Push and Delete Branches

1. Clone the master repository to your computer locally `git clone <master_repo_URL>`
2. Create task/feature branch of the master repository on Bash/Terminal `git branch <feature_branch_name>`
3. Link the local and remote branch `git push -u origin <feature_branch_name>`
4. Switch *head* to the branch `git checkout <feature_branch_name>`
5. Work on the local repository and git add and commit the changes to the repository with `git add <file_name>` and `git commit -m"<commit_message>"`
6. Then push the changes to the GitHub repository with `git push`
7. Create and send a pull request from the branch to master (see Pull Request section for more details on messages, reviews and accepting)
8. Once all work has been completed on the branch, please delete the branch after the last pull request has been merged. There are three parts of a branch that need to be deleted.
    -  One team member needs to delete the remote branch. It can be deleted by hitting the garbage/trash bin button next to the branch name on the GitHub branch tab or in Bash/Terminal with the command `git push origin --delete <feature_branch_name>`
    - Each team member will have to delete their own local branch by `git branch -d <feature_branch_name>`
    - Each team member will have to prune the local remote connection with the command `git remote prune origin`

To check your local branches `git branch -vv`   
To check all your branches `git branch -a`


#### How to Update your Branch

When your branch is behind do `git pull` to catch up.

If you need to catch your branch up to the master:
 - switch to your master branch `git checkout master` and update `git pull`
 - then switch to your feature branch and combine with master `git merge master`

If all else fails try `git pull` & `git push` from the feature and master branch until it matches.

When the error message "upstaged changes" occurs and you don't have any changes you want to push, here are two methods to discard the local difference:
 - `git stash` will "stash" your changes and they can be restored
     - see all your stashed changes `git stash list`
     - restore your changes `git stash pop`
     - remove them completely `git stash drop`.
 - `git reset --hard` will reset all of your changes to the previous commit


### Communication

To ensure open and transparent communication, team members will use issues to convey messages about action items, deadlines, meeting agendas, resources, bugs and any other relevant items. For more general communication such as organizing meetings our Slack channel will be used.

When there are task-oriented issues, before working on the task add a comment assigning the task to yourself. If you see a bug or typo either create an issue so the team member responsible for the file is aware or fix the issue yourself and send a pull request.


### Commit Messages
When adding new files or making changes to existing files, write simple and descriptive commit messages. For readability have:
- one commit message per task
- the title of the file (add the purpose if the title is not a good description)
- the changes in the file is being updated

### Pull Request Messages & Reviews
Once a pull request has been created assign the other team members as reviewers. Any team member can accept a pull request, ie either the creator or team members.
- Major/critical/final updates should have two other team members approval or reviews before the pull request is accepted
   - due to schedules or deadlines this can be waved
- Smaller administrative tasks (ie. changing folder names) can be accepted without other team members review

*Reminder do not push .Rhistory or .ipynb check points*
<br>


### Project Organization
This project will follow the project structure adopted from [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/). Raw data should never be pushed to GitHub due to privacy concerns and this folder is listed in the .gitignore file.

Notebooks and scrips should be named appropriately so the purpose can be clearly understood, naming conventions may be created for consistency. Reports should not be named "final" or similar terms as only the final version should be present and GitHub should be used for version control. Notebooks are for experiments which includes both Jupyter Notebooks and .Rmd files, due to version control issue Jupyer Notebook will be used for individual work instead of collaboration.

If you are unsure of where your file should be stored consult with the team. Large organization changes should be discussed between the team before implemented. Try to structure your code in modules and call those functions within your notebook.


### Outside & Future Contributors
This repository has been created for a course project and may not be monitored after the course. If you would like to comment or ask questions about the analysis, post an issue and one of the contributors may respond.




This Code of Conduct is adapted from the [Contributor Covenant](http:contributor-covenant.org), [version 1.0.0](http://contributor-covenant.org/version/1/0/0/).
