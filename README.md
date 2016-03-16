footbag-db
==========

[![CI status][2]][1]

[![Coverage Status](https://coveralls.io/repos/shuttle1987/footbag-db/badge.png?branch=develop)](https://coveralls.io/r/shuttle1987/footbag-db?branch=develop)

  [1]: https://travis-ci.org/shuttle1987/footbag-db/
  [2]: https://travis-ci.org/shuttle1987/footbag-db.svg
  
This project aims create a set of educational tools accessible from the web
to help people learn the skills and techniques involved in the sport of footbag.
At the projects core is a video encyclopedia of techniques in the sport that is easy to search.
By creating a database of the various footbag moves it makes it possible for people to search for
techniques by describing the moves without needing to know the names/nicknames for a move ahead of time.

##Installation
In this project I have used virtualenvwrapper to make sure that the versions of software used are consistent.
To install the site locally you will need to satisfy the dependencies found in requirements.txt.
If there any any problems with the packages or if updating the packages is appropriate please do create
an issue in the issues tracker.

Depending on the database backend being used the Django settings might need to be
changed.

###Initial migrations
In a bare install there's no database tables yet.
Run:

```
python manage.py makemigrations footbagmoves
python manage.py migrate --fake-initial
```
##Settings
Setting related to the deployment of the site can be found in the deployment_settings.cfg file in the top level.
This is just a standard configuration file as used by the python configparser.

Sample file is as follows:
```
[ServerType]
live_server: yes

[secrets]
SECRET_KEY: SuperSecretASCIIstring

[database]
MYSQL_PASS: MYSQLpassword
MYSQL_DB_NAME: footbag_database
MYSQL_DB_USER: janis
MYSQL_TEST_DB_NAME: test_footbag_database
```

###Secret key
This is not stored in the settings.py file because it's not safe to store in version control.
Store the secret key in secrets section of the config file.

##Git workflow
For a conceptual overview of the type of branching strategy we are using have a
look at http://scottchacon.com/2011/08/31/github-flow.html .
Because this is a web based project there is a develop branch that is hosted
on a development subdomain.
As much as possible the development site is the same as the live site.
This lets us test changes in a controlled environment before we go live with them.

There are 2 important branches:

1. **master branch**: This directly reflects what is on the live website.
   Therefore this branch must always be in a state that can be deployed at all times.
   Because the master branch is deployed to the live website make sure that all commits
   pass the unit tests and are to the best of your knowledge bug free.
2. **develop branch**: This directly reflects what is on the development site.
   This is currently hosted on our development server, so be mindful when pushing changes to this branch.


###Master branch
Before anything is pushed to the master branch it first needs to be tested on the develop branch.
Because the master branch *is* the live site any changes to this branch must be via a pull request.

This branch is deployed to the live site via the invoke script found in tasks.py
Note that the script will not deploy to the live site if *any* unit tests do not pass,
so please make sure that all the test pass before creating a pull request.

###New features
Any new features should be worked on in a development site on their own branch before
they are pushed to the develop branch.

To keep things organized in the network graphs for this git repository work on
any orthogonal features in a named branch. Please choose descriptive names.
If you are making a bugfix then fast forward merging is ok.

##Issues/bugs
Any issues or bugs should be reported in the github issues tracking page https://github.com/shuttle1987/footbag-db/issues.
Please tag bugs with the bug tag.

##Questions
Feel free to contact me with any questions relating to this project.
