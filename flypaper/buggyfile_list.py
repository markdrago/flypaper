from buggyfile import BuggyFile

class BuggyFileList(object):
    def __init__(self):
        self.filenames = {}

    def add_buggy_file(self, bug, filename):
        if filename not in self.filenames:
            self.filenames[filename] = BuggyFile(filename)
        self.filenames[filename].add_bug(bug)

