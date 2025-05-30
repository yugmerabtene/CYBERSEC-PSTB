from scapy.all import sniff, IP, TCP, UDP, ARP, ICMP
import signal
import sys
from collections import defaultdict

# Variables globales pour la détection des scans
tcp_syn_counts = defaultdict(int)
arp_requests = defaultdict(int)


# Fonction de gestion des interruptions
def signal_handler(sig, frame):
    print("\nArrêt du sniffer réseau.")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


# Fonction de détection des scans de ports TCP
def detect_port_scan(packet):
    if packet.haslayer(TCP) and packet[TCP].flags == 2:  # SYN flag
        tcp_syn_counts[packet[IP].src] += 1
        if tcp_syn_counts[packet[IP].src] > 10:
            print(f"[ALERTE] Scan de ports détecté depuis {packet[IP].src}")


# Fonction de détection des requêtes ARP suspectes
def detect_arp_attack(packet):
    if packet.haslayer(ARP) and packet[ARP].op == 1:  # Requête ARP
        arp_requests[packet[ARP].psrc] += 1
        if arp_requests[packet[ARP].psrc] > 5:
            print(f"[ALERTE] Activité ARP suspecte depuis {packet[ARP].psrc}")


# Fonction de détection des pings ICMP
def detect_icmp_scan(packet):
    if packet.haslayer(ICMP) and packet[ICMP].type == 8:  # Echo Request (Ping)
        print(f"[ALERTE] Ping détecté depuis {packet[IP].src} vers {packet[IP].dst}")


# Fonction de traitement des paquets
def packet_handler(packet):
    if packet.haslayer(IP):
        print(f"Paquet capturé: {packet[IP].src} -> {packet[IP].dst} | Protocole: {packet[IP].proto}")

        if packet.haslayer(TCP):
            detect_port_scan(packet)
        elif packet.haslayer(ARP):
            detect_arp_attack(packet)
        elif packet.haslayer(ICMP):
            detect_icmp_scan(packet)


# Lancer la capture des paquets
def start_sniffer():
    print("Démarrage du sniffer réseau...")
    sniff(prn=packet_handler, store=0)


if __name__ == "__main__":
    start_sniffer()
