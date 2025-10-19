"""Traffic data parser module."""

from datetime import datetime
from pathlib import Path
from typing import List, Tuple


def parse_traffic_file(file_path: Path) -> List[Tuple[datetime, int]]:
    """
    Parse traffic file and return list of (timestamp, car_count) tuples.
    
    """
    records = []
    
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue
                
            try:
                timestamp_str, count_str = line.split()
                timestamp = datetime.fromisoformat(timestamp_str)
                car_count = int(count_str)
                
                if car_count < 0:
                    raise ValueError(f"Car count cannot be negative: {car_count}")
                    
                records.append((timestamp, car_count))
                
            except ValueError as e:
                raise ValueError(f"Invalid format at line {line_num}: {line}") from e
    
    return records