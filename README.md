# Penhelper - Web Security Assessment Automation Tool

Penhelper is a Python-based automation tool designed for web security assessment, penetration testing, and vulnerability detection. The tool offers a range of modules that automate tasks such as technologies detection, subdomain enumeration, endpoint detection, security header analysis, DNS reconnaissance, and more. Penhelper simplifies the process of identifying vulnerabilities and potential security weaknesses in web applications.

**Please Note:** This tool is currently in an alpha release, which means it's not yet feature-complete and might contain bugs or incomplete functionality. Contributions and feedback are welcome as we work towards improving and enhancing the tool.

## Table of Contents

- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [API setup](#Obtain-Google-API-Key-and-Custom-Search-Engine-ID)
- [Usage](#usage)
- [Modules](#modules)
- [Contributing](#contributing)


## Getting Started

### Installation

1. **Clone the Repository:**

   ```
   git clone https://github.com/kaster-san/Penhelper.git
   cd Penhelper
   ```

2. **Install Dependencies:**

   ```
   pip install -r requirements.txt
   ```

### Obtain Google API Key and Custom Search Engine ID

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).

2. Create a new project or select an existing one.

3. In the navigation pane, click on "APIs & Services" > "Dashboard."

4. Click on "+ ENABLE APIS AND SERVICES" at the top of the page.

5. Search for "Custom Search JSON API" and select it.

6. Click on the "Enable" button for the "Custom Search JSON API."

7. In the navigation pane, click on "APIs & Services" > "Credentials."

8. Click on "+ CREATE CREDENTIALS" and select "API Key."

9. A new API key will be created. Copy the generated API key.

### Create Custom Search Engine

1. Go to [Google Custom Search](https://cse.google.com/cse/create/new).

2. Click on "Create a Programmable Search Engine."

3. Follow the setup process to create a new search engine.

4. In the "Sites to Search" section, add the sites you want to search using Google Dorking.

5. Once the search engine is created, go to "Control Panel" > "Details" and copy the "Search Engine ID."

### Configure Penhelper with API Key and Engine ID

1. Open the `Penhelper.py` script.

2. Find the section where Google Dorking Module is performed.

3. Replace the placeholders 'YOUR_API_KEY' and 'YOUR_SEARCH_ENGINE_ID' with your API key and Custom Search Engine ID:

4. Save the changes.

With the Google API key and Custom Search Engine ID configured in the script, you can now use the Google Dorking feature of the **Penhelper** tool to search for potential sensitive information exposed via Google search results.

By following these steps, you'll be able to leverage the power of Google Dorking to enhance your security assessment workflows and discover potential vulnerabilities and exposures in your target websites.



## Usage

Run the main script `Penhelper.py` with the target URLs as arguments:

```
python Penhelper.py https://example.com
```

## Modules

The **Penhelper** tool includes the following modules:

- Technologies Detection and WordPress Scan
- Google Dorking
- Subdomain Enumeration
- Endpoints Enumeration
- SQL Injection (SQLi) Testing
- Security Headers Analysis
- DNS Enumeration and Open Ports Scan
- Service Scan (FTP, SMB, Telnet)


## Contributing

Contributions to the **Penhelper** tool are welcome! Feel free to open issues for bug reports or suggestions, and submit pull requests to contribute improvements or additional features.

## License

Penhelper is released under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html) (GPL-3.0) License.

This means that you are free to use, modify, and distribute this software under the terms of the GPL-3.0 license. However, it's important to understand and adhere to the terms outlined in the license document. You can find a copy of the full license text in the [LICENSE](./LICENSE.md) file.

Please note that any contributions you make to this project will also be covered by the same license terms.

For more details, please visit the [GNU website](https://www.gnu.org/licenses/gpl-3.0.en.html) to learn about the rights and restrictions provided by this license.

