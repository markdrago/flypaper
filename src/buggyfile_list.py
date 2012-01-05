from buggyfile import BuggyFileFactory


class BuggyFileList(object):
    def __init__(self):
        self._filenames = {}
        self._file_factory = BuggyFileFactory

    def get_files(self):
        return self._filenames.values()

    def add_buggy_file(self, bug, name):
        if name not in self._filenames:
            self._filenames[name] = self._file_factory.get_buggy_file(name)
        self._filenames[name].add_bug(bug)
