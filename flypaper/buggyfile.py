class BuggyFile(object):
    def __init__(self, filename):
        self._score = None
        self.bugs = {}
        self.filename = filename

    def add_bug(self, bug):
        if bug.bugid not in self.bugs:
            self.bugs[bug.bugid] = bug

    def get_score(self, startdate):
        '''the score for a file is the sum of the score for the bugs
           which were in it'''
        if self._score is None:
            self._score = sum([bug.get_score(startdate)
                for bug in self.bugs.values()]
            )
        return self._score


class BuggyFileFactory(object):
    @classmethod
    def get_buggy_file(cls, filename):
        return BuggyFile(filename)
