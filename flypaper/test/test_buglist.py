import unittest

from bug_list import BugList


class TestBugList(unittest.TestCase):
    def setUp(self):
        self.buglist = BugList()
        self.mock_bug_factory = MockBugFactory()
        self.buglist.bug_factory = self.mock_bug_factory

    def test_read_bug_list_creates_single_bug(self):
        bug_seq = ['bugid1']
        self.buglist.read_bug_list(bug_seq)
        self.assertEquals(1, len(self.buglist.bugs))

    def test_read_bug_list_strips_whitespace_from_bugids(self):
        bug_seq = ["bugid1  ", "bugid2\n"]
        self.buglist.read_bug_list(bug_seq)
        self.check_bugs_exist(['bugid1', 'bugid2'])

    def test_read_bug_list_avoids_duplicates(self):
        bug_seq = ['bugid1', 'bugid1', 'bugid2', 'bugid1']
        self.buglist.read_bug_list(bug_seq)
        self.check_bugs_exist(['bugid1', 'bugid2'])

    def check_bugs_exist(self, expected):
        actual = self.buglist.bugs.keys()
        actual.sort()
        self.assertEquals(expected, actual)


class MockBugFactory(object):
    def get_bug(self, bugid):
        return None
