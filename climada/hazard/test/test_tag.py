"""
Test Tag class
"""

import unittest

from climada.hazard.tag import Tag as TagHazard

class TestAppend(unittest.TestCase):
    """Test loading funcions from the Hazard class"""

    def test_append_right_pass(self):
        """Appends an other tag correctly."""
        tag1 = TagHazard('TC', 'file_name1.mat', 'dummy file 1')
        self.assertEqual('file_name1.mat', tag1.file_name)
        self.assertEqual('dummy file 1', tag1.description)
        self.assertEqual('TC', tag1.haz_type)

        tag2 = TagHazard('TC', 'file_name2.mat', 'dummy file 2')
        
        tag1.append(tag2)
        
        self.assertEqual(['file_name1.mat', 'file_name2.mat'], tag1.file_name)
        self.assertEqual(['dummy file 1', 'dummy file 2'], tag1.description)
        self.assertEqual('TC', tag1.haz_type)

    def test_append_wrong_pass(self):
        """Appends an other tag correctly."""
        tag1 = TagHazard('TC', 'file_name1.mat', 'dummy file 1')
        tag2 = TagHazard('EQ', 'file_name2.mat', 'dummy file 2')
        with self.assertLogs('climada.hazard.tag', level='ERROR') as cm:
            with self.assertRaises(ValueError):
                tag1.append(tag2)
        self.assertIn("Hazards of different type can't be appended: " \
                         + "TC != EQ.", cm.output[0])

    def test_equal_same(self):
        """Appends an other tag correctly."""
        tag1 = TagHazard('TC', 'file_name1.mat', 'dummy file 1')
        tag2 = TagHazard('TC', 'file_name1.mat', 'dummy file 1')
        tag1.append(tag2)        
        self.assertEqual(['file_name1.mat', 'file_name1.mat'], tag1.file_name)
        self.assertEqual(['dummy file 1', 'dummy file 1'], tag1.description)
        self.assertEqual('TC', tag1.haz_type)
        
    def test_append_empty(self):
        """Appends an other tag correctly."""
        tag1 = TagHazard('TC', 'file_name1.mat', 'dummy file 1')
        tag2 = TagHazard()
        tag2.haz_type = 'TC'
        
        tag1.append(tag2)    
        self.assertEqual('file_name1.mat', tag1.file_name)
        self.assertEqual('dummy file 1', tag1.description)
        
        tag1 = TagHazard()
        tag1.haz_type = 'TC'
        tag2 = TagHazard('TC', 'file_name1.mat', 'dummy file 1')
        
        tag1.append(tag2)
        self.assertEqual('file_name1.mat', tag1.file_name)
        self.assertEqual('dummy file 1', tag1.description)
 
class TestJoin(unittest.TestCase):
    """Test joining functions and string formation Tag class."""

    def test_one_str_pass(self):
        """ Test __str__ method with one file"""
        tag = TagHazard('TC', 'file_name1.mat', 'dummy file 1')
        self.assertEqual(str(tag), 
                ' Type: TC\n File: file_name1\n Description: dummy file 1')

    def test_teo_str_pass(self):
        """ Test __str__ method with one file"""
        tag1 = TagHazard('TC', 'file1.mat', 'desc1')
        tag2 = TagHazard('TC', 'file2.xls', 'desc2')
        tag1.append(tag2)
        self.assertEqual(str(tag1), 
                ' Type: TC\n File: file1 + file2\n Description: desc1 + desc2')

    def test_join_names_pass(self):
        """ Test join_file_names function."""
        tag1 = TagHazard('TC', 'file1', 'desc1')
        tag2 = TagHazard('TC', 'file2', 'desc2')
        tag1.append(tag2)
        join_name = tag1.join_file_names()
        self.assertEqual('file1 + file2', join_name)

    def test_join_descr_pass(self):
        """ Test join_descriptions function."""
        tag1 = TagHazard('TC', 'file1', 'desc1')
        tag2 = TagHazard('TC', 'file2', 'desc2')
        tag1.append(tag2)
        join_desc = tag1.join_descriptions()
        self.assertEqual('desc1 + desc2', join_desc)

# Execute Tests
TESTS = unittest.TestLoader().loadTestsFromTestCase(TestAppend)
TESTS.addTests(unittest.TestLoader().loadTestsFromTestCase(TestJoin))
unittest.TextTestRunner(verbosity=2).run(TESTS)
