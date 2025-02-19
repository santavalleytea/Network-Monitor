# used to monitor the network as a whole: 
#   monitoring incoming and outgoing packets  
#   total traffic in bytes 
from scapy.all import AsyncSniffer
import threading

class TrafficMonitor:
    def __init__(self):
        self.total_bytes_in = 0
        self.total_bytes_out = 0
        self.packet_count = {}
        self.stop_monitor = threading.Event()
        self.sniffer = None
        self.lock = threading.Lock()

    '''
    Function to monitor incoming packets 
    @params:         self.packet_out = {}

        packet: scapy.layers.l2.Ether (captured network packet)
    @ret: 
        dict containing source IP, destination IP, and packet size
        else None
    '''
    def incoming_packets(self, packet):
        if packet.haslayer("IP"):  #ensure that it a IP packet 
            packet_size = len(packet)
            with self.lock:
                self.total_bytes_in += packet_size

                #increment incoming packet ip in dictionary 
                dst_ip = packet["IP"].dst
                if dst_ip not in self.packet_count:
                    self.packet_count[dst_ip] = {'incoming': 0, 'outgoing': 0}
                self.packet_count[dst_ip]['incoming'] += 1  

            return {
                "type": "incoming",
                "src": packet["IP"].src, #source IP address of packet 
                "dst": packet["IP"].dst, #destination IP address of packet 
                "size": packet_size #size in bytes 
            }
        return None 
    
    '''
    Function to monitor outgoing packets
    @params: 
        packet: scapy.layers.l2.Ether (captured network packet)
    @ret: 
        dict containing source IP, destination IP, and packet size
        else None
    '''
    def outgoing_packets(self, packet):
        if packet.haslayer("IP"):  #ensure that it a IP packet 
            packet_size = len(packet)
            with self.lock:
                self.total_bytes_out += packet_size

                #decrement incoming packet ip in dictionary 
                dst_ip = packet["IP"].dst
                if dst_ip not in self.packet_count:
                    self.packet_count[dst_ip] = {'incoming': 0, 'outgoing': 0}
                self.packet_count[dst_ip]['outgoing'] += 1  

            return {
                "type": "outgoing",
                "src": packet["IP"].src, #source IP address of packet 
                "dst": packet["IP"].dst, #destination IP address of packet 
                "size": packet_size #size in bytes 
            }
        return None

    '''
    Function to monitor network traffic - continuously captures packets
    @params:
        callback: function that takes a dictionary (packet data) as input
    '''
    def start_monitoring(self, callback=None):
        self.sniffer = AsyncSniffer(prn=lambda packet: self.process_packet(packet, callback), store=False)
        self.sniffer.start()

    def stop_monitoring(self):
        print("Stopping packet sniffing...")
        self.stop_monitor.set()
        if self.sniffer:
            self.sniffer.stop()

    '''
    Function to analyse captured packets 
    @params: 
        packet: scapy.layers.l2.Ether
        callback: function that takes a dictionary (packet data) as input
    '''
    def process_packet(self, packet, callback=None):
        data_in = self.incoming_packets(packet)
        data_out = self.outgoing_packets(packet)

        if callback: 
            if data_in:
                callback(data_in) #external function to handle the processed packet data in real-time
            if data_out:
                callback(data_out)

    '''
    Function to return total traffic statistics
    @ret: 
        dict containing total bytes in and out
    '''
    def get_total_traffic(self):
        return {
            "total_bytes_in": self.total_bytes_in,
            "total_bytes_out": self.total_bytes_out
        }

    '''
    Function to return total packet incoming and outgoing IP
    @ret: 
        dict containing count of incoming and outgoing IP 
    '''
    def get_packet_counts(self):
        return self.packet_count