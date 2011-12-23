from buggyfile import BuggyFileFactory

class BuggyFileList(object):
    def __init__(self):
        self.filenames = {}
        self.buggy_file_factory = BuggyFileFactory

    def add_buggy_file(self, bug, filename):
        if filename not in self.filenames:
            self.filenames[filename] = self.buggy_file_factory.get_buggy_file(filename)
        self.filenames[filename].add_bug(bug)

