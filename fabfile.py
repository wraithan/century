from fabric.api import env, run, cd, sudo, local, get, prefix
from contextlib import contextmanager

env.hosts = ['wraithan.net', ]
project_name = 'century'
deploy_dir = '/srv/wsgi/%s/' % project_name
activate = 'source /home/wraithan/.virtualenvs/%s/bin/activate' % project_name

@contextmanager
def virtualenv():
    with cd(deploy_dir):
        with prefix(activate):
            yield

def virtualenv_local(cmd):
    local('source /home/wraithan/.virtualenvs/%s/bin/activate && %s' %s (project_name, cmd))


def deploy():
    git_pull()
    install_requirements()
    sync_db()
    reload_code()


def full_restart_gunicorn():
    stop_gunicorn()
    start_gunicorn()


def git_clone():
    with cd('/srv/wsgi/'):
        run('git clone git@github.com:wraithan/%s.git' % project_name)


def git_pull():
    with cd(deploy_dir):
        run('git pull')


def install_requirements():
    with virtualenv():
        run('pip install --upgrade -r deploy-requirements.txt')


def start_gunicorn():
    with virtualenv():
        run('./manage.py run_gunicorn -c conf/gunicorn.py')

def stop_gunicorn():
    with cd(deploy_dir):
        sudo('kill `cat gunicorn.pid`')


def reload_nginx_conf():
    sudo('/etc/rc.d/nginx check')
    sudo('/etc/rc.d/nginx reload')


def sync_db():
    with virtualenv():
        run('./manage.py syncdb')


def reload_code():
    with cd(deploy_dir):
        sudo('kill -HUP `cat gunicorn.pid`')


