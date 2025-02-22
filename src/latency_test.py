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
    try:
        packet = IP(dst=target_ip, ttl=64)/ICMP() #make ICMP packet

        start_time = time.time()
        reply = sr1(packet, timeout=timeout, verbose=False) #send packet and wait for reply

        if reply:
            latency_ms = (reply.time - start_time) * 1000  #convert to ms
            return round(latency_ms, 2)
    
    except Exception as e:
        print(f"[ERROR] Failed to ping {target_ip}: {e}")

    return None

