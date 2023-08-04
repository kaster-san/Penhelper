#This script checks for potential SQL injection vulnerabilities by injecting a single quote (') into each parameter.


import requests
import argparse
from urllib.parse import urlparse, urlencode

def check_param_vulnerability(url):
    try:
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        params = dict(map(lambda x: x.split('='), parsed_url.query.split('&')))

        #Sql injection-----------------------------------------------------
        print("                 -----------------------------Sqli_Teest---------------------------------------\n\n\n\n")

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
            
                if '404' not in response.text:
                    print(f"  [VULNERABLE] Parameter: {param}")
                    print(f"payload: {l}")
        f.close()

        #Xss--------------------------------------------------------------------
        print("                     -----------------------------Xss_Teest---------------------------------------\n\n\n\n")
        f = open("wordlists/xss.txt", "r")
        a = f.readlines()
        
        print(f"Checking URL for sql_injection: {url}")
        print("Parameter Vulnerabilities:")
        for param, value in params.items():
            for l in a:
                vulnerable_params = {k: l if k == param else v for k, v in params.items()}
                vulnerable_url = f"{base_url}?{urlencode(vulnerable_params)}"
                response = requests.get(vulnerable_url)
            
                if '404' not in response.text:
                    print(f"  [VULNERABLE] Parameter: {param}")
                    print(f"payload: {l}") 
        f.close()



    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, required=True)
    args = parser.parse_args()
    
    domains = open(args.path , "r")
    domains_list = domains.readlines()

    for domain in domains_list:
        check_param_vulnerability(domain)
