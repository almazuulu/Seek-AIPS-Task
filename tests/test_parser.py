"""Unit tests for parser module."""

import unittest
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from src.parser import parse_traffic_file


class TestParser(unittest.TestCase):
    """Test cases for traffic file parser."""
    
    def test_parse_valid_file(self):
        """Test parsing a valid traffic file."""
        content = """2021-12-01T05:00:00 5
2021-12-01T05:30:00 12
2021-12-01T06:00:00 14"""
        
        with NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            f.flush()
            temp_path = Path(f.name)
        
        try:
            records = parse_traffic_file(temp_path)
            
            self.assertEqual(len(records), 3)
            self.assertEqual(records[0][0], datetime(2021, 12, 1, 5, 0, 0))
            self.assertEqual(records[0][1], 5)
            self.assertEqual(records[1][1], 12)
            self.assertEqual(records[2][1], 14)
        finally:
            temp_path.unlink()
    
    def test_parse_empty_lines(self):
        """Test parsing file with empty lines."""
        content = """2021-12-01T05:00:00 5

2021-12-01T05:30:00 12"""
        
        with NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            f.flush()
            temp_path = Path(f.name)
        
        try:
            records = parse_traffic_file(temp_path)
            self.assertEqual(len(records), 2)
        finally:
            temp_path.unlink()
    
    def test_parse_zero_count(self):
        """Test parsing records with zero car count."""
        content = "2021-12-01T23:30:00 0"
        
        with NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            f.flush()
            temp_path = Path(f.name)
        
        try:
            records = parse_traffic_file(temp_path)
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0][1], 0)
        finally:
            temp_path.unlink()
    
    def test_parse_invalid_format(self):
        """Test parsing file with invalid format."""
        content = "invalid line"
        
        with NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            f.flush()
            temp_path = Path(f.name)
        
        try:
            with self.assertRaises(ValueError) as context:
                parse_traffic_file(temp_path)
            self.assertIn("Invalid format", str(context.exception))
        finally:
            temp_path.unlink()
    
    def test_parse_negative_count(self):
        """Test parsing file with negative car count."""
        content = "2021-12-01T05:00:00 -5"
        
        with NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            f.flush()
            temp_path = Path(f.name)
        
        try:
            with self.assertRaises(ValueError) as context:
                parse_traffic_file(temp_path)
            self.assertIn("cannot be negative", str(context.exception))
        finally:
            temp_path.unlink()
    
    def test_parse_invalid_timestamp(self):
        """Test parsing file with invalid timestamp."""
        content = "2021-13-01T05:00:00 5"
        
        with NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            f.flush()
            temp_path = Path(f.name)
        
        try:
            with self.assertRaises(ValueError):
                parse_traffic_file(temp_path)
        finally:
            temp_path.unlink()


if __name__ == '__main__':
    unittest.main()

