import nmap
import argparse

def scan_network(network_range):
    scanner = nmap.PortScanner()
    scanner.scan(hosts=network_range, arguments="-sn")  # Use -sn for ping scan

    active_hosts = []
    for ip_address in scanner.all_hosts():
        if scanner[ip_address].state() == 'up':
            active_hosts.append(ip_address)

    return active_hosts

def save_results_to_file(active_hosts, output_filename):
    with open(output_filename, "w") as file:
        file.write(f"Nombre d'hôtes actifs : {len(active_hosts)}\n")
        file.write("Adresses IP actives dans le réseau :\n")
        for host in active_hosts:
            file.write(host + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan active hosts in a network.")
    parser.add_argument("network_range", help="Specify the network range to scan (e.g., 10.66.13.0/24).")
    parser.add_argument("-o", "--output", help="Nom du fichier pour enregistrer les résultats. Si non spécifié, les résultats seront enregistrés dans un fichier par défaut.")
    args = parser.parse_args()

    active_hosts = scan_network(args.network_range)
    
    if active_hosts:
        active_hosts.sort()  # Trie les adresses IP par ordre croissant
        
        print(f"\nNombre d'hôtes actifs :   {len(active_hosts)}")
        print("\nAdresses IP actives dans le réseau :")
        for host in active_hosts:
            print(host)

        # Déterminer le nom du fichier de sortie
        if args.output:
            output_filename = args.output
        else:
            output_filename = "active_hosts.txt"

        # Enregistre les adresses IP actives dans un fichier texte
        save_results_to_file(active_hosts, output_filename)

        # Afficher le chemin du fichier sauvegardé
        print(f"\n -------------------Résultats sauvegardés dans le fichier : {output_filename}-------------------")
    else:
        print("Aucun hôte actif trouvé dans le réseau.")


