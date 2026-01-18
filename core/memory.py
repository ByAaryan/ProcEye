import os

def check_memory():
    """Check and return the total, free and used memory on the system."""
    mem_info = {}
    try:
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                key, value = line.split(':',1)
                int_value = int(value.split()[0])/(1024*1024)
                mem_info[key.strip()] = int_value
            return mem_info
    except (FileNotFoundError, PermissionError):
        return None

def calculate_memory_usage():
    """Calculate memory usage percentage."""
    mem_data = check_memory()
    mem_stats = {}
    if mem_data:
        mem_stats['MemTotal'] = mem_data.get('MemTotal', 0)
        mem_stats['MemAvailable'] = mem_data.get('MemAvailable', 0)
        mem_stats['MemUsed'] = mem_stats['MemTotal'] - mem_stats['MemAvailable']
        mem_stats['MemUsagePercentage'] = (mem_stats['MemUsed'] / mem_stats['MemTotal']) * 100 if mem_stats['MemTotal'] != 0 else 0
        return mem_stats
    return None
