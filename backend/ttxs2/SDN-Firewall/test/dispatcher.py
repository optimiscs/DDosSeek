from scapy.all import *
import sys
import socket
import fcntl

pcap_file = "./pcap/test2-dos.pcap"


def get_ip(iface):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),
                                        0x8915,
                                        struct.pack("256s", iface[:15]))[20:24])


def dispatch():
    pkts = rdpcap(pcap_file)
    n = len(pkts)
    print("#### pcap file contains", n, "packets.")
    n = min(len(pkts), 10)
    for i in range(n):
        pkt = pkts[i]
        
        if pkt[TCP].dport != 80:
            src = "00:00:00:00:00:01"
            dst = "00:00:00:00:00:02"
            s_ip = "10.0.0.1"
            d_ip = "10.0.0.2"
        else: 
            src = "00:00:00:00:00:02"
            dst = "00:00:00:00:00:01"
            s_ip = "10.0.0.2"
            d_ip = "10.0.0.1"
        
        pkt[Ether].src = src
        pkt[Ether].dst = dst
        pkt[IP].src = s_ip
        pkt[IP].dst = d_ip

        # reset to recalculate
        pkt[IP].len = None
        pkt[IP].checksum = None
        pkt[TCP].len = None
        pkt[TCP].checksum = None
        sendp(pkt, iface='h2-eth0')


if __name__ == '__main__':
    pcap_file = sys.argv[1]
    dispatch()
