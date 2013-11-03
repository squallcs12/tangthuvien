from fabric.api import task, run, require, put, sudo, local, env
import threading

env.hosts = ['root@210.211.109.43']

def deploy():
    "Deploy current branch to remote server"
    Deploy.deploy()

def setup():
    "Setup remote server before deploy"
    Deploy.setup()

def update():
    "Update local"
    Deploy.update_local()

def test():
    "Testing commands"
    print Deploy.get_python_version()

def restart_web():
    Deploy.init()
    Deploy.restart_web_services()

def init_folder_tree():
    Deploy.init_folder_tree()

class Deploy(object):

    @classmethod
    def sudo(cls, command):
        sudo(command, user='www-data')

    @classmethod
    def init(cls):
        cls.project_name = 'tangthuvien.vn'
        cls.deploy_dir = '/var/www/tangthuvien.vn'
        cls.current_dir = '/var/www/tangthuvien.vn/current'
        cls.share_dir = '/var/www/tangthuvien.vn/shared'
        cls.bin_dir = '%s/bin' % cls.share_dir
        cls.program_dir = "%s/program" % cls.share_dir
        cls.log_dir = "%s/log" % cls.share_dir
        cls.virtualenv_dir = '/var/www/tangthuvien.vn/shared/virtualenv'
        cls.git_source = "https://github.com/squallcs12/tangthuvien.git"
        cls.have_yum = cls.is_command_exists('yum')

    @classmethod
    def install_git(cls):
        if not cls.is_command_exists('git'):
            if cls.have_yum:
                sudo("yum install git -y")
            else:
                sudo("apt-get install git -y")

    @classmethod
    def is_command_exists(cls, command):
        return len(run("whereis %s" % command)) > len("%s: " % command)

    @classmethod
    def get_command_real_path(cls, command):
        return run("whereis %s" % command).split(' ')[1]

    @classmethod
    def mkdirs(cls):
        sudo("mkdir -p %s" % cls.deploy_dir)
        sudo("mkdir -p %s/releases" % cls.deploy_dir)
        sudo("mkdir -p %s" % cls.share_dir)
        sudo("mkdir -p %s/run" % cls.share_dir)
        sudo("mkdir -p %s/static" % cls.share_dir)
        sudo("mkdir -p %s/log" % cls.share_dir)
        sudo("mkdir -p %s/log/copybook" % cls.share_dir)
        sudo("mkdir -p %s/media" % cls.share_dir)
        sudo("mkdir -p %s/media/uploads" % cls.share_dir)
        sudo("mkdir -p %s/media/uploads/ckeditor" % cls.share_dir)
        sudo("mkdir -p %s/media/thumbs" % cls.share_dir)
        sudo("mkdir -p %s/media/thumbs/books" % cls.share_dir)
        sudo("mkdir -p %s/media/thumbs/books/covers" % cls.share_dir)
        sudo("mkdir -p %s/media/books" % cls.share_dir)
        sudo("mkdir -p %s/media/books/attachments" % cls.share_dir)
        sudo("mkdir -p %s/media/books/covers" % cls.share_dir)
        sudo("mkdir -p %s/media/books/prc" % cls.share_dir)
        sudo("mkdir -p %s" % cls.program_dir)
        sudo("mkdir -p -m 777 /var/log/tangthuvien.vn")
        sudo("touch %s" % cls.current_dir)  # so that we can remote it later
        sudo("touch %s/local_settings.py" % cls.share_dir)


    @classmethod
    def checkout_source(cls, current_time):
        release_dir = "%s/releases/%s" % (cls.deploy_dir, current_time)
        sudo("git clone %s %s;" % (cls.git_source, release_dir))
        sudo("rm %s" % cls.current_dir)

        sudo("ln -s %s/releases/%s %s" % (cls.deploy_dir, current_time, cls.current_dir))
        sudo("cd %s; git checkout %s" % (cls.current_dir, cls.branch()))
        sudo("chown -R www-data:www-data %s" % release_dir)

        cls.sudo("ln -s %s/media %s/media" % (cls.share_dir, cls.current_dir))
        cls.sudo("ln -s %s/static %s/static" % (cls.share_dir, cls.current_dir))

        cls.sudo("ln -s %s/local_settings.py %s/local_settings.py" % (cls.share_dir, cls.current_dir))

        cls.sudo("ln -s %s/bin %s" % (cls.current_dir, cls.bin_dir))
        cls.sudo("ln -s %s %s/env" % (cls.virtualenv_dir, cls.current_dir))
        cls.sudo("ln -s %s %s/program" % (cls.program_dir, cls.current_dir))
        cls.sudo("ln -s %s %s/log" % (cls.log_dir, cls.current_dir))

    @classmethod
    def sudo_virtualenv(cls, command):
        cls.sudo("source %s/bin/activate; %s" % (cls.virtualenv_dir, command))

    @classmethod
    def install_requirements(cls):
        cls.sudo_virtualenv("cd %s; pip install -r requirements.txt" % cls.current_dir)

    @classmethod
    def get_python_version(cls):
        return ".".join(run("python -V").split(' ')[1].split('.')[0:2])

    @classmethod
    def install_python(cls):
        if cls.get_python_version() != '2.7':
            sudo("cd ~; wget http://www.python.org/ftp/python/2.7.5/Python-2.7.5.tar.bz2")
            sudo("cd ~; tar -xf Python-2.7.5.tar.bz2")
            sudo("cd ~/Python-2.7.5; ./configure")
            sudo("cd ~/Python-2.7.5; make")
            sudo("cd ~/Python-2.7.5; make install")

    @classmethod
    def install_setup_tools(cls):
        if not cls.is_command_exists('easy_install'):
            sudo("cd ~; wget https://pypi.python.org/packages/source/s/setuptools/setuptools-1.1.5.tar.gz --no-check-certificate")
            sudo("cd ~; tar -xf setuptools-1.1.5.tar.gz")
            sudo("python2.7 ~/setuptools-1.1.5/setup.py install")

    @classmethod
    def install_redis(cls):
        if not cls.is_command_exists('redis-cli'):
            if cls.have_yum:
                sudo("yum install redis -y")
            else:
                sudo("apt-get install redis-server -y")

    @classmethod
    def install_pip(cls):
        if not cls.is_command_exists('pip'):
            sudo("%s pip" % cls.get_command_real_path('easy_install'))

    @classmethod
    def install_virtualenv(cls):
        if not cls.is_command_exists('virtualenv'):
            sudo("%s install virtualenv", cls.get_command_real_path('pip'))

    @classmethod
    def is_file_exists(cls, filename):
        return sudo("if test -f %s; then echo 1; else echo 0; fi" % filename) == '1'

    @classmethod
    def create_virtualenv(cls):
        if not cls.is_file_exists('%s/bin/activate' % cls.virtualenv_dir) :
            cls.sudo("%s %s" % (cls.get_command_real_path('virtualenv'), cls.virtualenv_dir))

    @classmethod
    def install_mysql_dev(cls):
        if cls.have_yum:
            sudo("yum install mysql-devel -y")
        else:
            sudo("apt-get install libmysqld-dev -y")

    @classmethod
    def create_user_and_group(cls):
        # user not exists
        if not sudo("cat /etc/passwd | grep www-data"):
            sudo("useradd www-data")
        else:
            if not sudo("cat /etc/group | grep www-data"):
                sudo("groupadd www-data")
                sudo("useradd -G www-data www-data")

    @classmethod
    def chown_dirs(cls):
        sudo("chown -R www-data:www-data %s" % cls.deploy_dir)
        sudo("chown -R www-data:www-data %s" % cls.deploy_dir)

    @classmethod
    def install_supervisor(cls):
        if not cls.is_command_exists('supervisorctl'):
            if cls.have_yum:
                sudo("yum install supervisor -y")
            else:
                sudo("apt-get install supervisor -y")

    @classmethod
    def copy_system_config_files(cls):
        sudo("rm -f /etc/nginx/sites-enabled/tangthuvien.vn.conf")
        sudo("cp %s/bin/nginx.conf /etc/nginx/sites-enabled/tangthuvien.vn.conf" % cls.current_dir)

    @classmethod
    def restart_web_services(cls):
        sudo("chmod 777 %s/bin/gunicorn_start.sh" % cls.current_dir)

        cls.sudo_virtualenv("supervisorctl -c%s/bin/supervisor.conf shutdown" % cls.current_dir)
        cls.sudo_virtualenv("supervisord -c%s/bin/supervisor.conf" % cls.current_dir)

        sudo("service nginx restart")

    @classmethod
    def run_migration(cls):
        cls.sudo_virtualenv('cd %s; python manage.py syncdb --migrate;' % cls.current_dir)

    @classmethod
    def collect_statics(cls):
        cls.sudo_virtualenv("cd %s; python manage.py collectstatic --noinput" % cls.current_dir)

    @classmethod
    def install_image_libs(cls):
        if cls.have_yum:
            sudo("yum install libpng-devel -y")
            sudo("yum install libjpeg-devel -y")
        else:
            sudo("apt-get install libpng-devel -y")
            sudo("apt-get install libjpeg-devel -y")

    @classmethod
    def combine_django_messages(cls):
        cls.sudo_virtualenv("cd %s; python manage.py compilemessages" % cls.current_dir)

    @classmethod
    def install_kindlegen(cls):
        if not cls.is_file_exists("%s/kindlegen" % cls.program_dir):
            sudo("cd /tmp; wget http://kindlegen.s3.amazonaws.com/kindlegen_linux_2.6_i386_v2_9.tar.gz")
            sudo("cd /tmp; tar -xf kindlegen_linux_2.6_i386_v2_9.tar.gz")
            sudo("cp /tmp/kindlegen %s" % cls.program_dir)

    @classmethod
    def branch(cls):
        return local("git branch | grep \"*\"", capture=True)[2:]

    @classmethod
    def update_cronjob_files(cls):
        replacements = {
            'virtualenv_dir': cls.virtualenv_dir,
            'current_dir': cls.current_dir,
            'share_dir': cls.share_dir,
            'bin_dir': cls.bin_dir,
            'program_dir': cls.program_dir,
            'log_dir': cls.log_dir,
        }
        dirs = os.listdir(".")
        sub_dirs = ('cron.daily', 'cron.hourly', 'cron.monthly', 'cron.weekly', 'cron.d',)
        for sub_dir in sub_dirs:
            cron_dir = os.path.join('/', 'etc', sub_dir)
            sudo("rm -f %s/%s*" % (cron_dir, cls.project_name))
        for dir_name in dirs:
            if not os.path.isdir(dir_name):  # if not a folder
                continue

            cronjobs_dir = "%s/cronjobs" % dir_name
            if not os.path.isdir(cronjobs_dir):  # if no crontabs
                continue
            for sub_dir in sub_dirs:
                cron_dir = "%s/%s" % (cronjobs_dir, sub_dir)
                if not os.path.isdir(cron_dir):
                    continue
                cron_files = os.listdir(cron_dir)
                for cron_file in cron_files:
                    source_file = os.path.join(cls.current_dir, dir_name, "cronjobs", sub_dir, cron_file)
                    destination_file_name = "%s_%s_%s" % (cls.project_name, dir_name, cron_file)
                    destination_file = os.path.join('/', 'etc', sub_dir, destination_file_name)
                    command = "cat %s" % source_file
                    for key, value in replacements.items():
                        command += " | sed 's/{{%s}}/%s/g'" % (key, value.replace('/', '\/'))
                    command += " > %s" % destination_file
                    sudo(command)

                    sudo("chmod 777 %s" % destination_file)

    @classmethod
    def setup(cls):
        cls.init()
        cls.mkdirs()
        cls.install_git()
        cls.install_python()
        cls.install_setup_tools()
        cls.install_pip()
        cls.install_virtualenv()
        cls.create_user_and_group()
        cls.chown_dirs()
        cls.create_virtualenv()
        cls.install_mysql_dev()
        cls.install_supervisor()
        cls.install_redis()
        cls.install_image_libs()
        cls.install_kindlegen()

    @classmethod
    def deploy(cls):
        cls.setup()
        current_time = run("date +%Y%m%d%H%M%S")
        cls.checkout_source(current_time)
        cls.install_requirements()
        cls.run_migration()
        cls.collect_statics()
        cls.combine_django_messages()
        cls.copy_system_config_files()
        cls.update_cronjob_files()
        cls.restart_web_services()

    @classmethod
    def init_folder_tree(cls):
        local("mkdir -p media/thumbs")
        local("mkdir -p media/thumbs/books")
        local("mkdir -p media/thumbs/books/covers")
        local("mkdir -p media/books")
        local("mkdir -p media/books/covers")
        local("mkdir -p media/uploads/ckeditor")
        local("mkdir -p run")
        local("mkdir -p static")
        local("mkdir -p log")
        local("mkdir -p log/copybook")
        local("mkdir -p media")
        local("mkdir -p media/uploads")
        local("mkdir -p media/uploads/ckeditor")
        local("mkdir -p media/thumbs")
        local("mkdir -p media/thumbs/books")
        local("mkdir -p media/thumbs/books/covers")
        local("mkdir -p media/books")
        local("mkdir -p media/books/attachments")
        local("mkdir -p media/books/covers")
        local("mkdir -p media/books/prc")
        local("mkdir -p program")
        local("python manage.py syncdb --migrate")


    @classmethod
    def update_local(cls):
        cls.init_folder_tree()
        local("sudo apt-get install libjpeg-dev -y")
        local("sudo apt-get install libpng-dev -y")
        local("git pull origin %s" % cls.branch())
        local("pip install -r requirements.txt")
        local("cd program; wget http://kindlegen.s3.amazonaws.com/kindlegen_linux_2.6_i386_v2_9.tar.gz")
        local("cd program; tar -xf kindlegen_linux_2.6_i386_v2_9.tar.gz")
        local("sudo mkdir -p /var/log/tangthuvien.vn/")
        local("sudo chmod 777 /var/log/tangthuvien.vn/")
        local("python manage.py syncdb --migrate")

