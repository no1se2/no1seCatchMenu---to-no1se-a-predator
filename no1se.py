import os
import platform
import time
import json
from colorama import Fore, init, Style
import keyboard
import requests
import subprocess
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

CONFIG_FILE = "config.json"
DISCORD_WEBHOOK = None

init(autoreset=True)

art = """
    ██████  ██████  ██████  ███████ ██████      ██████  ██    ██     ███    ██  ██████   ██ ███████ ███████ 
    ██      ██    ██ ██   ██ ██      ██   ██     ██   ██  ██  ██      ████   ██ ██    ██ ███ ██      ██      
    ██      ██    ██ ██   ██ █████   ██   ██     ██████    ████       ██ ██  ██ ██    ██  ██ ███████ █████   
    ██      ██    ██ ██   ██ ██      ██   ██     ██   ██    ██        ██  ██ ██ ██    ██  ██      ██ ██      
    ██████  ██████  ██████  ███████ ██████      ██████     ██        ██   ████  ██████   ██ ███████ ███████ 
                                        CsgoRoll Intelligence Dashboard 1.0
"""

art2 = """
    ██████  ██████  ██████  ███████ ██████      ██████  ██    ██     ███    ██  ██████   ██ ███████ ███████ 
    ██      ██    ██ ██   ██ ██      ██   ██     ██   ██  ██  ██      ████   ██ ██    ██ ███ ██      ██      
    ██      ██    ██ ██   ██ █████   ██   ██     ██████    ████       ██ ██  ██ ██    ██  ██ ███████ █████   
    ██      ██    ██ ██   ██ ██      ██   ██     ██   ██    ██        ██  ██ ██ ██    ██  ██      ██ ██      
    ██████  ██████  ██████  ███████ ██████      ██████     ██        ██   ████  ██████   ██ ███████ ███████ 
                                         Ah shit here we go again...
"""


# Clear function like always
def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
        

#My Amazing intro
def intro():
    clear()
    print(Fore.RED + art)
    time.sleep(0.5)
    clear()
    print(Fore.BLUE + art2)
    time.sleep(0.5)
    clear()
    print(Fore.LIGHTCYAN_EX + art)
    time.sleep(0.5)
    clear()
    print(Fore.LIGHTMAGENTA_EX + art2)

def verifyroot():
    if os.getuid() == 0:
        print(f"{Fore.GREEN} Running as root ✅")
        time.sleep(1)
    else:
        print(f"{Fore.RED}[!] Please run the script as root!")
        exit()

# ---------------------Checking if chromedriver.exe is installed-------------#
def check_if_chromedriver_installed():
    if platform.system() == "Windows":
        chromeexe = Path("C:\\Windows\\chromedriver-win64\\chromedriver.exe")
        if chromeexe.is_file():
            print(f"{Fore.GREEN} [✓] chromedriver.exe found. Continuing with the script.")
            time.sleep(2)
        else:
            print(f"{Fore.RED}[✘] chromedriver.exe not found.")
            input(f"{Fore.WHITE}[!] Press Enter To get it now...")
            clear()
            download_chromedriver()
    # If the user has Linux :) which they should, because Windows is shit!
    else:
        chromedriverlinux = Path("/usr/local/bin/chromedriver-linux64/chromedriver")
        if chromedriverlinux.is_file():
            print(f"{Fore.GREEN} [✓] chromedriver found. Continuing with the script.")
            time.sleep(2)
        else:
            print(f"{Fore.RED}[✘] chromedriver not found.")
            input(f"{Fore.WHITE}[!] Press Enter To get it now...")
            clear()
            download_chromedriver()

#----------------------------------------------------------------------------------------------------------------------------------#

# ---------------------Installing Chromedriver if not found. fucking hell This process took some time.-------------#
def get_chrome_version():
    if platform.system() == "Windows":
        try:
            output = subprocess.check_output(['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'], stderr=subprocess.STDOUT, text=True)
            version = output.strip().split()[-1]
            return version
        except Exception as e:
            print(Fore.RED + "Error", "Fuck, I couldn't get the Chrome version. Contact no1se. I'm exiting the script...")
            exit()
