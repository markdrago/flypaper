import unittest
from datetime import datetime

from buggyfile import BuggyFile


class TestBuggyFile(unittest.TestCase):
    def setUp(self):
        self.filename = 'myfile'
        self.buggyfile = BuggyFile(self.filename)

    def test_buggyfile_stores_filename(self):
        self.assertEquals(self.filename, self.buggyfile.filename)

    def test_buggyfile_stores_bugs(self):
        bug = MockBug()
        self.buggyfile.add_bug(bug)
        self.assertIs(bug, self.buggyfile.bugs.values()[0])

    def test_buggyfile_stores_multiple_bugs(self):
        bug1 = MockBug('bugid1')
        bug2 = MockBug('bugid2')
        self.buggyfile.add_bug(bug1)
        self.buggyfile.add_bug(bug2)
        self.assertEquals(2, len(self.buggyfile.bugs))

    def test_buggyfile_refuses_to_store_duplicate_bug(self):
        bug1 = MockBug('bugid1')
        bug2 = MockBug('bugid1')
        self.buggyfile.add_bug(bug1)
        self.buggyfile.add_bug(bug2)
        self.assertEquals(1, len(self.buggyfile.bugs))

    def test_buggyfile_returns_score_of_zero_when_zero_bugs(self):
        self.assertEquals(0, self.buggyfile.get_score(None))

    def test_buggyfile_returns_score_of_sum_of_bugs_scores(self):
        self.buggyfile.add_bug(MockBug('bugid1', 1))
        self.buggyfile.add_bug(MockBug('bugid2', 2))
        self.buggyfile.add_bug(MockBug('bugid3', 3))
        self.assertEquals(6, self.buggyfile.get_score(None))

    def test_buggyfile_memoizes_score(self):
        bug = MockBug()
        self.buggyfile.add_bug(bug)
        self.buggyfile.get_score(None)
        self.buggyfile.get_score(None)
        self.buggyfile.get_score(None)
        self.assertEquals(1, bug.num_times_score_checked)

    def test_buggyfile_passes_startdate_to_bug_when_checking_score(self):
        dt = datetime(2011, 12, 23, 7, 32, 0)
        bug = MockBug()
        self.buggyfile.add_bug(bug)
        self.buggyfile.get_score(dt)
        self.assertEquals(dt, bug.startdate_checked)


class MockBug(object):
    def __init__(self, bugid='bugid', score=0):
        self.bugid = bugid
        self.score = score
        self.startdate_checked = None
        self.num_times_score_checked = 0

    def get_score(self, startdate):
        self.num_times_score_checked += 1
        self.startdate_checked = startdate
        return self.score
