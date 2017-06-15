# Fabfile to:
# - Install RVM
# - Install Ruby
# - Install Bundler

from fabric.api import *

env.hosts = ["172.17.0.2", "172.17.0.3"]
env.user = "root"

def prepare_requirements_softwares():
  run("yum install -y curl")

def install_rvm():
  with cd("$HOME"):
    run("gpg2 --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3")
    run("curl -L get.rvm.io | bash -s stable")
    run("echo \"source /etc/profile.d/rvm.sh\" | tee -a ~/.bashrc")

def install_ruby(ruby_version):
  run("source /etc/profile.d/rvm.sh")
  run("rvm requirements")
  run("rvm install ruby-%s" % ruby_version)
  run("gem install bundler")

def install(ruby_version = "2.3.1"):
  prepare_requirements_softwares()
  install_rvm()
  install_ruby(ruby_version)
