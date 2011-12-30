import os
from flypaper.mercurial_repo import MercurialRepo


class RepoFactory(object):
    @classmethod
    def get_repo(clazz, repodir, startdate):
        if os.path.isdir(repodir + "/.hg"):
            return MercurialRepo(repodir, startdate)
        else:
            raise Exception("No supported repository found: %s" % (repodir,))
