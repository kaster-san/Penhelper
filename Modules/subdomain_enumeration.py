import requests
from bs4 import BeautifulSoup

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