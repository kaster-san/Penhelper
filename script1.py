#!/usr/bin/env python3
import argparse
import requests
import webtech

def scan_website(url):
    try:
        response = requests.get(url, timeout=5)  # Set the timeout value here (in seconds)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        wt = webtech.WebTech(options={'json': True})
        report = wt.start_from_url(url)
        return report['tech']
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
        if techs is not None:
            results.append((url, techs))

    for url, techs in results:
        print("Site: {}".format(url))
        for tech in techs:
            print(" - {}".format(tech))

    print("Done")
