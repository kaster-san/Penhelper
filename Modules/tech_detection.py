import requests
import webtech



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