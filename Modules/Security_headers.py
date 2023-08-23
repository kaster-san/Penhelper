import requests
def analyze_security_headers(url):
    headers = requests.get(url).headers
    security_headers = {
        'Strict-Transport-Security': 'HTTP Strict Transport Security (HSTS) enforces secure connections.',
        'Content-Security-Policy': 'Content Security Policy (CSP) controls sources of content that can be executed.',
        'X-Content-Type-Options': 'X-Content-Type-Options prevents content type sniffing.',
        'X-Frame-Options': 'X-Frame-Options prevents clickjacking attacks.',
        'X-XSS-Protection': 'X-XSS-Protection prevents cross-site scripting attacks.',
        'Referrer-Policy': 'Referrer-Policy controls what information is included in the Referer header.',
        'Feature-Policy': 'Feature-Policy restricts which features can be used by the browser.',
    }
    print(f'Security Headers Analysis for: {url}')
    for header, description in security_headers.items():
        header_value = headers.get(header)
        if header_value:
            print(f'{header} Found : {header_value} ')
        else:
            print(f'{header}: Not found - {description}')
            analyze_missing_header_risks(header)
def analyze_header_risks(header, header_value):
    # Define potential risks associated with each security header
    risks = {
        'Strict-Transport-Security': 'Enforces secure connections and prevents downgrade attacks.',
        'Content-Security-Policy': 'Controls sources of executable content and mitigates XSS.',
        'X-Content-Type-Options': 'Prevents content type sniffing and MIME-based attacks.',
        'X-Frame-Options': 'Prevents clickjacking and UI redressing attacks.',
        'X-XSS-Protection': 'Mitigates cross-site scripting attacks.',
        'Referrer-Policy': 'Controls the information shared in the Referer header.',
        'Feature-Policy': 'Restricts usage of specific browser features to mitigate risk.',
    }
    
    risk_comment = risks.get(header)
    if risk_comment:
        print(f'Risks for {header}: {risk_comment}')
    else:
        print(f'No specific risks information available for {header}.')

def analyze_missing_header_risks(header):
    # Define potential risks associated with missing security headers
    missing_header_risks = {
        'Strict-Transport-Security': 'Missing HSTS header can lead to potential downgrade attacks.',
        'Content-Security-Policy': 'Missing CSP header may expose the application to XSS attacks.',
        'X-Content-Type-Options': 'Missing X-Content-Type-Options header could allow MIME-based attacks.',
        'X-Frame-Options': 'Missing X-Frame-Options header may expose the application to clickjacking.',
        'X-XSS-Protection': 'Missing X-XSS-Protection header could expose the application to XSS attacks.',
        'Referrer-Policy': 'Missing Referrer-Policy header may leak sensitive information.',
        'Feature-Policy': 'Missing Feature-Policy header may expose the application to unwanted features.',
    }
    
    risk_comment = missing_header_risks.get(header)
    if risk_comment:
        print(f'Risks for missing {header}: {risk_comment}')
    else:
        print(f'No specific risks information available for missing {header}.')