
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs , urlencode
import re

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