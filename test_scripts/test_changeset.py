import unittest

from scripts import changeset


class TestChangeSet(unittest.TestCase):

    def test__parse_filelist(self):
        filelist = """output.txt
firstfile.py
second.rs"""
        inverted = changeset._parse_filelist(filelist)
        self.assertEqual(
            inverted,
            "output.txt firstfile.py second.rs",
        )

