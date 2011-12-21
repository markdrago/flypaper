class ChangesetList(object):
    def __init__(self):
        self.changesets = {}

    def add(self, changeset):
        self.changesets[changeset.commitid] = changeset

    def remove_changesets_which_do_not_fix_a_bug(self):
        changesets_with_bugs_fixed = {}
        for commit_id in self.changesets:
            if len(self.changesets[commit_id].bugs_fixed) > 0:
                changesets_with_bugs_fixed[commit_id] = self.changesets[commit_id]
        self.changesets = changesets_with_bugs_fixed

