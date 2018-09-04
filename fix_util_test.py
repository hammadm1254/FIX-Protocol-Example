import unittest
import fix_util as sln

class TestFixUtil(unittest.TestCase):
    def setUp(self):
        self.defList = [{35: 'd', 555: 'GEH7'}, {35: 'd', 555: 'blah'}, {35: 'd'}]

    def test_load_files(self):
        with self.assertRaises(ValueError):
            sln.load_files('')
            sln.load_files([])

        self.assertEqual(len(sln.load_files(['secdef.dat'])), 250000)

    def test_get_defs_dict(self):
        with self.assertRaises(ValueError):
            sln.get_defs_dict([])
            sln.get_defs_dict('')
            sln.get_defs_dict('asdgfs')

        with self.assertRaises(TypeError):
            sln.get_defs_dict('32=f\x01555=GEH')

        self.assertEqual(sln.get_defs_dict('35=d\x01555=GEH7'), {35: 'd', 555: 'GEH7'})

    def test_verify_input(self):
        with self.assertRaises(AssertionError):
            sln.verify_input('23', 'GEH7', [{35: 'd', 555: 'GEH7'}])
            sln.verify_input(23, 435345, [{35: 'd', 555: 'GEH7'}])
            sln.verify_input(23, 'GEH7', {35: 'd', 555: 'GEH7'})
            sln.verify_input(23, 'GEH7', [])

        sln.verify_input(35, 'GEH7', [{35: 'd', 555: 'GEH7'}])

    def test_get_defs_by_tag_value(self):
        self.assertEqual(sln.get_defs_by_tag_value(555, 'GEH7', self.defList), [self.defList[0]],
                         'The return value does not contain matching tag-value pairs')
        self.assertEqual(sln.get_defs_by_tag_value(6937, 'GEH7', self.defList), [],
                         'The return value should be an empty list for this test case')

    def test_count_defs_by_tag_value(self):
        self.assertEqual(sln.count_defs_by_tag_value(35, 'd', self.defList), 3,
                         'Count of definitions returned does not match expected count for'
                         'specific tag/value pair')
        self.assertEqual(sln.count_defs_by_tag_value(555, 'blah', self.defList), 1,
                         'Count of definitions returned does not match expected count for'
                         'specific tag/value pair')
        self.assertEqual(sln.count_defs_by_tag_value(555, 'foo', self.defList), 0,
                         'Count of definitions returned does not match expected count for'
                         'specific tag/value pair')

    def test_get_defs_by_tag(self):
        self.assertEqual(sln.get_defs_by_tag(555, self.defList), self.defList[:2],
                         'The return value does not contain matching tag')
        self.assertEqual(sln.get_defs_by_tag(6937, self.defList), [],
                         'The return value should be an empty list for this test case')

    def test_count_defs_by_tag(self):
        self.assertEqual(sln.count_defs_by_tag(555, self.defList), 2,
                         'The count of defs with matching tag does not match expected count')
        self.assertEqual(sln.count_defs_by_tag(6937, self.defList), 0,
                         'The count of defs with matching tag does not match expected count')
        self.assertEqual(sln.count_defs_by_tag(35, self.defList), 3,
                         'The count of defs with matching tag does not match expected count')

    def test_count_values_by_tag(self):
        self.assertEqual(sln.count_values_by_tag(555, self.defList), {'GEH7': 1, 'blah': 1},
                         'The count dictionary is a mis-match for the mock data')
        self.assertEqual(sln.count_values_by_tag(555, self.defList), {'GEH7': 1, 'blah': 1},
                         'The count dictionary is a mis-match for the mock data')

    def test_get_values_of_tag(self):
        self.assertEqual(sln.get_values_of_tag(555, self.defList), ['GEH7', 'blah'],
                         'The list of values for tag is a mis-match for the mock data')

    def test_join_by_tag(self):
        self.assertEqual(sln.join_by_tag(35, 555, self.defList),
                         {'555=GEH7': {'d': 1},
                          '555=blah': {'d': 1}},
                         'The join is done incorrectly')
        self.assertEqual(sln.join_by_tag(555, 35, self.defList),
                         {'35=d': {'GEH7': 1, 'blah': 1}},
                         'The join is done incorrectly')

    def test_sort_by_tag(self):
        self.assertEqual(sln.sort_by_tag(555, self.defList),
                         [{35: 'd'}, {35: 'd', 555: 'blah'}, {35: 'd', 555: 'GEH7'}],
                         'The sorting is done incorrectly')

    def test_get_defs_excluding_tag(self):
        self.assertEqual(sln.get_defs_excluding_tag(555, self.defList), [self.defList[-1]],
                         'The list of defs do not exclude the correct tag')

    def test_get_defs_excluding_tag_value(self):
        self.assertEqual(sln.get_defs_excluding_tag_value(555, 'GEH7', self.defList),
                         self.defList[1:],
                         'The list of defs do not exclude the correct tag-value pair')
        self.assertEqual(sln.get_defs_excluding_tag_value(35, 'd', self.defList),
                         [],
                         'The list of defs do not exclude the correct tag-value pair')
        self.assertEqual(sln.get_defs_excluding_tag_value(555, 'foo', self.defList),
                         self.defList,
                         'The list of defs do not exclude the correct tag-value pair')

if __name__ == '__main__':
    unittest.main()