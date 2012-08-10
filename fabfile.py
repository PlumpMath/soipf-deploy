from fabric.api import *

# requirements:
#  local
#    lein
#    git
#  remote
#    java
#    mongodb

URL = "https://github.com/mcmt/soipf.git"
REPOSITORY = "soipf-checkout"

def build():
    #ensure_git(URL, REPOSITORY)
    local("git clone %(url)s %(dir)s" %
            {"url": URL,
             "dir": REPOSITORY})

    jar = None        

    with lcd(REPOSITORY):
        uber = local("lein uberjar", capture=True) \
            .split('\n')[-1]
        # assume no whitespace in the filepath
        jar = uber.split(' ')[-1]

    local("mkdir -p lib")
    local("ln -sf %(jar)s lib/soipf.jar" % {"jar": jar})

def deploy():
    sudo("mkdir -p /soipf/env/lib/")
    sudo("chown -R tim:tim /soipf")
    put("lib/soipf.jar", "/soipf/env/lib/soipf.jar")
