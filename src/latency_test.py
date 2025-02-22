# used to determine the latency 
from scapy.all import ICMP, IP, sr1
import time

'''
Function to perform latency test 
@params: 
    target_ip: string  | IP address to ping 
    timeout: int
@ret: 
    latency in ms
    else None
'''
def latency_test(target_ip, timeout=2):
    packet = IP(dst=target_ip)/ICMP() #make ICMP packet

    start_time = time.time()

    reply = sr1(packet, timeout=timeout, verbose=False) #send packet and wait for reply

    end_time = time.time()

    if reply:
        latency_ms = (end_time - start_time) * 1000  #convert to ms
        return round(latency_ms, 2)
    else:
        return None

