#!/usr/bin/env python3
import argparse
import requests
import webtech
import json
from bs4 import BeautifulSoup
import socket
import asyncio
import re
from urllib.parse import urljoin, urlparse, parse_qs , urlencode

#-------------------------------------------------tech detection functions-----------------------------------------------#
def scan_website(url):
    try:
        response = requests.get(url, timeout=10)  # Set the timeout value here (in seconds)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        wt = webtech.WebTech(options={'json': True})
        report = wt.start_from_url(url)
        return report
    except requests.exceptions.RequestException as e:
        print(f"Error scanning {url}: {e}")
        return None
    except webtech.utils.ConnectionException as e:
        print(f"Connection error scanning {url}: {e}")
        return None
#-------------------------------------------------subdomain enumeration functions-----------------------------------------------#
def clean_domain(domain):
    # Remove 'https://' if present at the beginning
    if domain.startswith("https://"):
        domain = domain[8:]

    # Remove 'http://' if present at the beginning
    if domain.startswith("http://"):
        domain = domain[7:]

    # Remove '/' at the end of the domain
    if domain.endswith("/"):
        domain = domain[:-1]

    return domain

def extract_subdomains_from_td(subdomain_td):
    subdomains = set()

    subdomain_list = subdomain_td.split("<br/>")
    for subdomain in subdomain_list:
        subdomain = subdomain.strip()
        if subdomain and "*" not in subdomain:
            subdomains.add(subdomain)

    return subdomains

