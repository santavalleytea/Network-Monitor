# main script
import threading
from traffic_monitor import monitor_traffic, get_total_traffic, get_packet_counts
from latency_test import latency_test

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
    threading.Thread(target=monitor_traffic, args=(handle_packet,), daemon=True).start()
    
    
    while True:
        # Show packet traffic
        print("\n------------------------------------------------------------------------------------------------------\n")

        print("----- Total Packet Traffic -----")
        print(f"Total Bytes: {get_total_traffic()} \n")

        print("----- Packet Counts Per IP -----")
        packet_counts = get_packet_counts()
        if packet_counts:
            for ip, counts in packet_counts.items():
                print(f"IP: {ip} | Incoming: {counts['incoming']} | Outgoing: {counts['outgoing']}")

        # Run latency test
        print("\n----- Latency Per IP -----")
        if packet_counts:
            packet_counts_copy = packet_counts.copy() #make copy to avoid RuntimeError

            for ip in packet_counts_copy.keys():
                latency = latency_test(ip)
                if latency is not None:
                    print(f"IP: {ip} | Latency: {latency} ms")
                else:
                    print(f"IP: {ip} | Timed Out")

        print("\n------------------------------------------------------------------------------------------------------\n")


        threading.Event().wait(5) #print packet traffic after some time 

