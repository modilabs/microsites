import os, sys
import collections

from fabric.api import env, run, cd


DEFAULTS = {
    'home': '/home/wsgi/srv/',
    'repo_name': 'reportcard',
    }

DEPLOYMENTS = {
    'dev': {
        'home': '/home/ubuntu/srv/',
        'host_string': 'ubuntu@litreportcards.modilabs.org',
        'project': 'reportcard-ec2',
        'key_filename': os.path.expanduser('~/.ssh/modilabs.pem'),
    },
}


def run_in_virtualenv(command):
    d = {
        'activate': os.path.join(
            env.project_directory, 'project_env', 'bin', 'activate'),
        'command': command,
        }
    run('source %(activate)s && %(command)s' % d)


def check_key_filename(deployment_name):
    if DEPLOYMENTS[deployment_name].has_key('key_filename') and \
        not os.path.exists(DEPLOYMENTS[deployment_name]['key_filename']):
        print "Cannot find required permissions file: %s" % \
            DEPLOYMENTS[deployment_name]['key_filename']
        return False
    return True

def setup_env(deployment_name):
    env.update(DEFAULTS)
    env.update(DEPLOYMENTS[deployment_name])
    if not check_key_filename(deployment_name): sys.exit(1)
    env.project_directory = os.path.join(env.home, env.project)
    env.code_src = os.path.join(env.project_directory, env.repo_name)
    env.wsgi_config_file = []
    env.wsgi_config_file.append(os.path.join(
        env.project_directory, 'apache', 'reportcard.wsgi'))
    env.wsgi_config_file.append(os.path.join(
        env.project_directory, 'apache', 'soillab.wsgi'))
    env.wsgi_config_file.append(os.path.join(
        env.project_directory, 'apache', 'soiltrack.wsgi'))
    env.pip_requirements_file = os.path.join(env.code_src, 'requirements.pip')


def deploy(deployment_name, branch='master'):
    setup_env(deployment_name)
    with cd(env.code_src):
        run("git fetch origin")
        run("git checkout origin/%s" % branch)
        run('pyclean .')
    run_in_virtualenv("pip install -r %s" % env.pip_requirements_file)
    with cd(env.code_src):
        run_in_virtualenv("python manage.py migrate")
        run_in_virtualenv("python manage.py collectstatic --noinput")
    if isinstance(env.wsgi_config_file, collections.Iterable):
        for config_file in env.wsgi_config_file:
            run('touch %s' % config_file)
    else:
        run('touch %s' % env.wsgi_config_file)
