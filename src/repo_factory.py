import os
from mercurial_repo import MercurialRepo


class RepoFactory(object):
    @classmethod
    def get_repo(cls, repodir, startdate):
        if os.path.isdir(repodir + "/.hg"):
            return MercurialRepo(repodir, startdate)
        else:
            msg = "No supported repository found: %s" % (repodir,)
            raise RepositoryNotFoundException(msg)


class RepositoryNotFoundException(Exception):
    pass