# If the user has Linux :) which they should, because Windows is shit!
    else:
        try:
            output = subprocess.check_output(['google-chrome', '--version'], stderr=subprocess.STDOUT, text=True)
            version = output.strip().split()[-1]
            return version
        except Exception as e:
            print(Fore.RED + "Error", "Fuck, I couldn't get the Chrome version. Contact no1se. I'm exiting the script...")
            exit()
        

def download_chromedriver():
    print(Fore.LIGHTMAGENTA_EX + art2)  
    chrome_version = get_chrome_version()
    print(f"{Fore.YELLOW}[!] Alright, so your Chrome version is: {chrome_version}")
    time.sleep(2)
    if platform.system() == "Windows":
        download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/win64/chromedriver-win64.zip"
    else:
        # If the user has Linux :) which they should, because Windows is shit!
        download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/linux64/chromedriver-linux64.zip"
    response = requests.get(download_url)
    if response.status_code == 200:
        print(f"{Fore.YELLOW}[!] Downloading chromedriver...")
        time.sleep(2)
        with open("chromedriver.zip", "wb") as f:
            f.write(response.content)

        import zipfile
        with zipfile.ZipFile("chromedriver.zip", "r") as z:
            if platform.system() == "Windows":
                z.extractall("c:\\Windows")
            else:
                # If the user has Linux :) which they should, because Windows is shit!
                z.extractall("/usr/local/bin")
                os.chmod("/usr/local/bin/chromedriver-linux64/chromedriver", 0o755)
        
        os.remove("chromedriver.zip")
        print(f"{Fore.GREEN}[✓] I got you homie", "You now have chromedriver installed.")
        input(F"{Fore.WHITE}[!] Press enter to continue...")
    else:
        print(f"{Fore.RED}[✘] Failed to download chromedriver. Contact no1se for help. Status code:{response.status_code}")
        exit(0)
#----------------------------------------------------------------------------------------------------------------------------------#

#--------------------------------Discord Webhook set up----------------------------------------------------------------------------#
def load_config():
    global DISCORD_WEBHOOK
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            DISCORD_WEBHOOK = data.get("webhook")
            if DISCORD_WEBHOOK:
                print(f"{Fore.GREEN}[+] Loaded webhook!")
                time.sleep(1)
            else:
                print(f"{Fore.RED}[-] Webhook is not set choose option 2 to set it!")
                time.sleep(2)
                
def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump({"webhook": DISCORD_WEBHOOK}, f)
        
def set_webhook():
    global DISCORD_WEBHOOK
    webhook = input("Enter your Discord Webhook URL: ").strip()
    if webhook.startswith("https://discord.com/api/webhooks/"):
        DISCORD_WEBHOOK = webhook
        save_config()
        print(f"{Fore.GREEN}[+] Webhook saved successfully!")
    else:
        print(f"{Fore.RED}[!] Invalid webhook URL.")
#--------------------------------Discord Webhook set up----------------------------------------------------------------------------#

def roll_color(class_str):
    if "bg-green" in class_str:
        return "green"
    elif "bg-red" in class_str:
        return "red"
    elif "bg-black" in class_str:
        return "black"
    return "unknown"


def get_last_two_rolls(driver):
    rolls = driver.find_elements(By.CSS_SELECTOR, "a.roll") 
    if len(rolls) < 2:
        return []
    return rolls[:2]  

def send_discord_alert(message: str):
    if not DISCORD_WEBHOOK:
        print(f"{Fore.RED}[!] No Discord webhook set. Choose option 2 from the menu to set it.")
        return
    
    payload = {
        "content": message,
        "username": "no1seRoll Alert",
        "avatar_url": "https://res.cloudinary.com/jerrick/image/upload/v1678827096/6410de58c7b229001d2b59f2.png"
    }
    try:
        requests.post(DISCORD_WEBHOOK, json=payload)
    except Exception as e:
        print(f"{Fore.RED}[X] Failed to send Discord Alert: {e}")

