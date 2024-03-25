import unittest
import os, sys
import sqlite3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from db import *


class TestCompanyFunctions(unittest.TestCase):

    def setUp(self):
        self.test_db = 'test_companies.db'
        connection = sqlite3.connect(self.test_db)
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS icons (icon_id INTEGER PRIMARY KEY, icon BLOB, company_name TEXT, number INTEGER, FOREIGN KEY(company_name) REFERENCES companies(name))')
        cursor.execute('CREATE TABLE IF NOT EXISTS slogans (slogan_id INTEGER PRIMARY KEY, slogan TEXT, company_name TEXT, number INTEGER, FOREIGN KEY(company_name) REFERENCES companies(name))')
        cursor.execute('CREATE TABLE IF NOT EXISTS products (product_id INTEGER PRIMARY KEY, product BLOB, company_name TEXT, number INTEGER, FOREIGN KEY(company_name) REFERENCES companies(name))')
        cursor.execute('CREATE TABLE IF NOT EXISTS companies (name TEXT PRIMARY KEY, description TEXT, logo BLOB, colors TEXT, shape TEXT, mood_board BLOB)')
        cursor.execute('CREATE TABLE IF NOT EXISTS logo (id INTEGER PRIMARY KEY, logo BLOB, logo_number INTEGER)')
        connection.commit()
        connection.close()

    def tearDown(self):
        os.remove(self.test_db)

    def test_insert_company_with_logo(self):
        status = insert_company_with_logo('TestCompany', 'TestDescription', b'TestLogo', 'TestColors', 'TestShape')
        result = get_company_by_name('TestCompany')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 'TestCompany')
        self.assertEqual(result[0][1], 'TestDescription')
        self.assertEqual(result[0][2], b'TestLogo')
        self.assertEqual(result[0][3], 'TestColors')
        self.assertEqual(result[0][4], 'TestShape')
        self.assertEqual(status, "OK")


    def test_update_slogan(self):
        status = insert_company_with_logo('TestCompany', 'TestDescription', b'TestLogo', 'TestColors', 'TestShape')
        update_slogan('TestCompany', 'NewSlogan', 1)
        result = get_slogan('TestCompany', 1)
        self.assertEqual(result, 'NewSlogan')
        self.assertEqual(status, "OK")

    def test_update_product(self):
        status1 = insert_company_with_logo('TestCompany', 'TestDescription', b'TestLogo', 'TestColors', 'TestShape')
        status2 = update_product('TestCompany', b'TestProduct', 1)
        result = get_product('TestCompany', 1)
        self.assertEqual(result, 'VGVzdFByb2R1Y3Q=')
        self.assertEqual(status1, "OK")
        self.assertEqual(status2, "OK")

    def test_update_mood_board(self):
        status1 = insert_company_with_logo('TestCompany', 'TestDescription', b'TestLogo', 'TestColors', 'TestShape')
        status2 = update_mood_board('TestCompany', b'TestMoodBoard')
        result = get_company_moodboard('TestCompany')
        self.assertEqual(result, 'VGVzdE1vb2RCb2FyZA==')
        self.assertEqual(status1, "OK")
        self.assertEqual(status2, "OK")

    def test_get_company_by_name(self):
        status = insert_company_with_logo('TestCompany', 'TestDescription', b'TestLogo', 'TestColors', 'TestShape')
        result = get_company_by_name('TestCompany')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 'TestCompany')
        self.assertEqual(result[0][1], 'TestDescription')
        self.assertEqual(result[0][2], b'TestLogo')
        self.assertEqual(result[0][3], 'TestColors')
        self.assertEqual(result[0][4], 'TestShape')
        self.assertEqual(status, "OK")

    def test_get_company_logo(self):
        status = insert_company_with_logo('TestCompany', 'TestDescription', b'TestLogo', 'TestColors', 'TestShape')
        result = get_company_logo('TestCompany')
        self.assertEqual(result, 'VGVzdExvZ28=')
        self.assertEqual(status, "OK")

    def test_get_company_shape_name(self):
        status = insert_company_with_logo('TestCompany', 'TestDescription', b'TestLogo', 'TestColors', 'TestShape')
        result = get_company_shape_name('TestCompany')
        self.assertEqual(result, 'TestShape')
        self.assertEqual(status, "OK")

    def test_get_company_colors(self):
        status = insert_company_with_logo('TestCompany', 'TestDescription', b'TestLogo', 'TestColors', 'TestShape')
        result = get_company_colors('TestCompany')
        self.assertEqual(result, 'TestColors')
        self.assertEqual(status, "OK")

    def test_get_company_moodboard(self):
        status1 = insert_company_with_logo('TestCompany', 'TestDescription', b'TestLogo', 'TestColors', 'TestShape')
        status2 = update_mood_board('TestCompany', b'TestMoodBoard')
        result = get_company_moodboard('TestCompany')
        self.assertEqual(result, 'VGVzdE1vb2RCb2FyZA==')
        self.assertEqual(status1, "OK")
        self.assertEqual(status2, "OK")

    def test_get_slogan(self):
        status1 = insert_company_with_logo('TestCompany', 'TestDescription', b'TestLogo', 'TestColors', 'TestShape')
        status2 = update_slogan('TestCompany', 'NewSlogan', 1)
        result = get_slogan('TestCompany', 1)
        self.assertEqual(result, 'NewSlogan')
        self.assertEqual(status1, "OK")
        self.assertEqual(status2, "OK")

    def test_get_product(self):
        status1 = insert_company_with_logo('TestCompany', 'TestDescription', b'TestLogo', 'TestColors', 'TestShape')
        status2 = update_product('TestCompany', b'TestProduct', 1)
        result = get_product('TestCompany', 1)
        self.assertEqual(result, 'VGVzdFByb2R1Y3Q=')
        self.assertEqual(status1, "OK")
        self.assertEqual(status2, "OK")

    def test_get_company_products(self):
        insert_company_with_logo('TestCompany', 'TestDescription', b'TestLogo', 'TestColors', 'TestShape')
        status1 = update_product('TestCompany', b'TestProduct1', 1)
        status2 = update_product('TestCompany', b'TestProduct2', 2)
        result = get_company_products('TestCompany')
        self.assertListEqual(result, ['VGVzdFByb2R1Y3Qx', 'VGVzdFByb2R1Y3Qy'])
        self.assertEqual(status1, "OK")
        self.assertEqual(status2, "OK")

if __name__ == '__main__':
    unittest.main()
