"""Integration tests for traffic counter application."""

import unittest
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile

from src.parser import parse_traffic_file
from src.analyzer import TrafficAnalyzer
from src.formatter import format_results


class TestIntegration(unittest.TestCase):
    """End-to-end integration tests."""
    
    def test_complete_workflow(self):
        """Test complete workflow from file to output."""
        content = """2021-12-01T05:00:00 5
2021-12-01T05:30:00 12
2021-12-01T06:00:00 14
2021-12-01T06:30:00 15
2021-12-01T07:00:00 25
2021-12-01T07:30:00 46
2021-12-01T08:00:00 42
2021-12-05T09:30:00 18
2021-12-05T10:30:00 15
2021-12-05T11:30:00 7"""
        
        with NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            f.flush()
            temp_path = Path(f.name)
        
        try:
            # Parse
            records = parse_traffic_file(temp_path)
            self.assertEqual(len(records), 10)
            
            # Analyze
            analyzer = TrafficAnalyzer(records)
            total = analyzer.get_total_cars()
            daily = analyzer.get_daily_totals()
            top3 = analyzer.get_top_half_hours(3)
            min_period = analyzer.get_min_contiguous_period(3)
            
            # Verify analysis
            self.assertEqual(total, 199)
            self.assertEqual(len(daily), 2)
            self.assertEqual(daily['2021-12-01'], 159)
            self.assertEqual(daily['2021-12-05'], 40)
            
            # Top 3 should be 46, 42, 25
            self.assertEqual(top3[0][1], 46)
            self.assertEqual(top3[1][1], 42)
            self.assertEqual(top3[2][1], 25)
            
            # Format
            output = format_results(total, daily, top3, min_period)
            self.assertIsInstance(output, str)
            
            # Verify output contains all required sections
            self.assertIn('TOTAL CARS', output)
            self.assertIn('DAILY TOTALS', output)
            self.assertIn('TOP 3 HALF HOURS', output)
            self.assertIn('MINIMUM 1.5 HOUR PERIOD', output)
            
            # Verify data is present
            self.assertIn('199', output)
            self.assertIn('2021-12-01 159', output)
            self.assertIn('2021-12-05 40', output)
            
        finally:
            temp_path.unlink()
    
    def test_sample_file_from_spec(self):
        """Test with the exact sample from specification."""
        content = """2021-12-01T05:00:00 5
2021-12-01T05:30:00 12
2021-12-01T06:00:00 14
2021-12-01T06:30:00 15
2021-12-01T07:00:00 25
2021-12-01T07:30:00 46
2021-12-01T08:00:00 42
2021-12-01T15:00:00 9
2021-12-01T15:30:00 11
2021-12-01T23:30:00 0
2021-12-05T09:30:00 18
2021-12-05T10:30:00 15
2021-12-05T11:30:00 7
2021-12-05T12:30:00 6
2021-12-05T13:30:00 9
2021-12-05T14:30:00 11
2021-12-05T15:30:00 15
2021-12-08T18:00:00 33
2021-12-08T19:00:00 28
2021-12-08T20:00:00 25
2021-12-08T21:00:00 21
2021-12-08T22:00:00 16
2021-12-08T23:00:00 11
2021-12-09T00:00:00 4"""
        
        with NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            f.flush()
            temp_path = Path(f.name)
        
        try:
            # Complete workflow
            records = parse_traffic_file(temp_path)
            analyzer = TrafficAnalyzer(records)
            
            total = analyzer.get_total_cars()
            daily = analyzer.get_daily_totals()
            top3 = analyzer.get_top_half_hours(3)
            min_period = analyzer.get_min_contiguous_period(3)
            
            # Verify key results
            self.assertEqual(total, 398)
            self.assertEqual(len(daily), 4)
            
            # Verify daily totals
            self.assertEqual(daily['2021-12-01'], 179)
            self.assertEqual(daily['2021-12-05'], 81)
            self.assertEqual(daily['2021-12-08'], 134)
            self.assertEqual(daily['2021-12-09'], 4)
            
            # Top 3: 46, 42, 33
            self.assertEqual(top3[0][1], 46)
            self.assertEqual(top3[1][1], 42)
            self.assertEqual(top3[2][1], 33)
            
            # Format output
            output = format_results(total, daily, top3, min_period)
            
            # Verify output contains all sections and data
            self.assertIn('TOTAL CARS', output)
            self.assertIn('DAILY TOTALS', output)
            self.assertIn('TOP 3 HALF HOURS', output)
            self.assertIn('MINIMUM 1.5 HOUR PERIOD', output)
            
            # Verify all key data is present
            self.assertIn('398', output)
            self.assertIn('2021-12-01 179', output)
            self.assertIn('2021-12-05 81', output)
            self.assertIn('2021-12-08 134', output)
            self.assertIn('2021-12-09 4', output)
            
            # Verify top 3 entries
            self.assertIn('2021-12-01T07:30:00 46', output)
            self.assertIn('2021-12-01T08:00:00 42', output)
            self.assertIn('2021-12-08T18:00:00 33', output)
            
        finally:
            temp_path.unlink()


if __name__ == '__main__':
    unittest.main()

