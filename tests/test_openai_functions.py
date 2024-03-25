import unittest
import os, sys
from unittest.mock import patch, MagicMock
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from openairequests import *
from db import *

class TestOPENAI(unittest.TestCase):

    @patch('openairequests.contact_dalle')
    @patch('openairequests.get_logo_rate')
    @patch('db.insert_or_replace_logo')
    @patch('db.get_logo_from_logos')
    def test_create_and_find_best_logo(self, mock_get_logo_from_logos, mock_insert_or_replace_logo, mock_get_logo_rate, mock_contact_dalle):
        mock_contact_dalle.side_effect = [("mocked_image_url", "mocked_image_response")] * 3
        mock_get_logo_rate.return_value = 8 
        mock_get_logo_from_logos.return_value = b'mocked_logo_content'

        result = create_and_find_best_logo("Test prompt", "Test Company", "Test description")

        mock_contact_dalle.assert_called()
        self.assertEqual(mock_contact_dalle.call_count, 3)
        mock_insert_or_replace_logo.assert_called()
        self.assertEqual(mock_insert_or_replace_logo.call_count, 3)
        mock_get_logo_rate.assert_called()
        self.assertEqual(mock_get_logo_rate.call_count, 3)
        self.assertEqual(mock_get_logo_from_logos.call_count, 1)
        self.assertEqual(result, b'mocked_logo_content')

    @patch('openairequests.contact_gpt4vision')
    def test_get_logo_rate(self, mock_contact_gpt4vision):
        
        mock_responses = [
            "rate: 7", 
            "rate: 8", 
            "rate: 9", 
            "rate: 10",
            "rate: 6", 
            "rate: 5", 
            "rate: 4", 
            "rate: 3", 
        ]
        mock_contact_gpt4vision.side_effect = mock_responses

        rate = get_logo_rate("Test description", "Test name", "Test image URL")

        expected_rate = 7*1.5 + 8*1.2 + 9*1 + 10*1.3 + 6*1 + 5*0.5 + 4*0.7 + 3*1
        self.assertEqual(rate, expected_rate)

if __name__ == '__main__':
    unittest.main()