# Fabfile to:
#   - Install logrotate
#   - Config logrotate
#   - Add new logrotate

from fabric.api import *
from fabric.contrib.files import exists
import ntpath

env.hosts = ["172.17.0.2", "172.17.0.3"]
env.user = "root"

def prepare_requirements_software():
  with settings(warn_only = True):
    if run("which logrotate").succeeded is not True:
      sudo("apt-get update")
      sudo("apt-get install logrotate")

def config_logrotate(logrotate_file):
  with settings(warn_only = True):
    logrotate_name = ntpath.basename(logrotate_file)
    with cd("/etc/logrotate.d"):
      if exists(logrotate_name, use_sudo = True) is not True:
        put(logrotate_file, logrotate_name, use_sudo = True)

        with cd("/etc/cron.daily"):
          if exists("logrotate") is not True:
            print("Cron daily for logrotate doesn't existing. Upload from template...")
            put("file_templates/logrotate_cron_daily", "logrotate", use_sudo = True, mode = "0755")
        sudo("logrotate %s" % logrotate_file)
        run("cat /var/lib/logrotate/status")
      else:
        print("Logrotate is exist")

def install(logrotate_file):
  prepare_requirements_software()
  config_logrotate(logrotate_file)
