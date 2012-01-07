import unittest

from datetime import datetime

from changeset import Changeset
from bug import Bug
from buggyfile_list import BuggyFileList
from flypaper import FlyPaper


class TestFlyPaper(unittest.TestCase):
    def setUp(self):
        self.fp = FlyPaper(None, None, datetime(2011, 1, 1, 0, 0, 0), False)

        #create a few bugs and changesets
        bug1id = 'bug1'
        self.bug1 = Bug(bug1id)
        self.fp._buglist.add(self.bug1)

        bug2id = 'bug2'
        self.bug2 = Bug(bug2id)
        self.fp._buglist.add(self.bug2)

        #only one bug is part of a changeset
        self.chg1 = Changeset('abc', datetime(2012, 1, 5, 8, 22, 0), bug1id)
        self.fp._changesets.add(self.chg1)

    def test_matching_bugs_with_changesets(self):
        self.fp._match_bugs_with_changesets()

        #verify that only that one bug is linked with a changeset
        self.assertEquals(set([self.chg1]), self.bug1.fixing_changesets)
        self.assertEquals(0, len(self.bug2.fixing_changesets))
        self.assertEquals(set([self.bug1]), self.chg1.bugs_fixed)

    def test_building_buggy_file_list(self):
        self.chg1.add_modified_file('file1')
        self.chg1.bugs_fixed.add(self.bug1)
        self.fp._build_buggy_file_list()
        self.assertEquals(1, len(self.fp._buggy_file_list._filenames))
        self.assertIn('file1', self.fp._buggy_file_list._filenames)

    def test_sorting_buggy_files_by_bugginess(self):
        buggy_file_list = BuggyFileList()
        buggy_file_factory = MockBuggyFileFactory()
        buggy_file_list._file_factory = buggy_file_factory

        #create two buggy files with score 3, one with score 2
        buggy_file_factory.next_score = 3
        buggy_file_list.add_buggy_file(self.bug1, 'file1')
        buggy_file_list.add_buggy_file(self.bug2, 'file2')
        buggy_file_factory.next_score = 2
        buggy_file_list.add_buggy_file(self.bug2, 'file3')
        self.fp._buggy_file_list = buggy_file_list

        results = self.fp._get_buggy_files_sorted_by_bugginess()

        self.assertIn(3, results)
        actual_with_3 = set([x.name for x in results[3]])
        self.assertEquals(set(('file1', 'file2')), actual_with_3)
        self.assertIn(2, results)
        self.assertEquals('file3', results[2][0].name)


class MockBuggyFileFactory(object):
    def __init__(self):
        self.next_score = 0

    def get_buggy_file(self, name):
        return MockBuggyFile(name, self.next_score)


class MockBuggyFile(object):
    def __init__(self, name, score):
        self.score = score
        self.name = name

    def get_score(self, unused_date):
        return self.score

    def add_bug(self, bug):
        pass
