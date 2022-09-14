import unittest
from datetime import datetime
from photo import NameMask


class Test_NameTemplate(unittest.TestCase):
    
    def test_create_name(self):
        filename = 'file.png'
        date = datetime(2022, 8, 2, 9, 0, 5)

        self.assertEqual(NameMask('(yy)_(mm)_(dd)_(H)_(MM)_(SS)').create_name(date, filename), '22_08_02_9_00_05.png')
        self.assertEqual(NameMask('(yyyy)_(mm)_(dd)_(H)_(MM)_(SS)').create_name(date, filename), '2022_08_02_9_00_05.png')
        self.assertEqual(NameMask('(yyyy)_(m)_(dd)_(H)_(MM)_(SS)').create_name(date, filename), '2022_8_02_9_00_05.png')
        self.assertEqual(NameMask('(yyyy)_(mm)_(d)_(H)_(MM)_(SS)').create_name(date, filename), '2022_08_2_9_00_05.png')
        self.assertEqual(NameMask('(yyyy)_(mm)_(dd)_(HH)_(MM)_(SS)').create_name(date, filename), '2022_08_02_09_00_05.png')
        self.assertEqual(NameMask('(yyyy)_(mm)_(dd)_(H)_(M)_(SS)').create_name(date, filename), '2022_08_02_9_0_05.png')
        self.assertEqual(NameMask('(yyyy)_(mm)_(dd)_(H)_(MM)_(S)').create_name(date, filename), '2022_08_02_9_00_5.png')
        self.assertEqual(NameMask('(yyyy)_(mm)_(dd)_(H)h(MM)m(SS)s').create_name(date, filename), '2022_08_02_9h00m05s.png')


if __name__ == '__main__':
    unittest.main()
