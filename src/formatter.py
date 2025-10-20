"""Output formatter module."""

from datetime import datetime
from typing import List, Tuple, Dict


def format_results(
    total_cars: int,
    daily_totals: Dict[str, int],
    top_half_hours: List[Tuple[datetime, int]],
    min_period: Tuple[List[Tuple[datetime, int]], int]
) -> str:
    """
    Format analysis results according to specification.
    """
    lines = []
    
    # Total cars
    lines.append("=" * 60)
    lines.append("TOTAL CARS")
    lines.append("=" * 60)
    lines.append(str(total_cars))
    lines.append("")
    
    # Daily totals
    lines.append("=" * 60)
    lines.append("DAILY TOTALS")
    lines.append("=" * 60)
    for date, count in daily_totals.items():
        lines.append(f"{date} {count}")
    lines.append("")
    
    # Top 3 half hours
    lines.append("=" * 60)
    lines.append("TOP 3 HALF HOURS WITH MOST CARS")
    lines.append("=" * 60)
    for timestamp, count in top_half_hours:
        lines.append(f"{timestamp.isoformat()} {count}")
    lines.append("")
    
    # Minimum 1.5 hour period
    lines.append("=" * 60)
    lines.append("MINIMUM 1.5 HOUR PERIOD (3 CONTIGUOUS HALF HOURS)")
    lines.append("=" * 60)
    min_records, total = min_period
    for timestamp, count in min_records:
        lines.append(f"{timestamp.isoformat()} {count}")
    lines.append(f"\nTotal cars in this period: {total}")
    
    return '\n'.join(lines)

