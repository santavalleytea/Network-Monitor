# main script
import threading
from traffic_monitor import monitor_traffic, get_total_traffic, get_packet_counts

'''
Callback function to handle network traffic
@params: 
    packet_data (dict)
'''
def handle_packet(packet_data):
    print("Packet Captured:", packet_data)

if __name__ == "__main__":
    #monitor in a separate thread
    threading.Thread(target=monitor_traffic, args=(handle_packet,), daemon=True).start()
    
    #print packet traffic after some time 
    while True:
        # print("----- Total Packet Traffic:", get_total_traffic(), "-----")
        # print("Packet Counts Per IP:", get_packet_counts())

        print("\n------------------------------------------------------------------------------------------------------\n")

        print("----- Total Packet Traffic -----")
        print(f"Total Bytes: {get_total_traffic()} \n")

        print("----- Packet Counts Per IP -----")
        packet_counts = get_packet_counts()
        if packet_counts:
            for ip, counts in packet_counts.items():
                print(f"IP: {ip} | Incoming: {counts['incoming']} | Outgoing: {counts['outgoing']}")

        print("\n------------------------------------------------------------------------------------------------------\n")

        threading.Event().wait(5)

