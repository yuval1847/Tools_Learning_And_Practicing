from scapy.all import IP, TCP, sr1, conf, UDP, ICMP
conf.verb = 0  # Disable Scapy verbose output

from config import args
from Techniques_Enum import Techniques


class scannig_techniques:
    """
    A static class which contains several open ports scanning techniques.
    """

    def __new__(cls, *args, **kwargs):
        """
        A function which runs before constructor and prevent initialization.
        """
        raise TypeError(f"{cls.__name__} cannot be instantiated")
    

    @staticmethod
    def scan():
        """
        A function which matched each scanning technics to its right function and returns the scanning results.
        """
        results = []
        target = args.ip
        ports = list(map(int, args.ports.replace(" ", "").split(",")))
        match args.scanning_technics:
            case Techniques.TCP_SYN_SCAN:
                results = scannig_techniques.tcp_syn_scan(target, ports)
            case Techniques.TCP_ACK_SCAN:
                results = scannig_techniques.tcp_ack_scan(target, ports)
            case Techniques.TCP_CONNECT_SCAN:
                results = scannig_techniques.tcp_connect_scan(target, ports)
            case Techniques.UDP_SCAN:
                results = scannig_techniques.udp_scan(target, ports)
            case _:
                raise Exception("There is no such a type scan")
        return results
        

    @staticmethod
    def tcp_syn_scan(target:str, ports:list, timeout:int=1):
        """
        A function which performs a tcp syn scan on the specified ports on the target and returns the results (filtered - no response, probably dropped by firewall, open - the port is open, close - the port is close).
        """
        results = []
        for port in ports:
            pkt = IP(dst=target)/TCP(dport=port, flags="S")
            resp = sr1(pkt, timeout=timeout)
            if resp is None:
                results.append((port, "tcp", "filtered"))  # no response
            elif resp.haslayer(TCP):
                tcp_layer = resp.getlayer(TCP)
                if tcp_layer.flags & 0x12:  # SYN+ACK -> open
                    # Send RST to close
                    rst = IP(dst=target)/TCP(dport=port, flags="R", seq=resp.ack)
                    sr1(rst, timeout=0.5)
                    results.append((port, "tcp", "open"))
                elif tcp_layer.flags & 0x14:  # RST+ACK -> closed
                    results.append((port, "tcp", "closed"))
                else:
                    results.append((port, "tcp", f"unknown_flags:{tcp_layer.flags}"))
            else:
                results.append((port, "tcp", "unknown_response"))
        return results
    
    @staticmethod
    def tcp_ack_scan(target:str, ports:list, timeout:int=1):
        """
        A function which performs a tcp ack scan on the specified ports on the target and returns the results (filtered - no response probably dropped by firewall, unfiltered - the port is open or close (the propuse of this scan is to check if there is a firewall)).
        """
        results = []
        for port in ports:
            pkt = IP(dst=target)/TCP(dport=port, flags="A")
            resp = sr1(pkt, timeout=timeout)
            if resp is None:
                results.append((port, "tcp", "filtered"))
            elif resp.haslayer(TCP):
                tcp_layer = resp.getlayer(TCP)
                if tcp_layer.flags & 0x4:  # RST -> unfiltered
                    results.append((port, "tcp", "unfiltered"))
                else:
                    results.append((port, "tcp", f"unknown_flags:{tcp_layer.flags}"))
            else:
                results.append((port, "tcp", "unknown_response"))
        return results
    
    @staticmethod
    def tcp_connect_scan(target:str, ports:list):
        """
        A function which performs a tcp connect scan on the specified ports on the target.
        """
        results = []
        for port in ports:
            pkt = IP(dst=target)/TCP(dport=port, flags="S")
            if results is None:
                results.append((port, "tcp", "filtered"))
            elif pkt.haslayer(TCP):
                tcp_layer = pkt.getlayer(TCP)
                if tcp_layer.flags & 0x12:  # SYN+ACK -> open
                    results.append((port, "tcp", "open"))
                elif tcp_layer.flags & 0x4:  # RST -> closed
                    results.append((port, "tcp", "closed"))
                else:
                    results.append((port, "tcp", f"unknown_flags:{tcp_layer.flags}"))
            else:
                results.append((port, "tcp", "unknown_response"))
        return results

    @staticmethod
    def udp_scan(target:str, ports:list):
        """
        A function which performs a udp scan on the specified ports on the target.
        """
        results = []
        for port in ports:
            pkt = IP(dst=target)/UDP(dport=port)
            resp = sr1(pkt, timeout=1)
            if resp is None:
                results.append((port, "udp", "open|filtered"))
            elif resp.haslayer(UDP):
                results.append((port, "udp", "open"))
            elif resp.haslayer(ICMP):
                icmp_layer = resp.getlayer(ICMP)
                if icmp_layer.type == 3 and icmp_layer.code == 3:
                    results.append((port, "udp", "closed"))
                elif icmp_layer.type == 3 and icmp_layer.code in [1, 2, 9, 10, 13]:
                    results.append((port, "udp", "filtered"))
                else:
                    results.append((port, "udp", f"unknown_icmp_type_code:{icmp_layer.type}_{icmp_layer.code}"))
            else:
                results.append((port, "udp", "unknown_response"))
        return results


    @staticmethod
    def print_results(results):
        """
        A function which prints the results of the scan.
        """
        print("Results:")
        min_spaces = 6
        spaces_amount = 0
        required_spaces = (min_spaces-3) * " "
        print(f"PORT/PROTOCOL{required_spaces}STATE")
        for port, scanning_protocol, state in sorted(results, key=lambda x: x[0]):
            spaces_amount = min_spaces + (6 - len(str(port)))
            required_spaces = spaces_amount * " "
            print(f"{port}/{scanning_protocol}{required_spaces}{state}")