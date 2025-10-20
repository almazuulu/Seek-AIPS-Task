"""Unit tests for formatter module."""

import unittest
from datetime import datetime
from src.formatter import format_results


class TestFormatter(unittest.TestCase):
    """Test cases for output formatter."""
    
    def test_format_results_complete(self):
        """Test formatting complete results."""
        total_cars = 100
        daily_totals = {
            '2021-12-01': 50,
            '2021-12-02': 30,
            '2021-12-03': 20,
        }
        top_half_hours = [
            (datetime(2021, 12, 1, 8, 0, 0), 25),
            (datetime(2021, 12, 2, 9, 0, 0), 20),
            (datetime(2021, 12, 3, 10, 0, 0), 15),
        ]
        min_period = (
            [
                (datetime(2021, 12, 1, 15, 0, 0), 3),
                (datetime(2021, 12, 1, 15, 30, 0), 2),
                (datetime(2021, 12, 1, 16, 0, 0), 4),
            ],
            9
        )
        
        output = format_results(total_cars, daily_totals, top_half_hours, min_period)
        
        # Check that all sections are present
        self.assertIn('TOTAL CARS', output)
        self.assertIn('DAILY TOTALS', output)
        self.assertIn('TOP 3 HALF HOURS WITH MOST CARS', output)
        self.assertIn('MINIMUM 1.5 HOUR PERIOD', output)
        
        # Check that data is present
        self.assertIn('100', output)
        self.assertIn('2021-12-01 50', output)
        self.assertIn('2021-12-02 30', output)
        self.assertIn('2021-12-03 20', output)
        self.assertIn('2021-12-01T08:00:00 25', output)
        self.assertIn('2021-12-02T09:00:00 20', output)
        self.assertIn('2021-12-03T10:00:00 15', output)
        self.assertIn('2021-12-01T15:00:00 3', output)
        self.assertIn('2021-12-01T15:30:00 2', output)
        self.assertIn('2021-12-01T16:00:00 4', output)
        self.assertIn('Total cars in this period: 9', output)
    
    def test_format_results_single_day(self):
        """Test formatting with single day."""
        total_cars = 20
        daily_totals = {'2021-12-01': 20}
        top_half_hours = [(datetime(2021, 12, 1, 8, 0, 0), 10)]
        min_period = ([(datetime(2021, 12, 1, 15, 0, 0), 5)], 5)
        
        output = format_results(total_cars, daily_totals, top_half_hours, min_period)
        
        # Check sections
        self.assertIn('TOTAL CARS', output)
        self.assertIn('DAILY TOTALS', output)
        
        # Check data
        self.assertIn('20', output)
        self.assertIn('2021-12-01 20', output)
        self.assertIn('2021-12-01T08:00:00 10', output)
        self.assertIn('Total cars in this period: 5', output)
    
    def test_format_results_zero_cars(self):
        """Test formatting with zero total cars."""
        total_cars = 0
        daily_totals = {'2021-12-01': 0}
        top_half_hours = [(datetime(2021, 12, 1, 8, 0, 0), 0)]
        min_period = ([(datetime(2021, 12, 1, 15, 0, 0), 0)], 0)
        
        output = format_results(total_cars, daily_totals, top_half_hours, min_period)
        
        # Check sections are present
        self.assertIn('TOTAL CARS', output)
        
        # Check zero handling
        lines = output.split('\n')
        # Find the line after "TOTAL CARS" header
        total_idx = None
        for i, line in enumerate(lines):
            if 'TOTAL CARS' in line:
                # Skip the separator line and get the value
                total_idx = i + 2
                break
        
        if total_idx:
            self.assertEqual(lines[total_idx], '0')
    
    def test_format_structure(self):
        """Test that output has proper structure with headers."""
        total_cars = 50
        daily_totals = {'2021-12-01': 50}
        top_half_hours = [(datetime(2021, 12, 1, 8, 0, 0), 25)]
        min_period = ([(datetime(2021, 12, 1, 15, 0, 0), 10)], 10)
        
        output = format_results(total_cars, daily_totals, top_half_hours, min_period)
        
        # Verify structure with separators
        self.assertIn('=' * 60, output)
        
        # Count sections (should have 4 main sections)
        section_count = output.count('=' * 60)
        self.assertEqual(section_count, 8)  # 8 separator lines (2 per section)


if __name__ == '__main__':
    unittest.main()
