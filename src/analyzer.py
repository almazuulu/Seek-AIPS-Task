"""Traffic data analyzer module."""

from datetime import datetime
from typing import List, Tuple, Dict
from collections import defaultdict


class TrafficAnalyzer:
    """Analyzes traffic data and computes various statistics."""
    
    def __init__(self, records: List[Tuple[datetime, int]]):
        """
        Initialize analyzer with traffic records.
        """
        self.records = records
    
    def get_total_cars(self) -> int:
        """
        Calculate total number of cars across all records.
        """
        return sum(count for _, count in self.records)
    
    def get_daily_totals(self) -> Dict[str, int]:
        """
        Group traffic by day and sum car counts.
        """
        daily_counts = defaultdict(int)
        
        for timestamp, count in self.records:
            date_str = timestamp.date().isoformat()
            daily_counts[date_str] += count
        
        # Sort by date
        return dict(sorted(daily_counts.items()))
    
    def get_top_half_hours(self, n: int = 3) -> List[Tuple[datetime, int]]:
        """
        Find top N half-hour periods with most cars.
        """
        # Sort by count (descending), then by timestamp (for stability)
        sorted_records = sorted(
            self.records,
            key=lambda x: (-x[1], x[0])
        )
        return sorted_records[:n]
    
    def get_min_contiguous_period(self, window_size: int = 3) -> Tuple[List[Tuple[datetime, int]], int]:
        """
        Find contiguous period with minimum total cars.
        """
        if len(self.records) < window_size:
            raise ValueError(
                f"Not enough records ({len(self.records)}) for window size {window_size}"
            )
        
        min_total = float('inf')
        min_window = []
        
        # Sliding window approach
        for i in range(len(self.records) - window_size + 1):
            window = self.records[i:i + window_size]
            window_total = sum(count for _, count in window)
            
            if window_total < min_total:
                min_total = window_total
                min_window = window
        
        return min_window, min_total
