import unittest

from changeset_list import ChangesetList


class TestChangesetList(unittest.TestCase):
    def setUp(self):
        self.changeset_list = ChangesetList()

    def test_add_changeset(self):
        chg = MockChangeset()
        self.changeset_list.add(chg)
        self.assertIn(chg.commitid, self.changeset_list._changesets)

    def test_add_changeset_refuses_to_keep_dupes(self):
        self.changeset_list.add(MockChangeset('abc'))
        self.changeset_list.add(MockChangeset('abc'))
        self.assertEquals(1, len(self.changeset_list._changesets))

    def test_remove_changesets_with_no_bugs_fixed(self):
        self.changeset_list.add(MockChangeset(num_bugs_fixed=0))
        self.changeset_list.remove_changesets_which_do_not_fix_a_bug()
        self.assertEquals(0, len(self.changeset_list._changesets))

    def test_remove_changesets_leaves_bugs_which_fix_bugs(self):
        no_bugs = MockChangeset(commitid='nobugs', num_bugs_fixed=0)
        with_bugs = MockChangeset(commitid='bugs', num_bugs_fixed=2)
        self.changeset_list.add(no_bugs)
        self.changeset_list.add(with_bugs)
        self.changeset_list.remove_changesets_which_do_not_fix_a_bug()
        self.assertEquals(1, len(self.changeset_list._changesets))
        self.assertIn(with_bugs.commitid, self.changeset_list._changesets)


class MockChangeset(object):
    def __init__(self, commitid='abc', num_bugs_fixed=0):
        self.commitid = commitid
        self.num_bugs_fixed = num_bugs_fixed

    def bugs_fixed_count(self):
        return self.num_bugs_fixed
