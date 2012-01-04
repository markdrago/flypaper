import unittest

import os
from shutil import rmtree
from tempfile import mkdtemp

from mercurial_repo import MercurialRepo


class TestMercurialRepo(unittest.TestCase):
    def setUp(self):
        self.directory = mkdtemp('-flypaper-hg-repo-tests')
        self.repo = MercurialRepo(self.directory)
        self.rmtree = True

    def create_real_repo(self):
        self.repo.get_command_output('hg init')

    def tearDown(self):
        if self.rmtree:
            rmtree(self.directory)

    def test_creating_single_simple_changeset(self):
        fields = ChangesetFields()
        chg = self.repo._create_single_changeset(fields.get_logoutput())
        self.assert_changeset_fields_match_expected(fields, chg)

    def test_creating_single_changeset_strips_whitespace(self):
        fields = ChangesetFields()
        fields.node = "  %s  " % (fields.node)
        fields.date = "\t%s\t" % (fields.date)
        fields.desc = "   %s\t\t" % (fields.desc)
        fields.files = " \t  %s\t " % (fields.files)
        chg = self.repo._create_single_changeset(fields.get_logoutput())
        clean_fields = ChangesetFields()
        self.assert_changeset_fields_match_expected(clean_fields, chg)

    def assert_changeset_fields_match_expected(self, fields, chg):
        self.assertEquals(fields.node, chg.commitid)
        self.assertEquals(fields.date, chg.date.strftime("%Y-%m-%d"))
        self.assertEquals(fields.desc, chg.description)
        self.assertEquals(set(fields.files.split(' ')), chg.modified_files)

    def test_creating_single_changeset_without_modified_files(self):
        fields = ChangesetFields()
        fields.files = ""
        chg = self.repo._create_single_changeset(fields.get_logoutput())
        self.assertEquals(set(), chg.modified_files)

    def test_creating_single_changeset_gives_none_with_no_output(self):
        self.assertIsNone(self.repo._create_single_changeset(""))

    def test_create_changeset_list(self):
        fields1 = ChangesetFields()
        fields2 = ChangesetFields()
        fields2.node = "defg5678defg"
        logoutput = "%s\n%s\n" % (fields1.get_logoutput(),
                                  fields2.get_logoutput())
        chg_list = self.repo._create_changeset_list(logoutput)
        self.assertEquals(2, len(chg_list.changesets))


class ChangesetFields(object):
    def __init__(self):
        self.node = "abcd1234abcd"
        self.date = "2012-01-03"
        self.desc = "ID-123 first line of commit message"
        self.files = "dir1/file1.txt dir2/file2.txt"

    def get_logoutput(self):
        return "%s\n%s\n#%s\n#%s\n" % (self.node, self.date,
                                       self.desc, self.files)
