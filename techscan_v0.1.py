import subprocess
import json
import os
import logging
import argparse

def execute_first_tool(url):
    logging.info("Executing CMSeek tool...")
    cmd = ['python', 'CMSeek/cmseek.py', '-u', url]

    try:
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        logging.error(f"Error while executing CMSeek: {e}")
        return

    output, error = process.communicate(input='y\n')
    process.wait()

    if error:
        logging.warning(f"CMSeek tool returned the following error:\n{error}")

def read_cms_result(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            cms_result = json.load(file)
    except FileNotFoundError:
        logging.error(f"CMSeek result file not found at {file_path}")
        return None, False
    except json.JSONDecodeError as e:
        logging.error(f"Error while reading CMSeek result: {e}")
        return None, False

    cms_detected = bool(cms_result.get('cms_id', None))
    return cms_result, cms_detected

def print_cms_result(cms_result):
    if not cms_result:
        print("No CMS detected.")
    else:
        print("CMS detected:")
        print(f"Site: {cms_result['url']}")
        print(f"WordPress Version: {cms_result['wp_version']}")
        print("Installed Plugins:")
        plugins = cms_result['wp_plugins'].split(',')
        for plugin in plugins:
            print(f" - {plugin.strip()}")
        print("Installed Themes:")
        themes = cms_result['wp_themes'].split(',')
        for theme in themes:
            print(f" - {theme.strip()}")
        # Add more details from the JSON file if needed

def execute_second_tool(url):
    result = subprocess.run(['python', 'script1.py', url], capture_output=True, text=True)
    webtech_output = result.stdout.strip()
    return webtech_output

def print_webtech_result(webtech_output):
    if not webtech_output:
        print("No technologies detected.")
    else:
        print("Technologies detected:")
        lines = webtech_output.split('\n')
        for line in lines:
            print(f" - {line.strip()}")
        print("Done")

def main(url):
    urldir = url[8:]
    execute_first_tool(url)
    cms_result, cms_detected = read_cms_result(f"CMSeek/Result/{urldir}/cms.json")

    if cms_detected:
        print_cms_result(cms_result)
    else:
        webtech_output = execute_second_tool(url)
        print_webtech_result(webtech_output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect CMS and Technologies")
    parser.add_argument("url", type=str, help="URL to scan")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    
    # Redirect subprocess output to a file
    urldir = args.url[8:]
    output_file_path = os.path.join("cmseek_output.txt")
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        process = subprocess.Popen(['python', 'CMSeek/cmseek.py', '-u', args.url], stdin=subprocess.PIPE, stdout=output_file, stderr=subprocess.PIPE, text=True)
        process.communicate(input='y\n')
        process.wait()

    # Read the subprocess output from the file
    main(args.url)
