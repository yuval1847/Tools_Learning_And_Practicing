from enum import Enum

class Techniques(Enum):
    """
    An enum which contains the name of each scanning technics.
    """
    TCP_SYN_SCAN = "tcp_syn_scan"
    TCP_ACK_SCAN = "tcp_ack_scan"
    TCP_CONNECT_SCAN = "tcp_connect_scan"
    UDP_SCAN = "udp_scan"