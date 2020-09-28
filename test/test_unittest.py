import unittest
import main


class Test_CleanString(unittest.TestCase):
    def test_cleanString(self):
        self.assertEqual(main.cleanString(":felipe"), "felipe")


if __name__ == '__main__':
    unittest.main()
