# ProcEye

A lightweight, custom system monitor for Linux built from scratch in Python. 

Unlike standard monitoring tools that rely on high-level libraries like `psutil`, this project interacts directly with the Linux kernel by parsing the `/proc` filesystem. This project is built with the goal of understanding Linux OS internals such as process management and memory usage, without relying on external monitoring libraries.

## Project Status: Work in Progress
This project is currently in the early stages of development. 
Core functionality is being built incrementally. New features, improvements, and optimizations will be implemented and pushed in upcoming updates.

## Current Features

The monitor currently consists of standalone modules capable of the following:

### Process Management (`processes.py`)
* **PID Retrieval:** Scans `/proc` to identify all active process IDs.
* **Name Resolution:** Maps PIDs to their executable names via `/proc/[pid]/comm`.
* **State Inspection:** Reads `/proc/[pid]/status` to determine if a process is Running, Sleeping, or Idle.
* **Live Reporting:** Filters and displays currently running processes.

### Memory Analysis (`memory.py`)
* **Direct Parsing:** Reads raw data from `/proc/meminfo`.
* **Calculation:** Converts kernel data (kB) into human-readable formats (GB).
* **Usage Stats:** Calculates Total, Free, Available, and Used memory percentages.

## Requirements
* **OS:** Linux (Tested on Arch-based distributions, but should work on any standard Linux kernel).
* **Python:** 3.6+
* **Dependencies:** None (Uses only the Python Standard Library).

## Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/ByAaryan/ProcEye.git](https://github.com/ByAaryan/ProcEye.git)
    cd ProcEye
    ```

2.  **Run the modules:**
    
    To view memory statistics:
    ```bash
    python3 memory.py
    ```

    To view process lists:
    ```bash
    python3 processes.py
    ```