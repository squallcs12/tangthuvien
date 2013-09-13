from fabric.api import task, run, require, put, sudo, local
import threading

settings = threading.local()
settings.branch = local("git branch | grep \"*\"", capture=True)[2:]

def deploy():
    pass
    
def update():
    local("git pull origin %s" % settings.branch)
    local("pip install -r requirements.txt")
    local("python manage.py migrate")