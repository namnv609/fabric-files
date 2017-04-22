# Fabfile to:
#   - Install RVM
#   - Install Ruby
#   - Install Bundler
#   - Install Rails

from fabric.api import *

env.hosts = ["172.17.0.2", "172.17.0.3"]
env.user = "root"

def prepare_requirement_softwares():
  run("apt-get update")
  run("apt-get install -y curl")

def install_rvm():
  with cd("$HOME"):
    run("curl -sSL https://github.com/rvm/rvm/tarball/stable -o rvm-stable.tar.gz")
    run("mkdir rvm-stable")
    run("tar -xzvf rvm-stable.tar.gz -C rvm-stable --strip-components=1")

  with cd("$HOME/rvm-stable"):
    run("./install --auto-dotfiles")
    run("echo \"source /usr/local/rvm/scripts/rvm\" | tee -a ~/.bashrc")

  with cd("$HOME"):
    run("rm -rf rvm-stable rvm-stable.tar.gz")

def install_ruby(ruby_version, rails_version):
  run("source /usr/local/rvm/scripts/rvm")
  run("rvm install ruby-%s" % ruby_version)
  run("gem install bundler")
  run("gem install rails -v %s" % rails_version)

def install(ruby_version = "2.3.1", rails_version = "4.2.6"):
  prepare_requirement_softwares()
  install_rvm()
  install_ruby(ruby_version, rails_version)
