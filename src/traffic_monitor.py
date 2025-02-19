# used to monitor the network as a whole: 
#   monitoring incoming and outgoing packets  
#   total traffic in bytes 

from scapy.all import sniff
import threading

total_bytes_in = 0
total_bytes_out = 0
packet_count = {}

'''
Function to monitor incoming packets 
@params: 
    packet: scapy.layers.l2.Ether (captured network packet)
@ret: 
    dict containing source IP, destination IP, and packet size
    else None
'''
def incoming_packets(packet):
    global total_bytes_in 

    if packet.haslayer("IP"):  #ensure that it a IP packet 
        packet_size = len(packet)
        total_bytes_in += packet_size
        data = {
            "type": "incoming",
            "src": packet["IP"].src, #source IP address of packet 
            "dst": packet["IP"].dst, #destination IP address of packet 
            "size": packet_size #size in bytes 
        }
        # print(data)

        #increment incoming packet ip in dictionary 
        dst_ip = packet["IP"].dst
        if dst_ip not in packet_count:
            packet_count[dst_ip] = {'incoming': 0, 'outgoing': 0}
        packet_count[dst_ip]['incoming'] += 1  

        return data
    
    return None 
'''
Function to monitor outgoing packets
@params: 
    packet: scapy.layers.l2.Ether (captured network packet)
@ret: 
    dict containing source IP, destination IP, and packet size
    else None
'''
def outgoing_packets(packet):
    global total_bytes_out

    if packet.haslayer("IP"):  #ensure that it a IP packet 
        packet_size = len(packet)
        total_bytes_out += packet_size
        data = {
            "type": "outgoing",
            "src": packet["IP"].src, #source IP address of packet 
            "dst": packet["IP"].dst, #destination IP address of packet 
            "size": packet_size #size in bytes 
        }
        # print(data)

        #decrement incoming packet ip in dictionary 
        dst_ip = packet["IP"].dst
        if dst_ip not in packet_count:
            packet_count[dst_ip] = {'incoming': 0, 'outgoing': 0}
        packet_count[dst_ip]['outgoing'] += 1  

        return data
    
    return None  #case where packet isn't an IP packet

'''
Function to monitor network traffic - continuously captures packets
@params:
    callback: function that takes a dictionary (packet data) as input
'''
def monitor_traffic(callback=None):
    sniff(prn=lambda packet: process_packet(packet, callback), store=False)


'''
Function to analyse captured packets 
@params: 
    packet: scapy.layers.l2.Ether
    callback: function that takes a dictionary (packet data) as input
'''
def process_packet(packet, callback=None):
    data_in = incoming_packets(packet)
    data_out = outgoing_packets(packet)

    if callback is not None: 
        if data_in is not None:
            callback(data_in) #external function to handle the processed packet data in real-time
        if data_out is not None:
            callback(data_out)

'''
Function to return total traffic statistics
@ret: 
    dict containing total bytes in and out
'''
def get_total_traffic():
    return {
        "total_bytes_in": total_bytes_in,
        "total_bytes_out": total_bytes_out
    }

'''
Function to return total packet incoming and outgoing IP
@ret: 
    dict containing count of incoming and outgoing IP 
'''
def get_packet_counts():
    return packet_count


'''
Function to continuously print total traffic statistics (for debugging)
'''
def print_total_traffic():
    global total_bytes_in
    global total_bytes_out

    while True:
        stats = get_total_traffic()
        print(stats)
        threading.Event().wait(5)  #wait time before printing - to reduce clutter

