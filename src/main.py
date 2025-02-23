# main script
import threading
import os
from traffic_monitor import TrafficMonitor
from latency_test import latency_test
from speed_test import run_speed_test
from logger import log_data

stop_event = threading.Event()
monitor = TrafficMonitor()
LOG_FILE = "logs.json"

'''
Callback function to handle network traffic
@params: 
    packet_data (dict)
'''
def handle_packet(packet_data):
    # print("Packet Captured:", packet_data)
    pass

if __name__ == "__main__":
    #monitor in a separate thread
    monitor_thread = threading.Thread(target=monitor.start_monitoring, args=(handle_packet,), daemon=True)
    monitor_thread.start()
    
    #print packet traffic after some time 
    try:
        while True:
            print("\n------------------------------------------------------------------------------------------------------\n")

            # Traffic Stats
            traffice_data = monitor.get_total_traffic()
            print("----- Total Packet Traffic -----")
            print(f"Total Bytes: {traffice_data} \n")

            print("----- Packet Counts Per IP -----")
            packet_counts = monitor.get_packet_counts()
            if packet_counts:
                for ip, counts in packet_counts.items():
                    print(f"IP: {ip} | Incoming: {counts['incoming']} | Outgoing: {counts['outgoing']}")
                
            # Run latency test
            print("\n----- Latency Per IP -----")
            latency_data = {}
            if packet_counts:
                packet_counts_copy = packet_counts.copy()  # Make a copy to avoid RuntimeError
                for ip in packet_counts_copy.keys():
                    latency = latency_test(ip)
                    if latency is not None:
                        print(f"IP: {ip} | Latency: {latency} ms")
                    else:
                        print(f"IP: {ip} | Timed Out")

            print("\n------------------------------------------------------------------------------------------------------\n")

            # Run speed test
            print("\n----- Speed Test Per IP -----")
            speed = run_speed_test()
            if speed:
                print(f"Download Speed: {speed['download_speed']} Mbps")
                print(f"Upload Speed: {speed['upload_speed']} Mbps")
            else:
                print("[ERROR] speed test failed.")

            print("\n------------------------------------------------------------------------------------------------------\n")

            log_data(
                monitor.get_total_traffic(),  # Traffic stats
                packet_counts,  # Packet counts per IP
                latency_data,  # Latency test results
                speed  # Speed test results
            )

            stop_event.wait(5)  # Wait 5 seconds before the next print

    except KeyboardInterrupt:
        print("\nStopping network monitor...")
        stop_event.set()
        monitor.stop_monitoring()  # Stop the network sniffer
        monitor_thread.join()  # Ensure the monitoring thread stops
        print("Network monitor stopped.")
        
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
            print(f"{LOG_FILE} deleted.")
        else:
            print(f"{LOG_FILE} not found, no need to delete.")