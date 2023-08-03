#This script checks for potential SQL injection vulnerabilities by injecting a single quote (') into each parameter.


import requests
from urllib.parse import urlparse, urlencode

def check_param_vulnerability(url):
    try:
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        params = dict(map(lambda x: x.split('='), parsed_url.query.split('&')))

        #Sql injection-----------------------------------------------------

                #Payloads
        f = open("sql.txt", "r")
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
                # else:
                #     print(f"  [OK] Parameter: {param}")
        f.close()

        #Xss--------------------------------------------------------------------
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    #target_url = "https://example.com/test.php?id=1&name=john&age=25"
    target_url = str(input("Url: "))
    check_param_vulnerability(target_url)
