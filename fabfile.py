import datetime
import os.path
from fabric.api import *

env.project_name = 'xbtests'
env.user_name = env.project_name
env.virtualenv = env.project_name
env.production = False
env.server_flavor = None
env.uploads_paths = ()
env.timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
env.branch = 'master'



# ENVIRONMENTS

def staging():
    raise NotImplemented
    
def production():
    """Deploy on live server"""
    env.production = True
    env.user_name = 'pb'
    env.hosts = ['%(user_name)s@web03.pb.io' % env]
    env.server_flavor = 'gunicorn'
    env.path = '/home/%(user_name)s/projects/%(project_name)s' % env



# COMMANDS

def deploy_only():
    """Push (local) and pull (remote) the Github repo"""
    if env.production:
        input = prompt('Are you sure you want to deploy to the production server?', default="n", validate=r'^[yYnN]$')
        if input not in ['y','Y']:
            exit()
    local("git push origin %(branch)s" % env)
    with cd(env.path):
        run("git pull origin %(branch)s" % env)

def deploy():
    """Update code, migrate database and restart server."""
    deploy_only()
    migrate()
    reload_server()

def migrate():
    """Sync and migrate the database."""
    with cd(env.path):
        run("../../.virtualenvs/%(virtualenv)s/bin/python ./manage.py syncdb" % env)
        run("../../.virtualenvs/%(virtualenv)s/bin/python ./manage.py migrate" % env)

def reload_server():
    """Reload the webserver and take the server flavor into account."""
    if env.server_flavor == 'lighttpd':
        run('~/init/%(project_name)s restart' % env)
    elif env.server_flavor == 'mod_wsgi':
        run("touch %(path)s/deploy/project.wsgi" % env)
    elif env.server_flavor == 'gunicorn':
        run("sudo supervisorctl restart %(user_name)s__%(project_name)s" % env)
    else:
        raise NotImplementedError, "reload_server() is not configured for %(server_flavor)s server flavor." % env

def get_dump():
    """Create, download and import database dump"""
    env.dump_filename = "dump-%(timestamp)s.sql" % env
    with cd(env.path):
        run('export DJANGO_SETTINGS_MODULE=settings ; echo "from django.conf import settings ; print \'mysqldump -u%%(USER)s -p%%(PASSWORD)s %%(NAME)s > %(dump_filename)s\' %% settings.DATABASES[\'default\']" | ~/.virtualenvs/%(virtualenv)s/bin/python | sh' % env)
        get('%(path)s/%(dump_filename)s' % env, env.dump_filename)
        run('rm -f %(path)s/%(dump_filename)s' % env)
    if prompt('Import dump and OVERWRITE EXISTING DATABASE? (y/n)', default="n") == "y":
        local('python ./manage.py dbshell < %(dump_filename)s' % env)
        if prompt('Delete downloaded dump? (y/n)', default="n") == "y":
            local('rm %(dump_filename)s' % env)

def get_uploads():
    """Get update from remote server and unpack locally"""
    env.uploads_filename = "uploads-%(timestamp)s.tar.gz" % env
    env.uploads_paths_joined = " ".join(env.uploads_paths)
    with cd(env.path):
        run('tar -czf %(uploads_filename)s %(uploads_paths_joined)s' % env)
        get('%(path)s/%(uploads_filename)s' % env, env.uploads_filename)
        run('rm %(uploads_filename)s' % env)
    local('tar -xvzf %(uploads_filename)s' % env)
    local('rm %(uploads_filename)s' % env)

def push_dump():
    """Push a local db dump to remote server and import it"""
    local('mysqldump %(project_name)s > dump.sql' % env)
    put('dump.sql', '%(path)s/dump.sql' % env)
    with cd(env.path):
        env.dump_filename = "dump-%(timestamp)s.sql" % env
        run('export DJANGO_SETTINGS_MODULE=settings ; echo "from django.conf import settings ; print \'mysqldump -u%%(USER)s -p%%(PASSWORD)s %%(NAME)s > ~/backups/db/%(dump_filename)s\' %% settings.DATABASES[\'default\']" | ~/.virtualenvs/%(virtualenv)s/bin/python | sh' % env)
        run('../../.virtualenvs/%(virtualenv)s/bin/python ./manage.py dbshell < dump.sql' % env)
        run('rm dump.sql')
    local('rm dump.sql')

def push_uploads():
    """Push local uploads to the remote server and unpack"""
    env.uploads_filename = "uploads-%(timestamp)s.tar.gz" % env
    env.uploads_paths_joined = " ".join(env.uploads_paths)
    local('tar -czf %(uploads_filename)s %(uploads_paths_joined)s' % env)
    put(env.uploads_filename, '%(path)s/%(uploads_filename)s' % env)
    with cd(env.path):
        run('tar -xzf %(uploads_filename)s' % env)
        run('rm %(uploads_filename)s' % env)
    local('rm %(uploads_filename)s' % env)

def install_requirements():
    """Install requirements from requirements.txt"""
    with cd(env.path):
        run('~/.virtualenvs/%(virtualenv)s/bin/pip install -r requirements.txt' % env)

def update_requirements():
    """Update requirements from requirements.txt"""
    with cd(env.path):
        run('~/.virtualenvs/%(virtualenv)s/bin/pip install -Ur requirements.txt' % env)
