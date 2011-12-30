import unittest

from buggyfile_list import BuggyFileList


class BuggyFileListTest(unittest.TestCase):
    def setUp(self):
        self.filelist = BuggyFileList()
        self.mock_buggy_file_factory = MockBuggyFileFactory()
        self.filelist.buggy_file_factory = self.mock_buggy_file_factory

    def test_buggyfile_list_creates_and_stores_buggy_file(self):
        filename = 'myfile'
        mockbug = MockBug()
        self.filelist.add_buggy_file(mockbug, filename)
        self.assertEquals(1, len(self.filelist.filenames))
        actual = self.mock_buggy_file_factory.names_requested
        self.assertEquals(['myfile'], actual)

    def test_buggyfile_list_adds_bug_to_buggy_file(self):
        filename = 'myfile'
        mockbug = MockBug()
        self.filelist.add_buggy_file(mockbug, filename)
        self.assertEquals(1, len(self.filelist.filenames[filename].bugs))
        self.assertEquals(mockbug, self.filelist.filenames[filename].bugs[0])

    def test_buggyfile_reuses_buggyfiles_it_has_already_created(self):
        filename = 'myfile'
        mockbug1 = MockBug()
        mockbug2 = MockBug()
        self.filelist.add_buggy_file(mockbug1, filename)
        self.filelist.add_buggy_file(mockbug2, filename)
        self.assertEquals(1, len(self.filelist.filenames))
        self.assertEquals(2, len(self.filelist.filenames[filename].bugs))


class MockBuggyFileFactory(object):
    def __init__(self):
        self.names_requested = []

    def get_buggy_file(self, filename):
        self.names_requested.append(filename)
        return MockBuggyFile()


class MockBuggyFile(object):
    def __init__(self):
        self.bugs = []

    def add_bug(self, bug):
        self.bugs.append(bug)


class MockBug(object):
    pass
