import socket
import argparse
import asyncio

def dns_lookup(domain_names):
    results = {}

    for domain_name in domain_names:
        try:
            ip_addresses = socket.gethostbyname_ex(domain_name)
            if ip_addresses and ip_addresses[2]:
                results[domain_name] = ip_addresses[2]
            else:
                results[domain_name] = []
        except socket.gaierror as e:
            results[domain_name] = str(e)

    return results

def reverse_dns_lookup(ip_addresses):
    results = {}

    for ip_address in ip_addresses:
        try:
            domain_name = socket.gethostbyaddr(ip_address)[0]
            results[ip_address] = domain_name
        except socket.herror as e:
            results[ip_address] = str(e)

    return results

def format_results(results):
    formatted_results = []
    for key, value in results.items():
        if isinstance(value, list):
            formatted_results.append(f"Résultats de recherche DNS pour le domaine : {key}")
            formatted_results.append("Adresses IP associées :")
            for ip_address in value:
                formatted_results.append(ip_address)
        else:
            formatted_results.append(f"Erreur de résolution DNS pour le domaine : {key} ({value})")
        formatted_results.append("")

    return "\n".join(formatted_results)

def save_results_to_file(results, filename):
    with open(filename, "w") as file:
        for value in results.values():
            if isinstance(value, list):
                for ip_address in value:
                    file.write(ip_address + "\n")

async def perform_dns_lookups(domain_names, reverse_ips, output_file):
    domain_results = dns_lookup(domain_names)
    formatted_domain_results = format_results(domain_results)
    print(formatted_domain_results)

    if output_file:
        save_results_to_file(domain_results, output_file)

    if reverse_ips:
        reverse_results = reverse_dns_lookup(reverse_ips)
        print(format_results(reverse_results))

        if output_file:
            with open(output_file, "a") as file:  # Append to the file for reverse DNS results
                for value in reverse_results.values():
                    if isinstance(value, list):
                        for ip_address in value:
                            file.write(ip_address + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script DNS pour effectuer des recherches de noms de domaine et d'adresses IP.")
    parser.add_argument("domains", nargs="*", help="Noms de domaine à rechercher.")
    parser.add_argument("-r", "--reverse", nargs="*", help="Adresses IP pour effectuer une recherche DNS inverse.")
    parser.add_argument("-o", "--output", default="results.txt", help="Nom du fichier pour enregistrer les résultats. Par défaut, 'results.txt' sera utilisé.")

    args = parser.parse_args()

    domain_names = args.domains
    reverse_ips = args.reverse

    if args.domains and args.domains[0].endswith('.txt'):
        with open(args.domains[0], "r") as file:
            domain_names = [line.strip() for line in file if line.strip()]

    if args.reverse and args.reverse[0].endswith('.txt'):
        with open(args.reverse[0], "r") as file:
            reverse_ips = [line.strip() for line in file if line.strip()]

    if domain_names or reverse_ips:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(perform_dns_lookups(domain_names, reverse_ips, args.output))

    print(f"-------------------Les résultats ont été sauvegardés dans le fichier : {args.output}------------------")