def monitor_start():
    print(Fore.LIGHTMAGENTA_EX + art2)
    # ------------setting the chromedriver------------------#
    if platform.system() == "Windows":
        PATH = "C:\\Windows\\chromedriver-win64\\chromedriver.exe"
    else:
        PATH = "/usr/local/bin/chromedriver-linux64/chromedriver"
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service(PATH, log_path=os.devnull)
    
    driver = webdriver.Chrome(options=options,service=service)
    driver.get("https://www.csgoroll.com/roll")
    print("[*] Opened CSGORoll roulette...")
    
    try:
        while True:
            last_two = get_last_two_rolls(driver)
            if len(last_two)< 2:
                print(f"{Fore.YELLOW}[-] Not enough rolls yet...")
                time.sleep(1)
                continue
            colors = [roll_color(r.get_attribute("class")) for r in last_two]
            color_map = {"green": Fore.GREEN, "red": Fore.RED, "black": Fore.WHITE}
            formatted = ", ".join(color_map.get(c, Fore.MAGENTA) + c + Style.RESET_ALL for c in colors)
            
            print(f"Last two rolls: {formatted}")
                
            if colors == ["green", "green"]:
                print(Fore.LIGHTGREEN_EX + "🚨 DOUBLE GREEN DETECTED! 🚨" + Style.RESET_ALL)
                send_discord_alert("🚨🎰 DOUBLE GREEN ALERT on CSGORoll! Possible triple incoming! 🎰🚨")
                time.sleep(10)
            else:
                print(Fore.LIGHTBLACK_EX + "[*] No double green yet..." + Style.RESET_ALL)
                time.sleep(2)
                
    except KeyboardInterrupt:
        print("\n[!] Stopping script...")
    finally:
        driver.quit()
        time.sleep(0.5)
        main_menu()

