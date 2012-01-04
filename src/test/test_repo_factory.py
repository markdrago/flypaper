import unittest

import os
from shutil import rmtree
from tempfile import mkdtemp

from mercurial_repo import MercurialRepo
from repo_factory import RepositoryNotFoundException
from repo_factory import RepoFactory


class TestRepoFactory(unittest.TestCase):
    def setUp(self):
        self.directory = mkdtemp('-flypaper-repo-factory-tests')
        self.rmtree = True

    def tearDown(self):
        if self.rmtree:
            rmtree(self.directory)

    def test_get_repo_fails_when_directory_is_not_present(self):
        non_existant_dir = os.path.join(self.directory, 'dne')
        with self.assertRaises(RepositoryNotFoundException):
            RepoFactory.get_repo(non_existant_dir)

    def test_get_repo_fails_when_non_supported_repo(self):
        os.mkdir(os.path.join(self.directory, '.dne'))
        with self.assertRaises(RepositoryNotFoundException):
            RepoFactory.get_repo(self.directory)

    def test_get_repo_returns_mercurial_repo(self):
        os.mkdir(os.path.join(self.directory, '.hg'))
        repo = RepoFactory.get_repo(self.directory)
        self.assertEquals(MercurialRepo, type(repo))
