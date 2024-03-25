import unittest
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools import *

class TestFunctions(unittest.TestCase):

    def test_get_color_from_csv(self):
        colors = get_color_from_csv()
        self.assertTrue(len(colors) > 0)
        self.assertIsInstance(colors[0], str)

    def test_get_random_colors(self):
        colors = get_random_colors()
        self.assertEqual(len(colors), 3)
        for color in colors:
            self.assertIsInstance(color, str)

    def test_get_random_shapes(self):
        shape = get_random_shapes()
        self.assertIn(shape, shapes)

    def test_read_logos_file(self):
        logos = read_logos_file()
        self.assertTrue(len(logos) > 0)
        for logo in logos:
            self.assertIsInstance(logo, list)
            self.assertTrue(len(logo) > 0)

    def test_make_and_load_pickle_file(self):
        data = ["test data"]
        file_path = "./test_data.pickle"
        make_pickle_file(data, file_path)
        self.assertTrue(os.path.exists(file_path))
        loaded_data = load_pickle_file(file_path)
        os.remove(file_path)
        self.assertEqual(data, loaded_data)

if __name__ == "__main__":
    unittest.main()
