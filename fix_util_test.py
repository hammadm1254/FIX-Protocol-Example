import unittest
import fix_util as sln

class TestFixUtil(unittest.TestCase):
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

        self.assertEqual(sln.get_defs_dict('35=d\x01555=GEH7'), {35 : 'd', 555 : 'GEH7'})

    def test_verify_input(self):
        with self.assertRaises(AssertionError):
            sln.verify_input('23', 'GEH7', [{35 : 'd', 555 : 'GEH7'}])
            sln.verify_input(23, 435345, [{35 : 'd', 555 : 'GEH7'}])
            sln.verify_input(23, 'GEH7', {35: 'd', 555: 'GEH7'})
            sln.verify_input(23, 'GEH7', [])

        sln.verify_input(35, 'GEH7', [{35: 'd', 555: 'GEH7'}])

if __name__ == '__main__':
    unittest.main()