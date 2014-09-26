""" This fabfile is designed to help deploy the site using git. The workflow being
used here assumes that the master branch is for a the deployable site.
"""

from fabric.api import lcd, local, prefix, run
from contextlib import contextmanager

virtualenv_name = 'footbagsite'

#This is a helper to make sure that we are in the right virtualenv
@contextmanager
def virtualenvwrapper():
    with prefix("source ~/.virtualenvs/footbagsite/bin/activate"):
        yield

def run_tests():
    """ Run the unit test suite """
    with virtualenvwrapper():
        local('python manage.py test footbag_site', shell='/bin/bash')

def prepare_deployment(branch_name):
    """ Prepare to deploy from a git branch if and only if the unit tests pass
    The syntax to call this from the command line is:
    fab prepare_deployment:branch_name
    where branch_name is the name of the branch being deployed
    """
    run_tests()
    local('git add -p && git commit')
    local('git checkout master && git merge ' + branch_name)

def deploy():
    """ Deploy from the dev folder to the live site using git, assumes changes have
    already been prepared with prepare_deployment.
    """
    with lcd('~/footbagsite/www_footbag_info/'):
        compile_scss()
        local('git pull ~/footbagsite/dev-site/')
        with virtualenvwrapper():
            local('python manage.py migrate footbagmoves', shell='/bin/bash')
        restart_server()

def restart_server():
    """ The command to restart the web server.
    PythonAnywhere is set up such that touching the WSGI file restarts the server.
    Change this command to whatever your web server requires."""
    local('touch /var/www/www_footbag_info_wsgi.py')#restarts PythonAnywhere server

def compile_scss():
    """ Compile the SCSS files into regular CSS and place those in the static directory.
    Requires SCSS processor to be installed."""
    local('mkdir -p static/basic_theme/css/', shell='/bin/bash')
    with virtualenvwrapper():
        with lcd('scss/'):
            local('pyscss *.scss > ../static/basic_theme/css/style.css', shell='/bin/bash')

