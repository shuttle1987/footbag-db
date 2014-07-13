footbag-db
==========

This project aims create a set of educational tools accessible from the web
to help people learn the skills and techniques involved in the sport of footbag.
At the projects core is a video encyclopedia of techniques in the sport that is easy to search. By creating a database of the various footbag moves it makes it possible for people to search for techniques by describing the moves without needing to know the names/nicknames for a move ahead of time. 

##Installation
In this project I have used virtualenvwrapper to make sure that the versions of software used are consistent. To install the site you need to satisfy the dependencies found in requirements.txt.

##Git workflow
For a conceptual overview I think it's good to have a look at http://scottchacon.com/2011/08/31/github-flow.html .
The assumption is that the master branch is always in a state that can be deployed.
Because the master branch should always be able to be deployed any commits to the master branch should pass all tests. (The Fabric deployment will not deploy to master if unit tests fail)

Any features should be worked on in a development site on their own branch before being deployed to the main site
using the Fabric deployment. Fabric will not deploy the site if the unit tests do not pass.

To keep things looking good in the network graphs for this git repository any orthogonal feature is worked on in its own named branch.

##Issues/bugs
Any issues or bugs should be reported in the github issues tracking page https://github.com/shuttle1987/footbag-db/issues.

##Questions
Feel free to contact me with any questions relating to this project.
