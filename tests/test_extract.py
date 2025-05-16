
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../dags")))

from unittest.mock import patch, MagicMock
from src.extract import extract_breweries

@patch("src.extract.requests.get")
@patch("src.extract.upload_to_s3")
def test_extract_breweries_success(mock_upload, mock_get):
    mock_get.side_effect = [
        MagicMock(status_code=200, json=lambda: [{"id": 1, "name": "Test", "state": "TX"}]),
        MagicMock(status_code=200, json=lambda: [])
    ]
    extract_breweries("20250101")
    assert mock_upload.called
