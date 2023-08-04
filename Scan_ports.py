import socket
import argparse

def scan_ports(ip_address, ports):
    open_ports = []

    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)  # Définir un délai d'attente pour la connexion (1 seconde dans cet exemple)
                result = s.connect_ex((ip_address, port))
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

def print_scan_results(ip_address, open_ports):
    if open_ports:
        print(f"Scan report for {ip_address}")
        print("Host is up")
        print("PORT   STATE SERVICE")
        for port in open_ports:
            service_name = get_service_name(port)
            print(f"{str(port).ljust(6)} open  {service_name}")
        print()
  

def save_results_to_file(results, filename):
    with open(filename, "w") as file:
        for ip_address, open_ports in results.items():
            file.write(f"Scan report for {ip_address}\n")
            file.write("Host is up\n")
            file.write("PORT   STATE SERVICE\n")
            for port in open_ports:
                service_name = get_service_name(port)
                file.write(f"{str(port).ljust(6)} open  {service_name}\n")
            file.write("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan des ports ouverts sur une liste d'adresses IP.")
    parser.add_argument("ip_file", help="Fichier contenant les adresses IP à scanner.")
    parser.add_argument("-o", "--output", help="Nom du fichier pour enregistrer les résultats. Si non spécifié, les résultats seront enregistrés dans un fichier par défaut.")
    args = parser.parse_args()

    with open(args.ip_file, "r") as file:
        ip_addresses = [line.strip() for line in file if line.strip()]
        
    if not ip_addresses:
        print("Aucune adresse IP trouvée dans le fichier.")
    else:
        # Liste des ports à scanner (par exemple, [80, 443, 22])
        port_list = [21, 22, 23, 25, 53, 80, 81, 135, 139, 143, 161, 194,220, 443, 389, 445, 636, 989, 993, 995, 1080, 1194, 1433, 2222, 3306, 3389, 5432, 5900, 8080 ]

        results = {}
        for ip_address in ip_addresses:
            open_ports = scan_ports(ip_address, port_list)
            results[ip_address] = open_ports
            print_scan_results(ip_address, open_ports)

        # Déterminer le nom du fichier de sortie
        if args.output:
            output_filename = args.output
        else:
            output_filename = "resultats_ports.txt"

        # Enregistre les résultats dans un fichier texte
        save_results_to_file(results, output_filename)

        # Afficher le chemin du fichier sauvegardé
        print(f"-------------------Résultats sauvegardés dans le fichier : {output_filename}-------------------")