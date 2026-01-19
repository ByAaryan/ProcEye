import os

def get_pids():
    """Retrieve a list of all process IDs (PIDs) on the system."""
    pids = []
    for entry in os.listdir('/proc'):
        if entry.isdigit():
            pids.append(entry)
    return pids

def get_process_name(pid):
    
    """Retrieve the name of the process given their PID."""
    
    try:
        with open(f'/proc/{pid}/comm', 'r') as f:
            return f.read().strip()
    except (FileNotFoundError, PermissionError):
        return None

def status(pid):
    try:
        with open(f'/proc/{pid}/status', 'r') as f:
            proc_data = {}
            for line in f:
                key , value = line.split(':', 1)
                proc_data[key.strip()] = value.strip()
            return proc_data
            
    except (FileNotFoundError, PermissionError):
        return None

def running_processes():
    """Retrieve a list of currently running processes."""
    processes = {}
    for pid in get_pids():
        proc_data = status(pid)
        if proc_data:
            state = proc_data.get('State', 'Unknown')
            proc_memory_inMB = int(proc_data.get('VmRSS', '0 kb').split()[0])/(1024)
            if 'R' in state or 'S' in state or 'D' in state:
                processes[pid] = (proc_data.get('Name', 'Unknown'), proc_memory_inMB)
    return processes
