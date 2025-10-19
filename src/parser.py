def parse_traffic_file(file_path):
    """
    Parses the traffic file and returns a list of traffic records.
    """
    records = []
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                timestamp, count = line.split()
                timestamp = datetime.fromisoformat(timestamp)
                count = int(count)
            except ValueError as e:
                raise ValueError(f"Invalid line format: {line} at line {line_num}: {e}")