class BuggyFile(object):
    def __init__(self, filename):
        self._score = None
        self._bugs = {}
        self.filename = filename

    def add_bug(self, bug):
        if bug.bugid not in self._bugs:
            self._bugs[bug.bugid] = bug

    def get_score(self, startdate):
        '''the score for a file is the sum of the score for the bugs
           which were in it'''
        if self._score is None:
            self._score = sum([bug.get_score(startdate) for bug in self._bugs.values()])
        return self._score

