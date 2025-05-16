import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../dags")))

from unittest.mock import patch, MagicMock
from src.aggregate import aggregate_to_gold

@patch("src.aggregate.create_spark_session")
def test_aggregate_to_gold_success(mock_spark):
    mock_df = MagicMock()
    mock_df.groupBy().count.return_value = mock_df
    mock_spark.return_value.read.format().load.return_value = mock_df

    result = aggregate_to_gold("20250101")
    assert result is True
    mock_df.write.format().mode().partitionBy().save.assert_called()
