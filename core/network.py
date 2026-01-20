def network_stat():
    """Read network statistics from /proc/net/dev."""
    
    with open('/proc/net/dev', 'r') as f:
        data = f.readlines()
        data = data[2:]  # Skip the first two header lines
        rx_tx = {}
        for line in data:
            parts = line.split()
            iface = parts[0].strip(':')
            rx_bytes = int(parts[1])
            tx_bytes = int(parts[9])
            rx_tx[iface] = (rx_bytes, tx_bytes)

    return rx_tx

def compute_speed(old_stats, new_stats, interval):
    """from two network stats, compute speed in bytes/sec."""

    speeds = {}
    total_rx = 0
    total_tx = 0
    for iface in new_stats.keys():
        if iface in old_stats:
            rx_speed = (new_stats[iface][0] - old_stats[iface][0]) / interval  # bytes per second
            tx_speed = (new_stats[iface][1] - old_stats[iface][1]) / interval  # bytes per second
            speeds[iface] = (rx_speed, tx_speed)
            if iface != 'lo':
                total_rx += rx_speed
                total_tx += tx_speed
    return speeds, total_rx, total_tx

def format_speed(speed_bytes):
    """Format bytes/sec to human-readable KB/s or MB/s."""
    if speed_bytes > 1024 * 1024:
        return f"{speed_bytes / (1024 * 1024):.2f} MB/s"
    else:
        return f"{speed_bytes / 1024:.2f} KB/s"
