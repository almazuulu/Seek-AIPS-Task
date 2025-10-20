# Traffic Counter Analysis System

A Python application that analyzes automated traffic counter data and generates comprehensive reports.

## Overview

This system processes traffic counter data files and produces analysis including:
- Total number of cars
- Daily car counts
- Top 3 busiest half-hour periods
- Minimum traffic 1.5-hour period (3 contiguous half-hour records)

## Project Structure

```
Seek-AIPS-Task/
├── src/
│   ├── __init__.py
│   ├── main.py          # Main entry point and CLI
│   ├── parser.py        # File parsing logic
│   ├── analyzer.py      # Traffic analysis algorithms
│   └── formatter.py     # Output formatting
├── tests/
│   ├── __init__.py
│   ├── test_parser.py      # Parser unit tests
│   ├── test_analyzer.py    # Analyzer unit tests
│   ├── test_formatter.py   # Formatter unit tests
│   └── test_integration.py # End-to-end integration tests
├── traffic.txt          # Sample input data
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Requirements

- Python 3.8 or higher
- No external dependencies (uses only standard library)

## Installation

1. Clone or download this repository
2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  
# On Windows: venv\Scripts\activate
```

## Usage

### Basic Usage

Run the application with an input file:

```bash
python -m src.main traffic.txt
```

### Input Format

The input file should contain one record per line in the format:
```
YYYY-MM-DDTHH:MM:SS <count>
```

Example:
```
2021-12-01T05:00:00 5
2021-12-01T05:30:00 12
2021-12-01T06:00:00 14
```

### Output Format

The program outputs results in a well-structured format with clear section headers:

1. **Total Cars**: Overall count of all vehicles
2. **Daily Totals**: Breakdown by date in format `YYYY-MM-DD <count>`
3. **Top 3 Half Hours**: Busiest periods in timestamp format
4. **Minimum 1.5 Hour Period**: Least busy 3 contiguous half-hour records

Example output:
```
============================================================
TOTAL CARS
============================================================
398

============================================================
DAILY TOTALS
============================================================
2021-12-01 179
2021-12-05 81
2021-12-08 134
2021-12-09 4

============================================================
TOP 3 HALF HOURS WITH MOST CARS
============================================================
2021-12-01T07:30:00 46
2021-12-01T08:00:00 42
2021-12-08T18:00:00 33

============================================================
MINIMUM 1.5 HOUR PERIOD (3 CONTIGUOUS HALF HOURS)
============================================================
2021-12-01T15:00:00 9
2021-12-01T15:30:00 11
2021-12-01T23:30:00 0

Total cars in this period: 20
```

## Running Tests

Run all unit and integration tests:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Run specific test modules:

```bash
python -m unittest tests.test_parser
python -m unittest tests.test_analyzer
python -m unittest tests.test_formatter
python -m unittest tests.test_integration
```

## Architecture

### Design Principles

- **Separation of Concerns**: Each module has a single, well-defined responsibility
- **Testability**: All components are independently testable
- **Type Hints**: All functions use type annotations for clarity
- **Error Handling**: Robust validation and informative error messages

### Module Responsibilities

**parser.py**
- Reads and validates input files
- Converts text records to structured data (datetime, count tuples)
- Handles parsing errors with line numbers

**analyzer.py**
- `TrafficAnalyzer` class encapsulates all analysis logic
- Calculates total car counts
- Groups data by day
- Finds top N periods using sorting
- Identifies minimum contiguous periods using sliding window algorithm

**formatter.py**
- Converts analysis results to required output format
- Handles date/datetime formatting consistently

**main.py**
- Coordinates the workflow: parse → analyze → format → output
- Handles command-line arguments
- Manages errors at the application level

## Test Coverage

The test suite includes:

- **Parser Tests** (6 tests): Valid/invalid formats, empty lines, edge cases
- **Analyzer Tests** (9 tests): All calculation methods, edge cases, error handling
- **Formatter Tests** (4 tests): Output formatting, structure validation, edge cases
- **Integration Tests** (2 tests): End-to-end workflow with realistic data

**Total: 21 tests** - All passing ✓

## Algorithms

### Top 3 Half-Hours
- Time Complexity: O(n log n) - sorting-based approach
- Stable sort ensures consistent ordering for ties

### Minimum 1.5-Hour Period
- Time Complexity: O(n) - sliding window approach
- Space Complexity: O(1) - constant extra space
- Efficiently finds the minimum sum of 3 contiguous elements

## Assumptions

- Input files are machine-generated and well-formed (as specified)
- Timestamps are in ISO 8601 format
- Car counts are non-negative integers
- Records may not be in chronological order
- Empty lines in input files are ignored

## Future Enhancements

Possible extensions for production use:
- Support for multiple output formats (JSON, CSV)
- Configurable analysis parameters (window size, top N)
- Data visualization capabilities
- Streaming support for large files
- Performance optimization for massive datasets

## Author

Created by Askarbek Almazbek uulu for SEEK AIPS Coding Challenge
