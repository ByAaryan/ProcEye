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

def bytes_to_gb(bytes):
    return round(bytes / (1024 ** 3), 2)
