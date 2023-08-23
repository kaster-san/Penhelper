
import socket




def scan_ports(ip_of_dm):
    open_ports = []
    ports = [21, 22, 23, 25, 53, 80, 81, 135, 139, 143, 161, 194,220, 443, 389, 445, 636, 989, 993, 995, 1080, 1194, 1433, 2222, 3306, 3389, 5432, 5900, 8080 ]
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)  # Définir un délai d'attente pour la connexion (1 seconde dans cet exemple)
                result = s.connect_ex((ip_of_dm, port))
                if result == 0:  # Si la connexion a réussi, le port est ouvert
                    open_ports.append(port)
        except socket.error:
            pass

    return open_ports

def get_service_name(port):
    service_names = {
        21: "ftp",
        22: "ssh",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        81: "Alternate HTTP",
        135: "Microsoft RPC",
        139: "NetBIOS",
        143: "IMAP",
        161: "SNMP (Simple Network Management Protocol)",
        194: "IRC",
        220: "IMAP3",
        389: "LDAP (Lightweight Directory Access Protocol)",
        443: "HTTPS",
        445: "Microsoft-DS",
        636: "LDAPS (LDAP over SSL)",
        989: "FTPS (FTP Secure)",
        993: "IMAPS",
        995: "POP3S",
        1080: "SOCKS Proxy",
        1194: "OpenVPN",
        1433: "Microsoft SQL Server",
        2222: "DirectAdmin",
        3306: "MySQL Server",
        3389: "RDP (Remote Desktop Protocol)",
        5432: "PostgreSQL",
        5900: "VNC (Virtual Network Computing)",
        8080: "HTTP Alternate",
        # Ajoutez d'autres numéros de port et leurs noms de service ici
    }

    return service_names.get(port, "Unknown")

def print_scan_results(ip_of_dm, open_ports):
    if open_ports:
        print(f"Scan report for {ip_of_dm}")
        print("Host is up")
        print("PORT   STATE  SERVICE")
        for port in open_ports:
            service_name = get_service_name(port)
            print(f"{str(port).ljust(6)} open  {service_name}")
        print()