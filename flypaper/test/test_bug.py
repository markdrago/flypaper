import unittest
from datetime import datetime

from bug import Bug


class TestBug(unittest.TestCase):
    def setUp(self):
        self.bugid = 'abc'
        self.bug = Bug(self.bugid)

    def test_bug_stores_bugid(self):
        self.assertEquals(self.bugid, self.bug.bugid)

    def test_bug_stores_fixing_changeset(self):
        changeset = MockChangeset()
        self.bug.add_fixing_changeset(changeset)
        self.assertIs(changeset, self.bug.fixing_changesets.pop())

    def test_bug_stores_multiple_fixing_changesets(self):
        self.bug.add_fixing_changeset(MockChangeset())
        self.bug.add_fixing_changeset(MockChangeset())
        self.assertEquals(2, len(self.bug.fixing_changesets))

    def test_bug_has_score_of_changeset_with_highest_score(self):
        self.bug.add_fixing_changeset(MockChangeset(2))
        self.bug.add_fixing_changeset(MockChangeset(4))
        self.bug.add_fixing_changeset(MockChangeset(3))
        self.assertEquals(4, self.bug.get_score(None))

    def test_bug_passes_startdate_information_to_changeset(self):
        changeset = MockChangeset()
        dt = datetime(2011, 12, 22, 19, 4, 00)
        self.bug.add_fixing_changeset(changeset)
        self.bug.get_score(dt)
        self.assertEquals(dt, changeset.startdate_asked_for)

    def test_bug_returns_zero_for_score_when_no_changesets_fix_it(self):
        self.assertEquals(0, self.bug.get_score(None))

    def test_bug_memoizes_score(self):
        changeset = MockChangeset()
        self.bug.add_fixing_changeset(changeset)
        self.bug.get_score(None)
        self.bug.get_score(None)
        self.bug.get_score(None)
        self.assertEquals(1, changeset.num_times_score_checked)

    def test_bug_to_string(self):
        self.assertEquals(self.bugid, str(self.bug))


class MockChangeset(object):
    def __init__(self, score=0):
        self.score = score
        self.startdate_asked_for = None
        self.num_times_score_checked = 0

    def get_score(self, startdate):
        self.num_times_score_checked += 1
        self.startdate_asked_for = startdate
        return self.score