def main_menu():
    while True:
        #Squidward
        clear()
        print(f"{Fore.LIGHTMAGENTA_EX}                 ╔═════════════════════════════════╗")
        print(f"{Fore.LIGHTMAGENTA_EX}                 ║" + f"{Fore.LIGHTMAGENTA_EX}        .--'''''''''--.          " + f"{Fore.LIGHTMAGENTA_EX}║")
        print(f"{Fore.LIGHTMAGENTA_EX}                 ║" + f"{Fore.LIGHTMAGENTA_EX}     .'      .---.      '.       " + f"{Fore.LIGHTMAGENTA_EX}║")
        print(f"{Fore.LIGHTMAGENTA_EX}                 ║" + f"{Fore.LIGHTMAGENTA_EX}    /    .-----------.    \\      " + f"{Fore.LIGHTMAGENTA_EX}║")
        print(f"{Fore.LIGHTMAGENTA_EX}                 ║" + f"{Fore.LIGHTMAGENTA_EX}   /        .-----.        \\     " + f"{Fore.LIGHTMAGENTA_EX}║")
        print(f"{Fore.LIGHTMAGENTA_EX}                 ║" + f"{Fore.LIGHTMAGENTA_EX}   |       .-.   .-.       |     " + f"{Fore.LIGHTMAGENTA_EX}║")
        print(f"{Fore.LIGHTMAGENTA_EX}                 ║" + f"{Fore.LIGHTMAGENTA_EX}   |      /   \\ /   \\      |     " + f"{Fore.LIGHTMAGENTA_EX}║")
        print(f"{Fore.LIGHTMAGENTA_EX}                 ║" + f"{Fore.LIGHTMAGENTA_EX}    \\    | .-. | .-. |    /      " + f"{Fore.LIGHTMAGENTA_EX}║")
        print(f"{Fore.LIGHTMAGENTA_EX}                 ║" + f"{Fore.LIGHTMAGENTA_EX}     '-._| | | | | | |_.-'       " + f"{Fore.LIGHTMAGENTA_EX}║")
        print(f"{Fore.LIGHTMAGENTA_EX}                 ║" + f"{Fore.LIGHTMAGENTA_EX}         | '-' | '-' |           " + f"{Fore.LIGHTMAGENTA_EX}║")
        print(f"{Fore.LIGHTMAGENTA_EX}                 ║" + f"{Fore.LIGHTMAGENTA_EX}          \\___/ \\___/            " + f"{Fore.LIGHTMAGENTA_EX}║")
        print(f"{Fore.LIGHTMAGENTA_EX}                 ║" + f"{Fore.LIGHTMAGENTA_EX}       _.-'  /   \\  `-._         " + f"{Fore.LIGHTMAGENTA_EX}║")
        print(f"{Fore.LIGHTMAGENTA_EX}                 ║" + f"{Fore.LIGHTMAGENTA_EX}     .' _.--|     |--._ '.       " + f"{Fore.LIGHTMAGENTA_EX}║")
        print(f"{Fore.LIGHTMAGENTA_EX}                 ║" + f"{Fore.LIGHTMAGENTA_EX}     ' _...-|     |-..._ '       " + f"{Fore.LIGHTMAGENTA_EX}║")
        print(f"{Fore.LIGHTMAGENTA_EX}                 ║" + f"{Fore.LIGHTMAGENTA_EX}            |     |              " + f"{Fore.LIGHTMAGENTA_EX}║")
        print(f"{Fore.LIGHTMAGENTA_EX}                 ║" + f"{Fore.LIGHTMAGENTA_EX}            '.___.'              " + f"{Fore.LIGHTMAGENTA_EX}║")
        print(f"{Fore.LIGHTMAGENTA_EX}                 ╚═════════════════════════════════╝")
        #Squidward
        print(f"{Fore.LIGHTMAGENTA_EX}╔═══════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.LIGHTMAGENTA_EX}║" + f"{Fore.WHITE}                     WELCOME TO {Fore.LIGHTMAGENTA_EX}no1seRoll.                   ║")
        print(f"{Fore.LIGHTMAGENTA_EX}╚═══════════════════════════════════════════════════════════════════╝")

        print(f"{Fore.WHITE}                       Please select an option:")
        print(f"{Fore.LIGHTMAGENTA_EX}           ╔═══════════════════════════════════════╗")
        print(f"{Fore.MAGENTA}           ║{Fore.WHITE}[{Fore.LIGHTMAGENTA_EX}1{Fore.WHITE}] Start jackpot monitoring.{Fore.MAGENTA}       Pretty cool ║")
        print(f"{Fore.MAGENTA}           ║{Fore.WHITE}[{Fore.LIGHTMAGENTA_EX}2{Fore.WHITE}] Set Discord Webhook.{Fore.MAGENTA}      Pretty cool ║")
        print(f"{Fore.MAGENTA}           ║{Fore.WHITE}[{Fore.LIGHTMAGENTA_EX}3{Fore.WHITE}] Exit{Fore.MAGENTA}                               ║")
        print(f"{Fore.LIGHTMAGENTA_EX}           ╚═══════════════════════════════════════╝")
        
        choice = keyboard.read_key()
        clear()
        
        if choice == "1":
            monitor_start()
        
        elif choice == "2":
            set_webhook()
            time.sleep(2)
        elif choice == "3":
            print(f"{Fore.LIGHTYELLOW_EX}Exiting Ghost Shell...")            
            exit(0)
        else:
            print("")
            print(f"{Fore.RED}Please select a valid option!")
            time.sleep(2)

if platform.system() == "Linux": 
    verifyroot()
    intro()
    check_if_chromedriver_installed()
    load_config()
    main_menu()
else:
    intro()
    check_if_chromedriver_installed()
    load_config()
    main_menu()
