import socket
import sys
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
    

    @classmethod
    def scan():
        """
        A function which matched each scanning technics to its right function.
        """
        match args.scanning_technics:
            case Techniques.TCP_SYN_SCAN:
                pass
            case Techniques.TCP_ACK_SCAN:
                pass
            case Techniques.TCP_CONNECT_SCAN:
                pass
            case Techniques.UDP_SCAN:
                pass
            case _:
                raise Exception("There is no such a type scan")
        

    @classmethod
    def tcp_syn_scan(target:str, ports:list):
        """
        A function which performs a tcp syn scan on the specified ports on the target and returns the results.
        """
        results = []
        for i in range(len(ports)):
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            port_state = test_socket.connect_ex((ports[i], target))
            if port_state is None:
                results.append([ports[i], "tcp", "open"])
            results.append([ports[i], "tcp", "close"])
        return results


    @classmethod
    def print_results(results:dict):
        """
        A function which prints the results of the scan.
        """
        print("Results:")
        for i in results:
            print(f"{results[i][0]}/{results[i][1]}    {results[i][2]}")