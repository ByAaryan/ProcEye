import time

def read_all_cpu_stats():
    """Read all CPU statistics from /proc/stat."""
    cpu_stats = {}
    try:
        with open('/proc/stat', 'r') as f:
            for line in f:
                if line.startswith('cpu'):
                    parts = line.split()
                    cpu_id = parts[0]
                    values = list(map(int, parts[1:]))
                    cpu_stats[cpu_id] = values
        return cpu_stats
    except (FileNotFoundError, PermissionError):
        return None


def cpu_usage(core,cpu1,cpu2):
    """Calculate CPU usage percentage."""

    total1 = sum(cpu1[core][0:9])
    total2 = sum(cpu2[core][0:9])
    idle1 = cpu1[core][3]
    idle2 = cpu2[core][3]

    total_diff = total2 - total1
    idle_diff = idle2 - idle1
    
    usage = (total_diff - idle_diff)/total_diff * 100 if total_diff != 0 else 0
    return usage

            
