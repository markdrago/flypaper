from buggyfile import BuggyFileFactory


class BuggyFileList(object):
    def __init__(self):
        self.filenames = {}
        self.buggy_file_factory = BuggyFileFactory

    def add_buggy_file(self, bug, name):
        if name not in self.filenames:
            self.filenames[name] = self.buggy_file_factory.get_buggy_file(name)
        self.filenames[name].add_bug(bug)
