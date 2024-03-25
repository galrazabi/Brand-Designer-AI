import unittest, sys, os
from unittest.mock import patch, MagicMock
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from report import *


class TestReport(unittest.TestCase):

    @patch('report.requests.get')
    def test_get_cashflow_report(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"annualReports": [{"example": "data"}]}
        mock_get.return_value = mock_response
        result = get_cashflow_report("AAPL")
        self.assertEqual(result, {"example": "data"})

    @patch('report.requests.get')
    def test_get_company_overview(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"Description": "Company description"}
        mock_get.return_value = mock_response
        result = get_company_overview("AAPL")
        self.assertEqual(result, "Company description")

    @patch('report.contact_openai')
    def test_make_report(self, mock_contact_openai):
        mock_contact_openai.return_value = "Generated report"
        result = make_report("Apple", {"data": "description"})
        self.assertEqual(result, "Generated report")

    @patch('report.make_report')
    @patch('report.find_similar_companies')
    @patch('report.get_company_overview')
    @patch('report.get_cashflow_report')
    @patch('report.get_google_image')
    @patch('report.get_logo_description')
    @patch('db.update_report')
    def test_create_report(self, mock_update_report, mock_get_logo_description,
                        mock_get_google_image, mock_get_cashflow_report,
                        mock_get_company_overview, mock_find_similar_companies,
                        mock_make_report):
        mock_find_similar_companies.return_value = [("Company1", "Description1", "Symbol1")]
        mock_get_company_overview.return_value = "Company overview"
        mock_get_cashflow_report.return_value = {"cashflow": "data"}
        mock_get_google_image.return_value = "logo_url"
        mock_get_logo_description.return_value = "Logo description"
        mock_update_report.return_value = None
        mock_make_report.return_value = "Generated report"

        result = create_report("Company", "Description")
        expected_data = "Company: Company1\n\nGenerated report"
        self.assertEqual(result, expected_data)
        
if __name__ == '__main__':
    unittest.main()
