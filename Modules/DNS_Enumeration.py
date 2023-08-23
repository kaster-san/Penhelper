
import socket



def get_ip_for_domain(domain_name):
    try:
        ip_of_dm = socket.gethostbyname(domain_name)
        return ip_of_dm
    except socket.gaierror as e:
        return str(e)
def print_dns_results(domain_name,dns_result) :
    print(f"The IP of {domain_name} is: ")
    print(f"    {dns_result}")
    
# def dns_lookup(domain_names):
#     results = {}

#     for domain_name in domain_names:
#         try:
#             ip_of_dmes = socket.gethostbyname_ex(domain_name)
#             if ip_of_dmes and ip_of_dmes[2]:
#                 results[domain_name] = ip_of_dmes[2]
#             else:
#                 results[domain_name] = []
#         except socket.gaierror as e:
#             results[domain_name] = str(e)

#     return results

# def reverse_dns_lookup(ip_of_dmes):
#     results = {}

#     for ip_of_dm in ip_of_dmes:
#         try:
#             domain_name = socket.gethostbyaddr(ip_of_dm)[0]
#             results[ip_of_dm] = domain_name
#         except socket.herror as e:
#             results[ip_of_dm] = str(e)

#     return results

# def format_results(results):
#     formatted_results = []
#     for key, value in results.items():
#         if isinstance(value, list):
#             formatted_results.append(f"Résultats de recherche DNS pour le domaine : {key}")
#             formatted_results.append("Adresses IP associées :")
#             for ip_of_dm in value:
#                 formatted_results.append(ip_of_dm)
#         else:
#             formatted_results.append(f"Erreur de résolution DNS pour le domaine : {key} ({value})")
#         formatted_results.append("")

#     return "\n".join(formatted_results)

# def save_results_to_file(results, filename):
#     with open(filename, "w") as file:
#         for value in results.values():
#             if isinstance(value, list):
#                 for ip_of_dm in value:
#                     file.write(ip_of_dm + "\n")

# async def perform_dns_lookups(domain_names, reverse_ips, output_file):
#     domain_results = dns_lookup(domain_names)
#     formatted_domain_results = format_results(domain_results)
#     print(formatted_domain_results)

#     if output_file:
#         save_results_to_file(domain_results, output_file)

#     if reverse_ips:
#         reverse_results = reverse_dns_lookup(reverse_ips)
#         print(format_results(reverse_results))

#         if output_file:
#             with open(output_file, "a") as file:  # Append to the file for reverse DNS results
#                 for value in reverse_results.values():
#                     if isinstance(value, list):
#                         for ip_of_dm in value:
#                             file.write(ip_of_dm + "\n")