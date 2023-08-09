import socket
import argparse
from ftplib import FTP
import telnetlib3

from smb.SMBConnection import SMBConnection


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


def connect_ftp(ip_address, port):
    try:
        with FTP() as ftp:
            ftp.connect(ip_address, port)
            ftp.login()
            
            server_info = ftp.getwelcome()  # Get server information
            print(f"Server Information for FTP server ({ip_address}:{port}):")
            print(server_info)
            
            # Get the list of files in the FTP root directory
            file_list = ftp.nlst()
            print(f"\nList of files in FTP server ({ip_address}:{port}):")
            for file in file_list:
                print(file)
            
            # Download each file from the server
            for remote_filename in file_list:
                local_filename = "downloaded_" + remote_filename  # Adjust the local file name if needed
                
                try:
                    with open(local_filename, "wb") as local_file:
                        ftp.retrbinary("RETR " + remote_filename, local_file.write)
                        print(f"\nFile '{remote_filename}' downloaded and saved as '{local_filename}'")
                except Exception as download_error:
                    print(f"\nError downloading file '{remote_filename}': {download_error}")
            
            ftp.quit()
            return True
    except Exception as e:
        return False



def connect_telnet(ip_address, port):
    try:
        conn = telnetlib3.open_connection(ip_address, port)
        conn.wait_for_close()
        return True
    except Exception as e:
        return False
#def connect_telnet(ip_address, port):
    try:
        conn = telnetlib3.open_connection(ip_address, port)
        print(f"Telnet connection succeeded for {ip_address}:{port}")
        
        # Lire la bannière du serveur
        server_banner = conn.read_until(b"\n").decode("utf-8")
        print("Server Banner:")
        print(server_banner)
        
        # Attendre l'invite de commande
        conn.wait_for(b"Command Prompt:")
        print("Connected to Command Prompt")
        
        # Envoyer la commande 'help' pour obtenir les commandes et options disponibles
        conn.write("help\r\n")
        commands_info = conn.read_until(b"Command Prompt:").decode("utf-8")
        print("Commands and Options:")
        print(commands_info)
        
        # Envoyer une commande spécifique (par exemple, 'system') pour obtenir des informations sur l'état du système
        conn.write("system\r\n")
        system_info = conn.read_until(b"Command Prompt:").decode("utf-8")
        print("System Status:")
        print(system_info)

        # Envoyer une commande personnalisée (par exemple, 'custom_command') et afficher la réponse
        conn.write("custom_command\r\n")
        custom_response = conn.read_until(b"Command Prompt:").decode("utf-8")
        print("Custom Command Response:")
        print(custom_response)
        
        # Fermer la connexion
        conn.close()
        return True
    except Exception as e:
        print(f"Telnet connection failed for {ip_address}:{port}: {str(e)}")
        return False


def connect_smb(ip_address, port):
    try:
        # Créer une instance de SMBConnection
        smb_connection = SMBConnection('username', 'password', 'client_name', 'server_name', use_ntlm_v2=True)

        # Se connecter au serveur SMB
        if smb_connection.connect(ip_address, port):
            print(f"SMB connection succeeded for {ip_address}:{port}")

            # Exemple : Lister les fichiers dans un répertoire partagé
            share_name = 'ShareName'
            directory = '\\'
            file_list = smb_connection.listPath(share_name, directory)

            print(f"List of files in SMB share {share_name} on {ip_address}:{port}:")
            for file_info in file_list:
                print(file_info.filename)
 # Se déconnecter du serveur SMB
            smb_connection.close()
            return True
        else:
            print(f"SMB connection failed for {ip_address}:{port}")
            return False
    except Exception as e:
        print(f"Error during SMB connection for {ip_address}:{port}: {str(e)}")
        return False

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


            # Tester les ports FTP et Telnet
            for port in open_ports:
                if port == 21:
                    if connect_ftp(ip_address, port):
                        print(f"FTP connection succeeded for {ip_address}:{port}")
                    else:
                        print(f"FTP connection failed for {ip_address}:{port}")
                elif port == 23:
                    if connect_telnet(ip_address, port):
                        print(f"Telnet connection succeeded for {ip_address}:{port}")
                    else:
                        print(f"Telnet connection failed for {ip_address}:{port}")
                elif port == 445:
                    if connect_smb(ip_address, port):
                        print(f"SMB connection succeeded for {ip_address}:{port}")
                    else:
                        print(f"SMB connection failed for {ip_address}:{port}")
        
        # Déterminer le nom du fichier de sortie
        if args.output:
            output_filename = args.output
        else:
            output_filename = "resultats_ports.txt"

        # Enregistre les résultats dans un fichier texte
        save_results_to_file(results, output_filename)

        # Afficher le chemin du fichier sauvegardé
        print(f"-------------------Résultats sauvegardés dans le fichier : {output_filename}-------------------")
