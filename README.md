
![example workflow](https://github.com/marcpage/scheduling/actions/workflows/CI.yml/badge.svg)

# Staff Scheduling
Restaurant staff scheduling website

The goal is to have a website that can be deployed to an Amazon Elastic Cloud instance and would support multiple restaurants.
This will facilitate the communication of schedule between employees and managers.

Restaurant turn-over is a huge challenge to establishing standard practices in scheduling. 
* Wouldn't it be great as a restaurant employee if there was a standard way to communicate when you want to work, when you could work, when you'd rather not work, and when you cannot work? 
* Wouldn't it be great as a schedule manager or general manager if you could have a system that takes employee input, your input and automatically creates a starting point for the schedule for each week?
* Wouldn't it be great as an employee if you had to have someone cover you you could have a list of employees ranked from those who would most like to work that shift to least like to work that shift?

Oh, and I am using this project to help family members get experience in coding in python with a project that has commercial value.

# Contents

* [Why is this public domain](#why-is-this-public-domain)
* [How to work in the codebase](#how-to-work-in-the-codebase)
  * [Get the latest source](#get-the-latest-source)
  * [Modify the source](#modify-the-source)
    * [Interface](#interface)
    * [Logic](#logic)
    * [Data Model](#data-model)
  * [Check your changes](#check-your-changes)
  * [Run the code](#run-the-code)
    * [Boot-strap process](#boot-strap-process)
  * [Submit the code](#submit-the-code)
    * [Create a new source branch](#create-a-new-source-branch)
    * [Review your changes](#review-your-changes)
    * [Commit your changes](#commit-your-changes)
    * [Push your changes](#push-your-changes)
    * [Merge changes from main branch](#merge-changes-from-main-branch)
  * [Create a Pull Request](#create-a-pull-request)
  * [Get ready for the next change](#get-ready-for-the-next-change)
  * [Working on Windows](#working-on-windows)

# Why is this public domain

`If this fills such a valuable need for restaurants, why are you putting the source in the public domain?`

I believe that those who have the technical skills to implement this for their restaurant can save themselves a lot of time and money.
For those other restaurants that do not have those with the skills to deploy this, enterprising people with the skills can sell this solution to them.
I feel there is a great need in society for this tool. 
If I try to sell it by myself, I may make a lot of money but I will not be able to fulfill the need as effectively as several people going out and filling that need.

If you wish to sell your services to set this up for a restaurant or even for several restaurants, please do.
If you receive feedback, please contribute it back here, but most of all, fill the need.

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

`./pr_build.sh fix` (Note: pr_build.sh has only been tested on macOS and Ubuntu)

This will reformat your code, and run some checks on it. 
If any of the checks fail, you must address these problems before submitting.

## Run the code

`./pr_build.sh run` (Note: pr_build.sh has only been tested on macOS and Ubuntu)

This will check the changes again, and start the web server (on port `8000`).
You can try out your changes by going to http://localhost:8000/

You can make changes while the web server is running and as long as you don't have invalid Python, the server will update to your changes live.
This allows you to make changes and refresh the page and see the changes.

### Boot-strap process

The first step in the boot-strap process is to create an admin account. 
The first user to log in creates an admin account.

<kbd><img width="438" alt="Screen Shot 2021-12-30 at 10 00 13 PM" src="https://user-images.githubusercontent.com/695749/147803534-921b7948-d016-4075-918c-6e140514784b.png"></kbd>

Once the admin account is created, the admin can create a restaurant.

<kbd><img width="265" alt="Screen Shot 2021-12-30 at 10 01 02 PM" src="https://user-images.githubusercontent.com/695749/147803589-1b29d7be-5db8-4aa8-8ef8-30866718ff2a.png"></kbd>

After the restaurant is created, log out and create the general manager account on the restaurant page: http://localhost:8000/restaurant/1

<kbd><img width="472" alt="Screen Shot 2021-12-30 at 10 02 43 PM" src="https://user-images.githubusercontent.com/695749/147803602-a0d0c794-6b1b-46d4-aee6-8aac25bd3ee1.png"></kbd>

Log out of the GM's account.

<kbd><img width="345" alt="Screen Shot 2021-12-30 at 10 02 54 PM" src="https://user-images.githubusercontent.com/695749/147803659-90cedf29-e970-4658-97bd-cb5ff2262bb2.png"></kbd>

Log in as the admin account and go to the new restaurant's page.

<kbd><img width="309" alt="Screen Shot 2021-12-30 at 10 03 08 PM" src="https://user-images.githubusercontent.com/695749/147803671-3884e393-672a-4ab2-b84f-1fab3c7d642f.png"></kbd>

Set the GM account on the restaurant page.

<kbd><img width="289" alt="Screen Shot 2021-12-30 at 10 03 24 PM" src="https://user-images.githubusercontent.com/695749/147803693-b35dc91b-9fc1-4721-99b0-2f8107e78616.png"></kbd>

Log out of the admin account and log back into the GM account.

<kbd><img width="344" alt="Screen Shot 2021-12-30 at 10 04 33 PM" src="https://user-images.githubusercontent.com/695749/147803715-0cff3421-3a95-43f1-911c-d7d5b91a7606.png"></kbd>

Go to the restaurant's page and add the roles.

<kbd><img width="399" alt="Screen Shot 2021-12-30 at 10 05 15 PM" src="https://user-images.githubusercontent.com/695749/147803731-f90d2c9e-d881-44a8-a459-7402cbf097af.png"></kbd>

Log out and create an employee account on the restaurant page: http://localhost:8000/restaurant/1

<kbd><img width="497" alt="Screen Shot 2021-12-30 at 10 06 57 PM" src="https://user-images.githubusercontent.com/695749/147803741-41c06fc6-278b-435a-85fd-0a23ab3b4f48.png"></kbd>

You can now set the employee's priority for the different roles.

<kbd><img width="422" alt="Screen Shot 2021-12-30 at 10 11 07 PM" src="https://user-images.githubusercontent.com/695749/147803779-7835ff76-4f01-47f7-9b99-2c0072ace34c.png"></kbd>

## Submit the code

First, verify that your changes are still valid.

`./pr_build.sh fix` (Note: pr_build.sh has only been tested on macOS and Ubuntu)

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

There should be a green button that says `Compare & pull request`.

<img width="553" alt="Screen Shot 2021-12-30 at 11 42 43 AM" src="https://user-images.githubusercontent.com/695749/147775951-2554acf3-cbb6-480f-ba6e-d46ec23f0985.png">

After the pull request is created, respond to comments, fix anything needed. 
Changes can be made, and then you can `commit` and `push` (see above) to update your branch.
Once everything is good, you can complete the pull request (green `Squash and merge` button near the bottom).

`<img` width="553" alt="Screen Shot 2021-12-30 at 11 45 48 AM" src="https://user-images.githubusercontent.com/695749/147775964-eb40d818-8ce0-4cb8-b31f-2191726616e8.png">

The confirm the completion by pressing the green `Confirm squash and merge` button.

<img width="562" alt="Screen Shot 2021-12-30 at 11 45 55 AM" src="https://user-images.githubusercontent.com/695749/147775991-a890c1aa-8d2f-4243-8663-97e514f5f8b1.png">

## Get ready for the next change

After the pull request is complete, `main` now has newer source than you have on your machine.

`git checkout main` \
`git pull`

You can now go back to the [Modify the source](#modify-the-source) step above.

## Working on Windows

The commands in `pr_build.sh` can be used to determine how to work on Windows.
Contribution of `pr_build.bat` to support Windows are definitely welcome.

