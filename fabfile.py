""" This fabfile is designed to help deploy the site using git. The workflow being
used here assumes that the master branch is for a the deployable site.
"""

from fabric.api import lcd, local

def run_tests():
    """ Run the unit test suite """
    local('python manage.py test footbag_site')

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
    PythonAnywhere is set up such that touching the WSGI file restarts the server
    """
    with lcd('~/footbagsite/www_footbag_info/'):
        local('git pull ~/footbagsite/dev-site/')
        local('python manage.py migrate footbagmoves')
        restart_server()

def restart_server():
    """ The command to restart the web server """
    local('touch /var/www/www_footbag_info_wsgi.py')#restarts PythonAnywhere server
