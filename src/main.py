"""
Traffic Counter - Main Entry Point

Reads traffic data from file and makes analys reports
"""

import argparse
import sys
from pathlib import Path

from .parser import parse_traffic_file
from .analyzer import TrafficAnalyzer
from .formatter import format_results


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Analyze traffic counter data from a file.'
    )
    parser.add_argument(
        'input_file',
        type=str,
        help='Path to the input file with traffic data'
    )
    return parser.parse_args()


def main():
    """Main execution function."""
    try:
        # Parsing command line argumens
        args = parse_arguments()
        
        # Checking file existence
        input_path = Path(args.input_file)
        if not input_path.exists():
            print(f"Error: File '{args.input_file}' not found.", file=sys.stderr)
            sys.exit(1)
            
        # 1. Reading and parsing the input file
        traffic_records = parse_traffic_file(input_path)
        
        # 2. Analyzing traffic data
        analyzer = TrafficAnalyzer(traffic_records)
        total_cars = analyzer.get_total_cars()
        daily_totals = analyzer.get_daily_totals()
        top_half_hours = analyzer.get_top_half_hours(3)
        min_period = analyzer.get_min_contiguous_period(3)
        
        # 3. Fomratting and outputting results
        output = format_results(total_cars, daily_totals, top_half_hours, min_period)
        print(output)
        
        
    except ValueError as e:
        print(f"Error: Invalid data format - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()