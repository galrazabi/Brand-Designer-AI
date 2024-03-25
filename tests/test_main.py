import unittest, sys, os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import main

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(main.app)

    @patch('main.generate_new_logo')
    @patch('main.db.insert_company_with_logo')
    def test_create_logo(self, mock_insert_company_with_logo, mock_generate_new_logo):
        mock_generate_new_logo.return_value = b"mocked_generated_logo"
        mock_insert_company_with_logo.return_value = None
        response = self.client.post("/createlogo", json={"name": "TestCompany", "description": "Test description"})
        assert response.status_code == 200
        assert mock_generate_new_logo.called
        assert mock_insert_company_with_logo.called

    @patch('main.generate_new_logo_by_existing_company')
    @patch('main.get_google_image')
    @patch('main.get_logo_description')
    @patch('main.get_logo_colors')
    @patch('main.db.insert_company_with_logo')
    def test_create_logo_inspired_by_existing(self, mock_insert_company_with_logo, mock_get_logo_colors, mock_get_logo_description, mock_get_google_image, mock_generate_new_logo_by_existing_company):
        mock_generate_new_logo_by_existing_company.return_value = b"mocked_generated_logo"
        mock_get_logo_colors.return_value = "blue, green"
        mock_get_logo_description.return_value = "Sample description"
        mock_get_google_image.return_value = "sample_image_url"
        mock_insert_company_with_logo.return_value = None
        response = self.client.post("/createlogoinspiredbyexisting", json={"name": "TestCompany", "description": "Test description", "name_existing_company": "ExistingCompany"})
        assert response.status_code == 200
        assert mock_generate_new_logo_by_existing_company.called
        assert mock_get_logo_colors.called
        assert mock_get_logo_description.called
        assert mock_get_google_image.called
        assert mock_insert_company_with_logo.called

    @patch('main.generate_moodboard_dalle')
    @patch('main.db.update_mood_board')
    def test_create_mood_board(self, mock_update_mood_board, mock_generate_moodboard_dalle):
        mock_generate_moodboard_dalle.return_value = b"mocked_generated_moodboard"
        mock_update_mood_board.return_value = None
        response = self.client.post("/createmoodboard", json={"name": "TestCompany"})
        assert response.status_code == 200

    @patch('main.create_report')
    @patch('main.db.update_report')
    def test_create_compatitors_report(self, mock_update_report, mock_create_report):
        mock_create_report.return_value = "mocked_report"
        mock_update_report.return_value = None
        response = self.client.post("/createreport", json={"name": "TestCompany"})
        assert response.status_code == 200

    @patch('main.generate_new_product')
    @patch('main.db.update_product')
    @patch('main.create_slogans')
    @patch('main.db.get_company_shape_name')
    @patch('main.db.get_company_colors')
    @patch('main.db.get_company_description')
    @patch('main.make_logo_shirt')
    def test_create_products(self, mock_make_logo_shirt, mock_get_company_description, mock_get_company_colors, mock_get_company_shape_name, mock_create_slogans, mock_update_product, mock_generate_new_product):
        mock_get_company_description.return_value = "Test description"
        mock_get_company_colors.return_value = ["blue", "green"]
        mock_get_company_shape_name.return_value = "circle"
        mock_generate_new_product.return_value = b"mocked_generated_product"
        mock_create_slogans.return_value = None
        mock_update_product.return_value = None
        mock_make_logo_shirt.return_value = b"mocked_generated_product"
        response = self.client.post("/createproducts", json={"name": "TestCompany"})
        assert response.status_code == 200
        assert mock_get_company_description.called
        assert mock_get_company_colors.called
        assert mock_get_company_shape_name.called
        assert mock_generate_new_product.called
        assert mock_create_slogans.called
        assert mock_update_product.called

if __name__ == '__main__':
    unittest.main()
