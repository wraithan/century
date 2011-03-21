from fabric.api import env, run, cd, sudo, local, get


env.hosts = ['wraithan.net', ]
deploy_dir = '/srv/wsgi/century/'
project_name = 'century'

def virtualenv_run(cmd):
    run('workon %s && %s' % (project_name, cmd))


def virtualenv_local(cmd):
    local('workon %s && %s' %s (project_name, cmd))


def deploy():
    git_pull()
    install_requirements()
    sync_db()
    reload_code()


def install():
    make_deploy_dir()
    git_clone()
    make_virtualenv()
    install_requirements()
    start_gunicorn()
    install_nginx_conf()
    enable_nginx_conf()
    reload_nginx_conf()
    create_db()
    sync_db()

def full_restart_gunicorn():
    stop_gunicorn()
    start_gunicorn()


def make_deploy_dir():
    sudo('mkdir ' + deploy_dir)
    sudo('chown wraithan:users ' + deploy_dir)


def git_clone():
    with cd('/srv/wsgi/'):
        run('git clone git@github.com:wraithan/%s.git' % project_name)


def git_pull():
    with cd(deploy_dir):
        run('git pull')


def make_virtualenv():
    run('mkvirtualenv --no-site-packages %s' % project_name)


def install_requirements():
    with cd(deploy_dir):
        virtualenv_run('pip install -r --upgrade deploy-requirements.txt')


def start_gunicorn():
    with cd(deploy_dir):
        virtualenv_run('gunicorn_django --pid=' + deploy_dir +
                       '/gunicorn.pid --workers=2 -b 127.0.0.1:8020 --daemon deploy_settings.py')

def stop_gunicorn():
    with cd(deploy_dir):
        sudo('kill `cat gunicorn.pid`')


def install_nginx_conf():
    sudo('cp ' + deploy_dir +
         '/conf/%s /etc/nginx/sites-available/%s' % (project_name, project_name))


def enable_nginx_conf():
    sudo('ln -s /etc/nginx/sites-available/%s /etc/nginx/sites-enabled/%s' % (project_name, project_name))


def reload_nginx_conf():
    sudo('/etc/rc.d/nginx check')
    sudo('/etc/rc.d/nginx reload')


def create_db():
    run('createdb %s')


def sync_db():
    with cd(deploy_dir):
        virtualenv_run('./manage.py syncdb')


def reload_code():
    with cd(deploy_dir):
        sudo('kill -HUP `cat gunicorn.pid`')


