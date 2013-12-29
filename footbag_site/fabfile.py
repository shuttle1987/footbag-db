from fabric.api import lcd, local

def prepare_deployment(branch_name):
    """ Prepare to deploy from a git branch if and only if the unit tests pass """
    local('python manage.py test footbag_site')
    local('git add -p && git commit')

def deploy():
    """ Deploy from the dev folder to the live site using git"""
    with lcd('~/footbagsite/www_footbag_info/footbag_site'):
        local('git pull ~/footbagsite/dev/www_footbag_info/footbagsite')
        local('python manage.py migrate footbagmoves')
        #local('command to restart webserver')
