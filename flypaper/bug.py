class Bug(object):
    def __init__(self, bugid):
        self.score = None
        self.bugid = bugid
        self.fixing_changesets = set()

    def add_fixing_changeset(self, changeset):
        self.fixing_changesets.add(changeset)

    def get_score(self, startdate):
        '''the score for a bug is the score for the latest changeset which
           fixes that bug, since the score for a changeset is based on recency
           alone, we just take the score for the highest scoring changeset'''
        if self.score is None:
            self.score = max([chg.get_score(startdate) for chg in self.fixing_changesets])
        return self.score
    
    def __str__(self):
        return str(self.bugid)

