import os

def get_disk_usage(path):
    """Returns the disk usage statistics about the given path."""
    usage = os.statvfs(path)
    total_space = usage.f_frsize * usage.f_blocks
    free_space = usage.f_frsize * usage.f_bavail
    used_space = total_space - free_space
    return {
        'total_space': total_space,
        'used_space': used_space,
        'free_space': free_space
    }

def get_disk_io_stats():
    """Returns disk I/O statistics (sectors read/written)."""
    io_stats = {}
    try:
        with open('/proc/diskstats', 'r') as f:
            for line in f:
                parts = line.split()
                if len(parts) < 14:
                    continue
                
                device_name = parts[2]

                if device_name.startswith('loop') or device_name.startswith('ram'):
                    continue

                # Index 5 = Sectors Read, Index 9 = Sectors Written
                # 1 Sector = 512 bytes (usually)
                sectors_read = int(parts[5])
                sectors_written = int(parts[9])
                
                io_stats[device_name] = {
                    'read_bytes': sectors_read * 512,
                    'write_bytes': sectors_written * 512
                }
    except (FileNotFoundError, PermissionError):
        return {}

    return io_stats

def bytes_to_gb(bytes):
    return round(bytes / (1024 ** 3), 2)

def bytes_to_mb(bytes):
    return round(bytes / (1024 ** 2), 2)

def calculate_disk_IO_speed(io_stats_old, io_stats_new, interval):
    """Calculate disk I/O speed in bytes per second."""
    speeds = {}
    for device in io_stats_new.keys():
        if device in io_stats_old:
            read_speed = (io_stats_new[device]['read_bytes'] - io_stats_old[device]['read_bytes']) / interval
            write_speed = (io_stats_new[device]['write_bytes'] - io_stats_old[device]['write_bytes']) / interval
            speeds[device] = {
                'read_speed': read_speed,
                'write_speed': write_speed
            }
    return speeds

def total_disk_io_speed(each_disk_io_speeds):
    total_read = 0
    total_write = 0
    for speeds in each_disk_io_speeds.values():
        total_read += speeds['read_speed']
        total_write += speeds['write_speed']
    return total_read, total_write
    