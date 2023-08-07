import requests
from bs4 import BeautifulSoup
import urllib.parse
import json

def get_url_input():
    url = input('Enter the website URL: ')
    return url

def is_valid_url(url):
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def get_absolute_link(base_url, relative_url):
    if relative_url is None:
        return None
    if relative_url.startswith(('http://', 'https://')):
        return relative_url
    return urllib.parse.urljoin(base_url, relative_url)

def get_web_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as err:
        print("Something went wrong: ", err)
        return None

def analyze_links(content, base_url):
    soup = BeautifulSoup(content, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a')]
    absolute_links = [get_absolute_link(base_url, link) for link in links]
    return absolute_links

def analyze_architecture(content, base_url):
    soup = BeautifulSoup(content, 'html.parser')
    architecture = {
        'scripts': {
            'count': len(soup.find_all('script')),
            'links': [get_absolute_link(base_url, script.get('src')) for script in soup.find_all('script') if script.get('src')]
        },
        'stylesheets': {
            'count': len(soup.find_all('link', {'rel': 'stylesheet'})),
            'links': [get_absolute_link(base_url, stylesheet.get('href')) for stylesheet in soup.find_all('link', {'rel': 'stylesheet'}) if stylesheet.get('href')]
        },
        'images': {
            'count': len(soup.find_all('img')),
            'links': [get_absolute_link(base_url, img.get('src')) for img in soup.find_all('img') if img.get('src')]
        },
        'videos': {
            'count': len(soup.find_all('video')),
            'links': [get_absolute_link(base_url, video.get('src')) for video in soup.find_all('video') if video.get('src')]
        },
        'audio': {
            'count': len(soup.find_all('audio')),
            'links': [get_absolute_link(base_url, audio.get('src')) for audio in soup.find_all('audio') if audio.get('src')]
        },
        'forms': {
            'count': len(soup.find_all('form')),
            'links': [base_url]
        },  # Include the URL of the page containing the form
        'iframes': {
            'count': len(soup.find_all('iframe')),
            'links': [get_absolute_link(base_url, iframe.get('src')) for iframe in soup.find_all('iframe') if iframe.get('src')]
        },
        'pdfs': {
            'count': len(soup.find_all('a', href=True, string=lambda s: s and s.lower().endswith('.pdf'))),
            'links': [get_absolute_link(base_url, link.get('href')) for link in soup.find_all('a', href=True, string=lambda s: s and s.lower().endswith('.pdf'))]
        },
        'documents': {
            'count': len(soup.find_all('a', href=True, string=lambda s: s and s.lower().endswith(('.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx')))),
            'links': [get_absolute_link(base_url, link.get('href')) for link in soup.find_all('a', href=True, string=lambda s: s and s.lower().endswith(('.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx')))]
        },
    }
    return architecture

def code():
    url = get_url_input()
    if not is_valid_url(url):
        print('Invalid URL, please try again.')
        return
    content = get_web_content(url)
    if content is None:
        print('Failed to access URL, please try again.')
        return

    results = {}
    results["links"] = analyze_links(content, url)
    results["architecture"] = analyze_architecture(content, url)

    print(f'Analysis Results:\n{json.dumps(results, indent=4)}')

    with open('results.json', 'w') as f:
        json.dump(results, f, indent=4)

    print('Analysis completed and results saved to results.json')

if __name__ == "__main__":
    code()
