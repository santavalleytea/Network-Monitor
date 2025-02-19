# main script
import threading
from traffic_monitor import TrafficMonitor

stop_event = threading.Event()
monitor = TrafficMonitor() # Create instance

'''
Callback function to handle network traffic
@params: 
    packet_data (dict)
'''
def handle_packet(packet_data):
    print("Packet Captured:", packet_data)

if __name__ == "__main__":
    #monitor in a separate thread
    monitor_thread = threading.Thread(target=monitor.start_monitoring, args=(handle_packet,), daemon=True)
    monitor_thread.start()

    try:
    #print packet traffic after some time 
        while not stop_event.is_set():
            # print("----- Total Packet Traffic:", get_total_traffic(), "-----")
            # print("Packet Counts Per IP:", get_packet_counts())

            print("\n------------------------------------------------------------------------------------------------------\n")

            print("----- Total Packet Traffic -----")
            print(f"Total Bytes: {monitor.get_total_traffic()} \n")

            print("----- Packet Counts Per IP -----")
            packet_counts = monitor.get_packet_counts()
            if packet_counts:
                for ip, counts in packet_counts.items():
                    print(f"IP: {ip} | Incoming: {counts['incoming']} | Outgoing: {counts['outgoing']}")

            print("\n------------------------------------------------------------------------------------------------------\n")

            stop_event.wait(5)
    
    except KeyboardInterrupt:
        print("\nStopping network monitor...")
        stop_event.set()
        monitor.stop_monitoring()
        monitor_thread.join()
        print("Network monitor stopped.")

