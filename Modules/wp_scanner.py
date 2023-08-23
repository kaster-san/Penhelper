import requests


def check_path(url):
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return None

def check_path1(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url  # Add https:// if the URL doesn't have a protocol
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None
def wp_scan(domain):
     
    paths_to_check = [
        ("wp-json/wp/v2/users", "User enumeration or IP address leak"),  # Comment about the risk
        ("xmlrpc.php", "Potential for DOS attack and brute forcing users"),  # Comment about the risk
        ("wp-cron.php", "Potential for DOS attack"),  # Comment about the risk
        ("wp-json/oembed/1.0/proxy", "Potential for SSRF attack") , # Comment about the risk
        ("index.php", "Default WordPress entry point"),
        ("wp-activate.php",  "Account activation page"),
        ("wp-admin/login.php",   "WordPress admin login page"),
        ("wp-admin/wp-login.php",   "Alternative admin login page"),
        ("login.php",   "General login page"),
        ("wp-login.php",   "WordPress login page"),
        ("wp-content",   "Content directory"),
        ("wp-content/uploads/",   "Uploaded files directory"),
        ("wp-includes/",   "WordPress core files directory"),
        ("wp-config.php",   "WordPress configuration file"),
        "?author=1", "?author=2", "?author=3", "?author=4", "?author=5", "?author=6", "?author=7" # User enumeration via author parameter
    ]
    
    #print(f"Scanning WordPress website: {domain}\n")
    for path in paths_to_check:
        if isinstance(path, tuple):
            path, comment = path
        else:
            comment = "User enumeration via author parameter"
        url = f"{domain}/{path}"
        response_content = check_path(url)
        if response_content:
            print(f"Path: {url}")
            print(f"Comment: {comment}")
            #print(f"Response Content:\n{response_content}\n")