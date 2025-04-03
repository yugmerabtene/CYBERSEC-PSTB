import socket
import threading

# Liste des requêtes spécifiques par défaut pour détecter les services
SERVICE_QUERIES = {
    21: b'USER anonymous\r\n',  # FTP
    22: b'\n',  # SSH
    25: b'HELO example.com\r\n',  # SMTP
    80: b'HEAD / HTTP/1.1\r\nHost: example.com\r\n\r\n',  # HTTP
    110: b'USER test\r\n',  # POP3
    143: b'LOGIN test test\r\n',  # IMAP
    443: b'HEAD / HTTP/1.1\r\nHost: example.com\r\n\r\n',  # HTTPS
    3306: b'\n',  # MySQL
    3389: b'\x03\x00\x00\x0b\x06\xd0\x00\x00\x12\x34\x00',  # RDP
    5900: b'\n',  # VNC
}


def grab_banner(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)  # Timeout plus long pour certains services lents
            if s.connect_ex((ip, port)) == 0:
                try:
                    # Envoie une requête spécifique si connue, sinon juste un ping vide
                    request = SERVICE_QUERIES.get(port, b'\n')
                    s.sendall(request)

                    banner = s.recv(1024).decode(errors='ignore').strip()
                    if banner:
                        print(f"[+] Port {port} ouvert – Service détecté : {banner}")
                    else:
                        print(f"[+] Port {port} ouvert – Aucune réponse identifiable.")
                except socket.error:
                    print(f"[+] Port {port} ouvert – Impossible de récupérer la bannière.")
    except Exception:
        pass


def scan_ports(ip, start_port, end_port):
    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=grab_banner, args=(ip, port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    ip = input("Entrez l'adresse IP à scanner : ")
    start_port = int(input("Port de début : "))
    end_port = int(input("Port de fin : "))

    scan_ports(ip, start_port, end_port)
