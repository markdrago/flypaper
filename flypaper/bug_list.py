from bug import BugFactory

class BugList(object):
    def __init__(self):
        self.bug_factory = BugFactory
        self.bugs = {}

    def read_bug_list(self, bugid_file):
        for line in bugid_file:
            bugid = line.strip()
            bug = self.bug_factory.get_bug(bugid)
            self.bugs[bugid] = bug

