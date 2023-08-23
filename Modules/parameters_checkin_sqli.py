#This script checks for potential SQL injection vulnerabilities by injecting a single quote (') into each parameter.


import requests
import subprocess
import argparse
from urllib.parse import urlparse, urlencode
from bs4 import BeautifulSoup
import subprocess
#-------------------------------------------------scan forms-----------------------------------------------------------

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"

#  Function to get all forms 
def get_forms(url):
    soup = BeautifulSoup(s.get(url).content, "html.parser")
    return soup.find_all("form")

def form_details(form):
    detailsOfForm = {}
    action = form.attrs.get("action")
    method = form.attrs.get("method", "get")
    inputs = []

    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({
            "type": input_type, 
            "name" : input_name,
            "value" : input_value,
        })
        
    detailsOfForm['action'] = action
    detailsOfForm['method'] = method
    detailsOfForm['inputs'] = inputs
    return detailsOfForm

def vulnerable(response):
    errors = {"quoted string not properly terminated", 
              "unclosed quotation mark after the charachter string",
              "you have an error in you SQL syntax" 
             }
    for error in errors:
        if error in response.content.decode().lower():
            return True
    return False

def sql_injection_scan(url):
    forms = get_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")
    
    for form in forms:
        details = form_details(form)
        
        for i in "\"'":
            data = {}
            for input_tag in details["inputs"]:
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    data[input_tag['name']] = input_tag["value"] + i
                elif input_tag["type"] != "submit":
                    data[input_tag['name']] = f"test{i}"
    
            print(url)
            form_details(form)

            if details["method"] == "post":
                res = s.post(url, data=data)
            elif details["method"] == "get":
                res = s.get(url, params=data)
            if vulnerable(res):
                print("SQL injection attack vulnerability in link: ", url )
                return(1)
            else:
                print("No SQL injection attack vulnerability detected")
                return(0)
                break
#-----------------------------------------------------------------------------------------------------------------------

def check_param_vulnerability(url):
    try:
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        params = dict(map(lambda x: x.split('='), parsed_url.query.split('&')))

        #------------------------------------------Sql injection-----------------------------------------------------

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
                is_error_based = sql_injection_scan(url)
            if not is_error_based :
                print("---> No error based detected\n")
                print("-->Searching for a blind sqli.....\n")
                print("...\n")

                try:
                    # Run the command and capture its output
                    command = "sqlmap -u " + url
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
                    a = output.rindex("you can find result")
                    print(output[a:])
                except UnicodeDecodeError:
                    pass  # Silently ignore the exception and continue with the execution
                    #Provide input to the process (in this case, just 'yes' to all prompts)
                    output, error = output.communicate(input='y\n')

            f.close()

        
    except Exception as e:
        print(f"An error occurred: {e}")


