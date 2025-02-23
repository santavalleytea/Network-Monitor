# used to log network information 
import json
import os
from datetime import datetime

LOG_FILE = "logs.json"

'''
Initialize log file if it doesn't exist
'''
def initialize_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as file:
            # Empty log list
            json.dump([], file)

def log_data(traffic_data, packet_count, latency_data, speed_data):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "traffic": traffic_data,
        "packets": packet_count,
        "latency": latency_data,
        "speed": speed_data
    }

    # Read file
    with open(LOG_FILE, 'r') as file:
        logs = json.load(file)
    
    logs.append(log_entry)

    # Updated logs
    with open(LOG_FILE, 'w') as file:
        json.dump(logs, file, indent=4)

initialize_log()
