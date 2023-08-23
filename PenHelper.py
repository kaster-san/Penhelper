#!/usr/bin/env python3
import argparse
import json
from Modules import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate web technology scanning.")
    parser.add_argument("urls", nargs='+', type=str, help="URLs of the websites to scan")
    args = parser.parse_args()

#------------------------------------------Technologies detection--------------------------------------------
    for url in args.urls:
        print(f"Technologies detection for : {url}")
        techs = tech_detection.scan_website(url)
        data_dict = techs
        pretty_json_string = json.dumps(data_dict, indent=4).replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace(",", "").replace('"', '')
        print(pretty_json_string)
        if "WordPress" in pretty_json_string:  # Check if "WordPress" is in the technologies discovered
            print("WordPress detected. Initiating WordPress scan...")
            wp_scanner.wp_scan(url)
        
#------------------------------------------GooGle Dorking-----------------------------------------------------
        print(f"Google dorking for : {url}")
        DorkKnight.dorkisation(url)
#-----subdomain enumeration,endpoint detection,sqli test,headers analyse,DNS enumeration,port&service scan------
        subdomains = subdomain_enumeration.crtsh_subdomain_enum(url)

        if subdomains:
            print(f"Subdomains found for {url}:", end="\n\n")
            for subdomain in subdomains:
                 print(subdomain)
            for subdomain in subdomains:
                 full_subdomain = "https://" + subdomain
                 paths=endpoints_enumeration.get_endpoints_recursive(full_subdomain)
                 print("Endpoints enumeration done ", end="\n\n")
                 for path_with_pr in paths:
                     if "ver" in path_with_pr :
                        continue
                     else :
                        parameters_checkin_sqli.check_param_vulnerability(path_with_pr)
            print()
            print("headers scan : ", end="\n\n")
            for subdomain in subdomains :
                    print()
                    try:
                        Security_headers.analyze_security_headers("https://" + subdomain)
                    except Exception as e:
                        print("An error occurred:", str(e))
                        print("=" * 50)
            print()
            print("DNS Reconnaissance and open ports scan started ", end="\n\n")
            for subdomain in subdomains:
                 ip_of_dm = DNS_Enumeration.get_ip_for_domain(subdomain)
                 DNS_Enumeration.print_dns_results(subdomain,ip_of_dm)
                 open_ports = ports_scan.scan_ports(DNS_Enumeration.get_ip_for_domain(subdomain))
                 ports_scan.print_scan_results(ip_of_dm,open_ports)
                             # Tester les ports FTP , SMB et telnet 
                 for port in open_ports:
                    if port == 21:
                        if service_scan.connect_ftp(ip_of_dm, port):
                            print(f"FTP connection succeeded for {ip_of_dm}:{port}")
                        else:
                            print(f"FTP connection failed for {ip_of_dm}:{port}")
                    elif port == 23:
                        if service_scan.connect_telnet(ip_of_dm, port):
                            print(f"Telnet connection succeeded for {ip_of_dm}:{port}")
                        else:
                            print(f"Telnet connection failed for {ip_of_dm}:{port}")
                    elif port == 445:
                        if service_scan.connect_smb(ip_of_dm, port):
                            print(f"SMB connection succeeded for {ip_of_dm}:{port}")
                        else:
                            print(f"SMB connection failed for {ip_of_dm}:{port}")
        else:
            print(f"No subdomains found for {url}.")     
        

    
