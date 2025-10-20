"""Unit tests for analyzer module."""

import unittest
from datetime import datetime
from src.analyzer import TrafficAnalyzer


class TestTrafficAnalyzer(unittest.TestCase):
    """Test cases for traffic analyzer."""
    
    def setUp(self):
        """Set up test data."""
        self.sample_records = [
            (datetime(2021, 12, 1, 5, 0, 0), 5),
            (datetime(2021, 12, 1, 5, 30, 0), 12),
            (datetime(2021, 12, 1, 6, 0, 0), 14),
            (datetime(2021, 12, 1, 7, 0, 0), 25),
            (datetime(2021, 12, 2, 5, 0, 0), 10),
            (datetime(2021, 12, 2, 5, 30, 0), 20),
        ]
    
    def test_get_total_cars(self):
        """Test total car count calculation."""
        analyzer = TrafficAnalyzer(self.sample_records)
        total = analyzer.get_total_cars()
        self.assertEqual(total, 5 + 12 + 14 + 25 + 10 + 20)
    
    def test_get_total_cars_empty(self):
        """Test total with empty records."""
        analyzer = TrafficAnalyzer([])
        self.assertEqual(analyzer.get_total_cars(), 0)
    
    def test_get_daily_totals(self):
        """Test daily aggregation."""
        analyzer = TrafficAnalyzer(self.sample_records)
        daily = analyzer.get_daily_totals()
        
        self.assertEqual(len(daily), 2)
        self.assertEqual(daily['2021-12-01'], 5 + 12 + 14 + 25)
        self.assertEqual(daily['2021-12-02'], 10 + 20)
    
    def test_get_daily_totals_sorted(self):
        """Test that daily totals are sorted by date."""
        analyzer = TrafficAnalyzer(self.sample_records)
        daily = analyzer.get_daily_totals()
        
        dates = list(daily.keys())
        self.assertEqual(dates, sorted(dates))
    
    def test_get_top_half_hours(self):
        """Test finding top N half-hour periods."""
        analyzer = TrafficAnalyzer(self.sample_records)
        top3 = analyzer.get_top_half_hours(3)
        
        self.assertEqual(len(top3), 3)
        self.assertEqual(top3[0][1], 25)  # Highest count
        self.assertEqual(top3[1][1], 20)
        self.assertEqual(top3[2][1], 14)
    
    def test_get_top_half_hours_fewer_records(self):
        """Test top N when fewer records exist."""
        records = [
            (datetime(2021, 12, 1, 5, 0, 0), 5),
            (datetime(2021, 12, 1, 5, 30, 0), 12),
        ]
        analyzer = TrafficAnalyzer(records)
        top5 = analyzer.get_top_half_hours(5)
        
        self.assertEqual(len(top5), 2)  # Only 2 records available
    
    def test_get_min_contiguous_period(self):
        """Test finding minimum contiguous period."""
        records = [
            (datetime(2021, 12, 1, 5, 0, 0), 10),
            (datetime(2021, 12, 1, 5, 30, 0), 5),
            (datetime(2021, 12, 1, 6, 0, 0), 3),   # Minimum period starts here
            (datetime(2021, 12, 1, 6, 30, 0), 2),  # 3 + 2 + 4 = 9
            (datetime(2021, 12, 1, 7, 0, 0), 4),   # Minimum period ends here
            (datetime(2021, 12, 1, 7, 30, 0), 20),
        ]
        analyzer = TrafficAnalyzer(records)
        min_period, total = analyzer.get_min_contiguous_period(3)
        
        self.assertEqual(len(min_period), 3)
        self.assertEqual(total, 9)
        self.assertEqual(min_period[0][1], 3)
        self.assertEqual(min_period[1][1], 2)
        self.assertEqual(min_period[2][1], 4)
    
    def test_get_min_contiguous_period_insufficient_records(self):
        """Test minimum period with insufficient records."""
        records = [
            (datetime(2021, 12, 1, 5, 0, 0), 10),
            (datetime(2021, 12, 1, 5, 30, 0), 5),
        ]
        analyzer = TrafficAnalyzer(records)
        
        with self.assertRaises(ValueError) as context:
            analyzer.get_min_contiguous_period(3)
        self.assertIn("Not enough records", str(context.exception))
    
    def test_get_min_contiguous_period_single_window(self):
        """Test with exactly one window."""
        records = [
            (datetime(2021, 12, 1, 5, 0, 0), 10),
            (datetime(2021, 12, 1, 5, 30, 0), 5),
            (datetime(2021, 12, 1, 6, 0, 0), 3),
        ]
        analyzer = TrafficAnalyzer(records)
        min_period, total = analyzer.get_min_contiguous_period(3)
        
        self.assertEqual(len(min_period), 3)
        self.assertEqual(total, 18)


if __name__ == '__main__':
    unittest.main()

