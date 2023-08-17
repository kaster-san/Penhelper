#This script checks for potential SQL injection vulnerabilities by injecting a single quote (') into each parameter.


import requests
import subprocess
from urllib.parse import urlparse, urlencode

def check_param_vulnerability(url):
    try:
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        params = dict(map(lambda x: x.split('='), parsed_url.query.split('&')))

        #Sql injection-----------------------------------------------------

                #Payloads
        f = open("wordlists/sql.txt", "r")
        a = f.readlines()
        error_keywords = ['error', 'syntax', 'exception', 'query', 'mysql', 'pg_', 'sqlite']
        is_error_based = 0
        
        print(f"Checking URL for sql_injection: {url}")
        print("Parameter Vulnerabilities:")
        for param, value in params.items():
            for l in a:
                vulnerable_params = {k: v + l if k == param else v for k, v in params.items()}
                vulnerable_url = f"{base_url}?{urlencode(vulnerable_params)}"
                response = requests.get(vulnerable_url)
                # print(response.text)
            
                for word in error_keywords:
                    if word in response.text:
                        print("Error based sql_inject detected")
                        print(f"  [VULNERABLE] Parameter: {param}")
                        print(f"payload: {l}")
                        is_error_based = 1
                        break
                        
            if not is_error_based :
                print("---> No error based detected\n")
                print("-->Searching for a blind sqli.....\n")
                print("...\n")

                try:
                    # Run the command and capture its output
                    command = "sqlmap -u " + url
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
                    a = output.rindex("you can find resul")
                    print(output[a:])
                except UnicodeDecodeError:
                    pass  # Silently ignore the exception and continue with the execution
                    #Provide input to the process (in this case, just 'yes' to all prompts)
                    output, error = process.communicate(input='y\n')

            f.close()

        #Xss--------------------------------------------------------------------
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    #target_url = "https://example.com/test.php?id=1&name=john&age=25"
    target_url = str(input("Url: "))
    check_param_vulnerability(target_url)
