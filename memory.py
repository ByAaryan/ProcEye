import os

def check_memory():
    """Check and return the total, free and used memory on the system."""
    mem_info = {}
    try:
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                key, value = line.split(':',1)
                int_value_inGB = round(int(value.split()[0])/(1024*1024), 2) 
                mem_info[key.strip()] = int_value_inGB
            return mem_info
    except (FileNotFoundError, PermissionError):
        return None
        
mem_data = check_memory()
mem_used = mem_data['MemTotal'] - mem_data['MemAvailable']
print(f"Total Memory: {mem_data['MemTotal']} GB \nFree Memory: {mem_data['MemAvailable']} GB \nUsed Memory: {mem_used} GB \nUsed: {mem_used/mem_data['MemTotal']*100:.2f}%")