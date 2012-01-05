import unittest

from datetime import datetime

from changeset import Changeset
from bug import Bug
from flypaper import FlyPaper


class TestFlyPaper(unittest.TestCase):
    def setUp(self):
        self.fp = FlyPaper(None, None, datetime(2011, 1, 1, 0, 0, 0), False)

    def test_matching_bugs_with_changesets(self):
        #create two bugs
        bug1id = 'bug1'
        bug1 = Bug(bug1id)
        self.fp._buglist.add(bug1)

        bug2id = 'bug2'
        bug2 = Bug(bug2id)
        self.fp._buglist.add(bug2)

        #only one bug is part of a changeset
        chg1 = Changeset('abc', datetime(2012, 1, 5, 8, 22, 0), bug1id)
        self.fp._changesets.add(chg1)

        self.fp._match_bugs_with_changesets()

        #verify that only that one bug is linked with a changeset
        self.assertEquals(set([chg1]), bug1.fixing_changesets)
        self.assertEquals(0, len(bug2.fixing_changesets))
        self.assertEquals(set([bug1]), chg1.bugs_fixed)
