import requests
import time
import datetime
from colorama import init, Fore, Style

# Inisialisasi colorama
init(autoreset=True)

# Fungsi untuk mendapatkan data pengguna
def get_user_data(auth_token):
    url = "https://api.pixelfarm.app/user"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Mobile/15E148 Safari/604.1"
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Fungsi untuk melakukan klaim
def claim(auth_token):
    url = "https://api.pixelfarm.app/user/claim"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Mobile/15E148 Safari/604.1"
    }
    response = requests.post(url, headers=headers)
    return response.json()

# Fungsi untuk menampilkan waktu hitung mundur dalam format jam:menit:detik
def countdown(seconds):
    while seconds:
        hours, remainder = divmod(seconds, 3600)
        mins, secs = divmod(remainder, 60)
        timeformat = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)
        print(f"{Fore.RED}Countdown to next claim: {timeformat}", end='\r')
        time.sleep(1)
        seconds -= 1

# Fungsi utama untuk menjalankan bot
def run_bot(auth_token, claim_interval):
    while True:
        user_data = get_user_data(auth_token)
        
        print(f"\n{Fore.YELLOW}{'='*40}")
        print(f"{Fore.YELLOW}PixelFarm Bot")
        print(f"{Fore.YELLOW}Channel: https://t.me/ugdairdrop")
        print(f"{Fore.YELLOW}{'='*40}")
        print(f"\n{Fore.YELLOW}{'='*40}")
        print(f"{Fore.GREEN}Telegram ID       : {user_data['data']['telegram_id']}")
        print(f"{Fore.GREEN}Telegram Username : {user_data['data']['telegram_username']}")
        print(f"{Fore.GREEN}Gem Amount        : {user_data['data']['gem_amount']}")
        print(f"{Fore.GREEN}Fruit Total       : {user_data['data']['crops'][0]['fruit_total']}")
        print(f"{Fore.GREEN}Tree Type         : {user_data['data']['crops'][0]['tree_type']}")
        print(f"{Fore.YELLOW}{'='*40}")

        claim_response = claim(auth_token)
        
        if claim_response['data']:
            print(f"\n{Fore.YELLOW}Claim Response: Sukses melakukan klaim")
            new_user_data = get_user_data(auth_token)
            claimed_fruit = new_user_data['data']['crops'][0]['fruit_total'] - user_data['data']['crops'][0]['fruit_total']
            total_fruit = new_user_data['data']['crops'][0]['fruit_total']
            print(f"{Fore.YELLOW}Jumlah fruit yang diklaim : {claimed_fruit}")
            print(f"{Fore.YELLOW}Jumlah total fruit setelah klaim : {total_fruit}")
        else:
            print(f"\n{Fore.RED}Claim Response: Gagal melakukan klaim")
        
        # Hitung mundur selama 6 jam (21600 detik) sebelum klaim berikutnya
        print(f"\n{Fore.GREEN}{'-'*40}")
        print(f"{Fore.BLUE}Menunggu untuk klaim berikutnya...")
        countdown(21600)
        print(f"\n{Fore.GREEN}{'-'*40}")

# Membaca auth token dari file teks
with open('data.txt', 'r') as file:
    auth_token = file.read().strip()

# Jalankan bot dengan interval klaim setiap 6 jam
run_bot(auth_token, 21600)
