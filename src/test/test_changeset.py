import unittest
from datetime import datetime

from changeset import Changeset


class TestChangeset(unittest.TestCase):
    def setUp(self):
        self.commitid = 'commitid'
        self.date = datetime(2011, 12, 30, 17, 59, 0)
        self.desc = 'description goes here'
        self.changeset = Changeset(self.commitid, self.date, self.desc)

    def test_description_contains_finds_substring(self):
        self.assertTrue(self.changeset.description_contains('rip'))

    def test_description_contains_can_return_false(self):
        self.assertFalse(self.changeset.description_contains('blah'))

    def test_add_bug_fixed_stores_bug(self):
        self.changeset.add_bug_fixed('abc')
        self.assertEqual(1, len(self.changeset.bugs_fixed))
        self.assertEqual('abc', self.changeset.bugs_fixed.pop())

    def test_add_bug_fixed_does_not_store_duplicates(self):
        self.changeset.add_bug_fixed('abc')
        self.changeset.add_bug_fixed('abc')
        self.assertEqual(1, len(self.changeset.bugs_fixed))
        self.assertEqual('abc', self.changeset.bugs_fixed.pop())

    def test_add_bug_fixed_increases_bugs_fixed_count(self):
        self.assertEqual(0, self.changeset.bugs_fixed_count())
        self.changeset.add_bug_fixed('abc')
        self.changeset.add_bug_fixed('def')
        self.assertEqual(2, self.changeset.bugs_fixed_count())

    def test_add_modified_file_stores_file(self):
        self.changeset.add_modified_file('file1')
        self.assertEqual(1, len(self.changeset.modified_files))
        self.assertEqual('file1', list(self.changeset.modified_files)[0])
        self.changeset.add_modified_file('file1')
        self.assertEqual(1, len(self.changeset.modified_files))

    def test_date_ratio(self):
        startdate = datetime(2011, 1, 1, 0, 0, 0)
        today = datetime(2011, 12, 31, 23, 59, 59)
        result = self.changeset._get_date_ratio(startdate, today)
        self.assertAlmostEqual(0.99931127, result, 7)

    def test_score_calculation(self):
        result = self.changeset._calculate_score(0.9, 3)
        self.assertAlmostEqual(0.42555748, result, 7)

    def test_get_score(self):
        startdate = datetime(2011, 1, 1, 0, 0, 0)
        self.changeset._today = datetime(2012, 1, 3, 19, 2, 0)
        result = self.changeset.get_score(startdate)