def crtsh_subdomain_enum(domain):
    domain = clean_domain(domain)
    base_url = "https://crt.sh/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://crt.sh/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers',
    }
    subdomains = set()

    try:
        response = requests.get(f"{base_url}?q=%.{domain}", headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        rows = soup.select("table tr")[1:]  # Skip the header row
        for row in rows:
            columns = row.select("td")
            if len(columns) >= 5:  # Ensure there are enough columns in the row
                subdomain_td = columns[5].decode_contents()  # Get the inner HTML of the <td> element
                subdomains |= extract_subdomains_from_td(subdomain_td)

        return subdomains

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
    except Exception as e:
        print(f"Error: {e}")

    return set()

#-------------------------------------------------DNS resolution functions-----------------------------------------------#
# def dns_lookup(domain_names):
#     results = {}

#     for domain_name in domain_names:
#         try:
#             ip_addresses = socket.gethostbyname_ex(domain_name)
#             if ip_addresses and ip_addresses[2]:
#                 results[domain_name] = ip_addresses[2]
#             else:
#                 results[domain_name] = []
#         except socket.gaierror as e:
#             results[domain_name] = str(e)

#     return results

# def reverse_dns_lookup(ip_addresses):
#     results = {}

#     for ip_address in ip_addresses:
#         try:
#             domain_name = socket.gethostbyaddr(ip_address)[0]
#             results[ip_address] = domain_name
#         except socket.herror as e:
#             results[ip_address] = str(e)

#     return results

# def format_results(results):
#     formatted_results = []
#     for key, value in results.items():
#         if isinstance(value, list):
#             formatted_results.append(f"Résultats de recherche DNS pour le domaine : {key}")
#             formatted_results.append("Adresses IP associées :")
#             for ip_address in value:
#                 formatted_results.append(ip_address)
#         else:
#             formatted_results.append(f"Erreur de résolution DNS pour le domaine : {key} ({value})")
#         formatted_results.append("")

#     return "\n".join(formatted_results)

# def save_results_to_file(results, filename):
#     with open(filename, "w") as file:
#         for value in results.values():
#             if isinstance(value, list):
#                 for ip_address in value:
#                     file.write(ip_address + "\n")

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
#                         for ip_address in value:
#                             file.write(ip_address + "\n")
def get_ip_for_domain(domain_name):
    try:
        ip_address = socket.gethostbyname(domain_name)
        return ip_address
    except socket.gaierror as e:
        return str(e)
def print_dns_results(domain_name,dns_result) :
    print(f"The IP of {domain_name} is: ")
    print(f"    {dns_result}")
    
#-------------------------------------------------Endpoints enumeration functions-----------------------------------------------#
def get_endpoints_recursive(url, discovered_endpoints=None):
    paths_with_parameters = []
    if discovered_endpoints is None:
        discovered_endpoints = set()

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find all anchor tags
            anchor_tags = soup.find_all('a', href=True)
            for tag in anchor_tags:
                endpoint = tag['href'].strip()
                # Check if the endpoint starts with '/' to handle relative URLs
                if endpoint.startswith('/'):
                    full_endpoint = urljoin(url, endpoint)
                    if full_endpoint not in discovered_endpoints:
                        discovered_endpoints.add(full_endpoint)
                        #print(full_endpoint)
                        save_endpoint_to_file(endpoint,'endpoints_with_par.txt')
                        get_endpoints_recursive(full_endpoint, discovered_endpoints)
                # Check if the endpoint is a valid URL within the same domain
                elif is_valid_url(endpoint):
                    if urlparse(endpoint).netloc == urlparse(url).netloc:
                        if endpoint not in discovered_endpoints:
                            discovered_endpoints.add(endpoint)
                            #print(endpoint)
                            save_endpoint_to_file(endpoint,'endpoints_with_par.txt')
                            get_endpoints_recursive(endpoint, discovered_endpoints)

            # Find all link tags
            link_tags = soup.find_all('link', href=True)
            for tag in link_tags:
                endpoint = tag['href'].strip()
                # Check if the endpoint starts with '/' to handle relative URLs
                if endpoint.startswith('/'):
                    full_endpoint = urljoin(url, endpoint)
                    if full_endpoint not in discovered_endpoints:
                        discovered_endpoints.add(full_endpoint)
                        #print(full_endpoint)
                        get_endpoints_recursive(full_endpoint, discovered_endpoints)
                # Check if the endpoint is a valid URL within the same domain
                elif is_valid_url(endpoint):
                    if urlparse(endpoint).netloc == urlparse(url).netloc:
                        if endpoint not in discovered_endpoints:
                            discovered_endpoints.add(endpoint)
                            #print(endpoint)
                            #save_endpoint_to_file(endpoint,'endpoints_with_par.txt')
                            get_endpoints_recursive(endpoint, discovered_endpoints)

                # Check if the endpoint has query parameters
                if has_query_parameters(endpoint):
                    #print(f"Endpoint with parameters detected: {endpoint}")
                    #save_endpoint_to_file(endpoint,'endpoints_with_par.txt')
                    paths_with_parameters.append(endpoint)
                    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
    return paths_with_parameters
def is_valid_url(url):
    # Check if the given URL has a valid format (e.g., http://example.com or https://www.example.com)
    pattern = re.compile(r'^(https?://)?([A-Za-z0-9.-]+)$')
    return pattern.match(url)

def has_query_parameters(url):
    # Check if the URL has query parameters
    parsed_url = urlparse(url)
    return bool(parse_qs(parsed_url.query))

def save_endpoint_to_file(endpoint, filename):
    with open(filename, 'a') as file:
        file.write(endpoint + '\n')
#--------------------------------------------port_scan----------------------------------------------------------------
def scan_ports(ip_address):
    open_ports = []
    ports = [21, 22, 23, 25, 53, 80, 81, 135, 139, 143, 161, 194,220, 443, 389, 445, 636, 989, 993, 995, 1080, 1194, 1433, 2222, 3306, 3389, 5432, 5900, 8080 ]
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
        print("PORT   STATE  SERVICE")
        for port in open_ports:
            service_name = get_service_name(port)
            print(f"{str(port).ljust(6)} open  {service_name}")
        print()
#-----------------------------------------------wordpress_scanner-------------------------------------------------------
def check_path(url):
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return None

def check_path1(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url  # Add https:// if the URL doesn't have a protocol
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None
def wp_scan(domain):
     
    paths_to_check = [
        ("wp-json/wp/v2/users", "User enumeration or IP address leak"),  # Comment about the risk
        ("xmlrpc.php", "Potential for DOS attack and brute forcing users"),  # Comment about the risk
        ("wp-cron.php", "Potential for DOS attack"),  # Comment about the risk
        ("wp-json/oembed/1.0/proxy", "Potential for SSRF attack") , # Comment about the risk
        ("index.php", "Default WordPress entry point"),
        ("wp-activate.php",  "Account activation page"),
        ("wp-admin/login.php",   "WordPress admin login page"),
        ("wp-admin/wp-login.php",   "Alternative admin login page"),
        ("login.php",   "General login page"),
        ("wp-login.php",   "WordPress login page"),
        ("wp-content",   "Content directory"),
        ("wp-content/uploads/",   "Uploaded files directory"),
        ("wp-includes/",   "WordPress core files directory"),
        ("wp-config.php",   "WordPress configuration file"),
        "?author=1", "?author=2", "?author=3", "?author=4", "?author=5", "?author=6", "?author=7" # User enumeration via author parameter
    ]
    
    #print(f"Scanning WordPress website: {domain}\n")
    for path in paths_to_check:
        if isinstance(path, tuple):
            path, comment = path
        else:
            comment = "User enumeration via author parameter"
        url = f"{domain}/{path}"
        response_content = check_path(url)
        if response_content:
            print(f"Path: {url}")
            print(f"Comment: {comment}")
            #print(f"Response Content:\n{response_content}\n")
#-------------------------------------------------parameter_testing----------------------------------------------------
def check_param_vulnerability(url):
    try:
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        params = dict(map(lambda x: x.split('='), parsed_url.query.split('&')))

        #Sql injection-----------------------------------------------------
        print(" ----------------------------------------Sqli_Test---------------------------------------\n\n\n\n")

        #Payloads
        f = open("wordlists/sql.txt", "r")
        a = f.readlines()
        
        print(f"Checking URL for sql_injection: {url}")
        print("Parameter Vulnerabilities:")
        for param, value in params.items():
            for l in a:
                vulnerable_params = {k: v + l if k == param else v for k, v in params.items()}
                vulnerable_url = f"{base_url}?{urlencode(vulnerable_params)}"
                response = requests.get(vulnerable_url)
                # print(response.text)
            
                if '200' in response.text:
                    print(f"  [VULNERABLE] Parameter: {param}")
                    print(f"payload: {l}")
        f.close()

        #Xss--------------------------------------------------------------------
        print("-----------------------------------------Xss_Test---------------------------------------\n\n\n\n")
        f = open("wordlists/xss.txt", "r")
        a = f.readlines()
        
        print(f"Checking URL for sql_injection: {url}")
        print("Parameter Vulnerabilities:")
        for param, value in params.items():
            for l in a:
                vulnerable_params = {k: l if k == param else v for k, v in params.items()}
                vulnerable_url = f"{base_url}?{urlencode(vulnerable_params)}"
                response = requests.get(vulnerable_url)
            
                if '200' in response.text:
                    print(f"  [VULNERABLE] Parameter: {param}")
                    print(f"payload: {l}") 
        f.close()



    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate web technology scanning.")
    parser.add_argument("urls", nargs='+', type=str, help="URLs of the websites to scan")
    args = parser.parse_args()

    
    for url in args.urls:
        print(f"Technologies detection for : {url}")
        techs = scan_website(url)
        data_dict = techs
        pretty_json_string = json.dumps(data_dict, indent=4).replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace(",", "").replace('"', '')
        print(pretty_json_string)
        if "WordPress" in pretty_json_string:  # Check if "WordPress" is in the technologies discovered
            print("WordPress detected. Initiating WordPress scan...")
            wp_scan(url)


        subdomains = crtsh_subdomain_enum(url)

        if subdomains:
            print(f"Subdomains found for {url}:", end="\n\n")
            for subdomain in subdomains:
                 print(subdomain)
            for subdomain in subdomains:
                 full_subdomain = "https://" + subdomain
                 paths=get_endpoints_recursive(full_subdomain)
                 print("Endpoints enumeration done ", end="\n\n")
                 for path_with_pr in paths:
                     if "ver" in path_with_pr :
                        continue
                     else :
                        check_param_vulnerability(path_with_pr)
            # print()
            # print("DNS Reconnaissance and open ports scan started ", end="\n\n")
            # for subdomain in subdomains:
            #      ip_of_dm = get_ip_for_domain(subdomain)
            #      print_dns_results(subdomain,ip_of_dm)
            #      open_ports = scan_ports(get_ip_for_domain(subdomain))
            #      print_scan_results(ip_of_dm,open_ports)
        else:
            print(f"No subdomains found for {url}.")     
        

    
