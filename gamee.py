import requests
import urllib.parse
import json
import time
import subprocess
# URL dan headers
url = "https://api.service.gameeapp.com/"
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://tg-tap-miniapp.laborx.io',
    'priority': 'u=1, i',
    'referer': 'https://tg-tap-miniapp.laborx.io/',
    'content-type': 'text/plain;charset=UTF-8',
    'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'Referer': 'https://tg-tap-miniapp.laborx.io/',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
}

# Fungsi untuk membaca initData dari file
def read_initdata_from_file(filename):
    initdata_list = []
    with open(filename, 'r') as file:
        for line in file:
            initdata_list.append(line.strip())
    return initdata_list


def get_nama_from_init_data(init_data):
    parsed_data = urllib.parse.parse_qs(init_data)
    if 'user' in parsed_data:
        user_data = parsed_data['user'][0]
        data = ""
        user_data_json = urllib.parse.unquote(user_data)
        user_data_dict = json.loads(user_data_json)
        if 'first_name' in user_data_dict:
            data = user_data_dict['first_name']
        if 'last_name' in user_data_dict:
            data = data + " " + user_data_dict['last_name']
        if 'username' in user_data_dict:
            data = data + " " + f"({user_data_dict['username']})"
        return data
    return None

# Fungsi untuk melakukan start session

def auth(initdata):
    response = requests.post('https://tg-bot-tap.laborx.io/api/v1/auth/validate-init',data=initdata, headers=headers)
    print(response.status_code)
    print(response.text)
    if response.status_code ==200:
        return response.json().get("token")
    return None

def start_session(token):
    headers["authorization"]=f'Bearer {token}'
    response = requests.post('https://tg-bot-tap.laborx.io/api/v1/farming/start',{}, headers=headers)
    return response


def claim_session(token):
    headers["authorization"]=f'Bearer {token}'
    response = requests.post('https://tg-bot-tap.laborx.io/api/v1/farming/finish',{},headers=headers)
    return response

# Fungsi untuk menjalankan operasi untuk setiap initData
def process_initdata(init_data):
    # Login
    nama = get_nama_from_init_data(init_data)
    print(nama)
    print(init_data)
    token = auth(init_data)
    print(token)
    if token:
        start_response = start_session(token)
        daily_response = claim_session(token)
        if start_response.status_code == 200:
            print("Mine Started")
        else:
            print(start_response.text)
            
        if daily_response.status_code == 200:
            print("Sudah Claim")
        else :
            print("Belum Waktunya Claim")
    else:
        print("gagal auth")
                

# Main program
def main():
    initdata_file = "initdata.txt"
    
    while True:
        initdata_list = read_initdata_from_file(initdata_file)
        
        for init_data in initdata_list:
            process_initdata(init_data.strip())
            print("\n")
        
        # Delay sebelum membaca ulang file initData
        time.sleep(0)  # Delay 60 detik sebelum membaca kembali file initData

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        subprocess.run(["python3.10", "gamee.py"])
