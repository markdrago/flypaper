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

        #create a few buggy files with different scores
        buggy_file_factory.next_score = 1
        buggy_file_list.add_buggy_file(self.bug1, 'file0')
        buggy_file_factory.next_score = 3
        buggy_file_list.add_buggy_file(self.bug1, 'file1')
        buggy_file_list.add_buggy_file(self.bug2, 'file2')
        buggy_file_factory.next_score = 2
        buggy_file_list.add_buggy_file(self.bug2, 'file3')
        self.fp._buggy_file_list = buggy_file_list

        results = self.fp._get_buggy_files_sorted_by_bugginess()

        self.assertEquals('file1', results[0].filename)
        self.assertEquals('file2', results[1].filename)
        self.assertEquals('file3', results[2].filename)
        self.assertEquals('file0', results[3].filename)

    def test_output_plain_text_without_bugs(self):
        self.fp._showbugs = False
        buggy_files = []
        buggy_files.append(MockBuggyFile('file3', 3.45678))
        buggy_files.append(MockBuggyFile('file2', 2.34321))
        buggy_files.append(MockBuggyFile('file1', 1.2))

        output = self.fp._get_output(buggy_files)
        expected = "3.457 file3\n"
        expected += "2.343 file2\n"
        expected += "1.200 file1\n"
        self.assertEquals(expected, output)

    def test_output_plain_text_with_bugs(self):
        self.fp._showbugs = True
        buggy_files = []
        bf1 = MockBuggyFile('file1', 3.456)
        bf1.add_bug(MockBug('bug1'))
        bf1.add_bug(MockBug('bug2'))
        buggy_files.append(bf1)
        bf2 = MockBuggyFile('file2', 2.345)
        bf2.add_bug(MockBug('bug3'))
        buggy_files.append(bf2)

        output = self.fp._get_output(buggy_files)
        expected = "3.456 file1 bug1,bug2\n"
        expected += "2.345 file2 bug3\n"
        self.assertEquals(expected, output)


class MockBuggyFileFactory(object):
    def __init__(self):
        self.next_score = 0

    def get_buggy_file(self, name):
        return MockBuggyFile(name, self.next_score)


class MockBuggyFile(object):
    def __init__(self, name, score):
        self.score = score
        self.filename = name
        self.bugs = []

    def get_score(self, unused_date):
        return self.score

    def add_bug(self, bug):
        self.bugs.append(bug)

    def get_bugs(self):
        return self.bugs


class MockBug(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
