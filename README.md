

# Staff Scheduling
Restaurant staff scheduling website

* [How to work in the codebase](#how-to-work-in-the-codebase)
  * [Get the latest source](#get-the-latest-source)
  * [Modify the source](#modify-the-source)
    * [Interface](#interface)
    * [Logic](#logic)
    * [Data Model](#data-model)
  * [Check your changes](#check-your-changes)
  * [Run the code](#run-the-code)
  * [Submit the code](#submit-the-code)
    * [Create a new source branch](#create-a-new-source-branch)
    * [Review your changes](#review-your-changes)
    * [Commit your changes](#commit-your-changes)
    * [Push your changes](#push-your-changes)
    * [Merge changes from main branch](#merge-changes-from-main-branch)
  * [Create a Pull Request](#create-a-pull-request)
  * [Get ready for the next change](#get-ready-for-the-next-change)

# How to work in the codebase

Assuming the source has been cloned to ~/Documents/scheduling (on cbook is has been).

`cd ~/Documents/scheduling`

## Get the latest source

`git pull`

## Modify the source

### Interface
The interface is stored in `src/ui` and `src/ui/template` (mainly).
These are just web pages, but have special markup to insert variables and have some basic logic.

### Logic
The logic behind the interface is stored in `src/scheduling.py`. 
This has the logic to perform when the interface makes a request.

### Data Model
The data model is stored in `src/model.py`.
This manages the database.
In general, you get objects or create objects.
If you modify an object you get back, you must call `flush()` on the model (`database.flush()`) before returning the webpage.
You only have to call `flush()` once, even for multiple changes to multiple objects.

## Check your changes

Make sure all files are saved to disk.

`./pr_build.sh fix`

This will reformat your code, and run some checks on it. 
If any of the checks fail, you must address these problems before submitting.

## Run the code

`./pr_build.sh run`

This will check the changes again, and start the web server (on port `8000`).
You can try out your changes by going to http://localhost:8000/

You can make changes while the web server is running and as long as you don't have invalid Python, the server will update to your changes live.
This allows you to make changes and refresh the page and see the changes.

## Submit the code

First, verify that your changes are still valid.

`./pr_build.sh fix`

### Create a new source branch

`git checkout -b users/my_name/meaningful_change_name`

### Review your changes

`git diff`

Review the changes you have made and look for things you missed.

### Commit your changes

`git commit -a`

Press `i` to start inserting text into the description.
Put the full description of your changes (which you reviewed in the last step).
When you are done, press `esc` then type `:wq` and press `return`.

### Push your changes

`git push`

The first time you `push` you will need to connect your branch upstream. 
Don't worry, git will helpfully give you the full command, which will be something like:

`git push --set-upstream origin users/my_name/meaningful_change_name`

Any changes you make to this branch after this point will just need `git commit -a` and `git push`.

### Merge changes from main branch

If there have been changes added to the `main` branch since your branch was created, you will need to merge those changes back into your branch.

`git checkout main` \
`git pull` \
`git checkout my_name/meaningful_change_name` \
`git merge main` 

If there were any changes in `main` that conflicted with your changes, they will be marked with HEAD and will show both changes in the same file.
Search through your files for HEAD.
Fix the conflicts by choosing from `main`, your branch, or rewrite the code to include both changes.

`git commit -a`

You can just leave the merge comment and type `:wq` and press `return`.

## Create a Pull Request

Changes go into `main` from your branch through a pull request.
This allows review of the code to get another set of eyes on it.

Go to https://github.com/marcpage/scheduling/pulls

There should be a green button that says `Compare & Pull Request`.

<img width="553" alt="Screen Shot 2021-12-30 at 11 42 43 AM" src="https://user-images.githubusercontent.com/695749/147775951-2554acf3-cbb6-480f-ba6e-d46ec23f0985.png">

After the pull request is created, respond to comments, fix anything needed. 
Changes can be made, and then you can `commit` and `push` (see above) to update your branch.
Once everything is good, you can complete the pull request (green `Squash and merge` button near the bottom).

<img width="553" alt="Screen Shot 2021-12-30 at 11 45 48 AM" src="https://user-images.githubusercontent.com/695749/147775964-eb40d818-8ce0-4cb8-b31f-2191726616e8.png">

The confirm the completion by pressing the green `Confirm squash and merge` button.

<img width="562" alt="Screen Shot 2021-12-30 at 11 45 55 AM" src="https://user-images.githubusercontent.com/695749/147775991-a890c1aa-8d2f-4243-8663-97e514f5f8b1.png">

## Get ready for the next change

After the pull request is complete, `main` now has newer source than you have on your machine.

`git checkout main` \
`git pull`

You can now go back to the `modify source` step above.


