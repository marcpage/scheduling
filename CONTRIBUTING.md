# Contributing to scheduling

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

## What should I know before getting started?

TODO

## Coding conventions

The only coding conventions are enforced by running black, pylint (with a line limit of 100 columns), and flake8. 
On Linux and macOS you can run `pr_build.sh` which will clean up your changes to comply with the coding conventions and error on what it doesn't clean up.

**Please** make sure that your editor does not reformat the code (especially to force it into columns less than 100).

## Pull request conventions

Pull Requests should be single-topic and small. 
If you are refactoring (or even reformatting), please do that as a single change with minimal other changes.
The idea is to make Code Reviews as easy as possible. 
We want lots of small code reviews instead of a few giant code reviews.

## How to run the tests and the website

On Linux and macOS, you can just run `./pr_build.sh` which will validate your source. 
`./prbuild.sh fix` will attempt to format your source correctly (`black`). 
`./pr_build.sh run` will run the web server on the default port `8000`.

**Note:** [Issue #40](https://github.com/marcpage/scheduling/issues/40) is available to create a pr_build.bat for Windows to do similar behavior.
This issue has details on how to run the various steps manually.

## Model documentation

You can view the [current model in use](https://dbdiagram.io/d/61d258173205b45b73d415fc).

## Notes to refer to when adding to this document

These are notes for me to add more information to this document.

* [atom](https://github.com/atom/atom/blob/master/CONTRIBUTING.md)
* [rails](https://github.com/rails/rails/blob/main/CONTRIBUTING.md)
* [opengovernment](https://github.com/opengovernment/opengovernment/blob/master/CONTRIBUTING.md)
