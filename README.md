footbag-db
==========

This project aims create a set of educational tools accessible from the web
to help people learn the skills and techniques involved in the sport of footbag.

Note on git workflow:
The assumption is that the master branch is always in such a state that the site
can be deployed from that branch at any given time. Any commits to the master branch
should pass all tests.

Any features should be worked on in their own branch then deployed to the main site
using the Fabric deployment.

Note on installation:
In this project I have used virtualenvwrapper to make sure that the versions of software used are consistent.

If you wish to run this site on your own computer you will need to set up a virtualenv
and install all the packages listed in requirements.txt.
