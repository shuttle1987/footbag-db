from invoke import task, run

@task
def compile_scss():
    """Compile the SCSS and copy to relevant static directory"""
    run("pyscss ./scss/*.scss > ./static/basic_theme/css/style.css")
    run("cp ./static/basic_theme/css/style.css ./footbag_site/static/basic_theme/css/style.css")

@task
def run_tests():
    """Run the unit testing suite"""
    run("python manage.py test")

def restart_server():
    """The command to restart the web server.
    PythonAnywhere is set up such that touching the WSGI file restarts the server.
    Change this command to whatever the web server requires."""
    run('touch /var/www/www_footbag_info_wsgi.py')#restarts PythonAnywhere server
