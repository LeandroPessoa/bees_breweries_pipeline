
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../dags")))

from unittest.mock import patch, MagicMock
from src.transform import transform_to_silver

@patch("src.transform.create_spark_session")
def test_transform_to_silver_success(mock_spark):
    mock_df = MagicMock()
    mock_df.dropna.return_value = mock_df
    mock_df.select.return_value = mock_df
    mock_spark.return_value.read.json.return_value = mock_df

    result = transform_to_silver("20250101")
    assert result is True
    mock_df.write.format().mode().partitionBy().save.assert_called()
