#!/usr/bin/env python3
import argparse
import requests
import webtech
import json

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate web technology scanning.")
    parser.add_argument("urls", nargs='+', type=str, help="URLs of the websites to scan")
    args = parser.parse_args()

    results = []

    for url in args.urls:
        techs = scan_website(url)
        data_dict = techs
        pretty_json_string = json.dumps(data_dict, indent=4).replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace(",", "").replace('"', '')
        
        print(pretty_json_string)
    print("Done")
