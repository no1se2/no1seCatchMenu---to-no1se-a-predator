from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from pathlib import Path
import os
import requests
import subprocess
from colorama import Fore, Back, Style, init
import platform
import random
import keyboard
import threading
import sys
import tkinter as tk
from tkinter import messagebox


#Only for linux users
if platform.system() == "Windows":
    print("")
else:
    if os.getuid() == 0:
        print(f"{Fore.GREEN}[✓] Running as root!")
        time.sleep(1)
    else:
        print(f"{Fore.RED}[✘] please run the script as root!")
        exit(1)

# art
art = """
        ██████  ██████  ██████  ███████ ██████      ██████  ██    ██     ███    ██  ██████   ██ ███████ ███████ 
        ██      ██    ██ ██   ██ ██      ██   ██     ██   ██  ██  ██      ████   ██ ██    ██ ███ ██      ██      
        ██      ██    ██ ██   ██ █████   ██   ██     ██████    ████       ██ ██  ██ ██    ██  ██ ███████ █████   
        ██      ██    ██ ██   ██ ██      ██   ██     ██   ██    ██        ██  ██ ██ ██    ██  ██      ██ ██      
        ██████  ██████  ██████  ███████ ██████      ██████     ██        ██   ████  ██████   ██ ███████ ███████ 
                                                1.0                                                                 
"""

art2 = """
        ██████╗ ██████╗ ██████╗ ███████╗██████╗     ██████╗ ██╗   ██╗    ███╗   ██╗ ██████╗  ██╗███████╗███████╗
        ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗    ██╔══██╗╚██╗ ██╔╝    ████╗  ██║██╔═══██╗███║██╔════╝██╔════╝
        ██║     ██║   ██║██║  ██║█████╗  ██║  ██║    ██████╔╝ ╚████╔╝     ██╔██╗ ██║██║   ██║╚██║███████╗█████╗  
        ██║     ██║   ██║██║  ██║██╔══╝  ██║  ██║    ██╔══██╗  ╚██╔╝      ██║╚██╗██║██║   ██║ ██║╚════██║██╔══╝  
        ╚██████╗╚██████╔╝██████╔╝███████╗██████╔╝    ██████╔╝   ██║       ██║ ╚████║╚██████╔╝ ██║███████║███████╗
        ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═════╝     ╚═════╝    ╚═╝       ╚═╝  ╚═══╝ ╚═════╝  ╚═╝╚══════╝╚══════╝
                                                2.0
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

init()

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



def msg_every_user():
    def stop_check():
        keyboard.wait('q')
        print(f"{Fore.RED} Stopping...")
        global running
        running = False
        driver.quit()
        time.sleep(2)
        
    
    global running
    running = True
    message_count = 0

    try:
        clear()
        print(Fore.LIGHTMAGENTA_EX + art2)
        # ------------setting the chromedriver------------------#
        if platform.system() == "Windows":
            PATH = "C:\\Windows\\chromedriver-win64\\chromedriver.exe"
        else:
            PATH = "/usr/local/bin/chromedriver-linux64/chromedriver"

        options = Options()
        options.headless = False
        options.add_argument('--log-level=3')
        options.add_argument('--silent')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-logging')


        service = Service(log_path=os.devnull)
        
        message = input(Fore.YELLOW + "[?] Enter the message you want to send: ")
        print()
        username = input(Fore.YELLOW + "[?] Enter username: ")
        print()
        #Asking the user if he wants to see the chromedriver or not...
        gui_or_not = input(Fore.YELLOW + "[?] Would you like to see the chrome tab? [y/n]: ")
        if gui_or_not.lower() == "n":
            options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")


        #-----The usual first step in automating catch chat---------#
        clear()
        print(Fore.LIGHTMAGENTA_EX + art2)

        
        driver = webdriver.Chrome(options=options,service=service)
        if gui_or_not.lower() == "n":
            print(f"{Fore.GREEN}[+] Resolution set to 1920x1080")
        else:
            driver.set_window_size(1280, 800)

        driver.get("https://catch-chat.com/")

        print(f"{Fore.GREEN}[+] Opening Catch Chat...")
        
        tos = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/button')
        time.sleep(2)
        tos.click()
        
        print(f"{Fore.GREEN}[+] Accepting the terms of service...")

        time.sleep(1)
        name = driver.find_element(By.ID, "inpNick")
        time.sleep(1)
        name.send_keys(username)
        
        print(f"{Fore.GREEN}[+] Setting up {username} as the username...")

        age = driver.find_element(By.ID, "inpAge")
        time.sleep(0.5)
        age.send_keys(18)

        print(f"{Fore.GREEN}[+] Setting up the age to 18")
        
        sex = driver.find_element(By.ID, "btnSex")
        time.sleep(0.5)
        sex.click()

        print(f"{Fore.GREEN}[+] Changing gender to female")
        
        time.sleep(0.5)
        sex.click()

        driver.find_element(By.XPATH, '/html/body/main/header/div[1]/button[4]').click()

        catchin = driver.find_element(By.ID, "btnCatchIn")
        time.sleep(0.5)
        catchin.click()
        print(f"{Fore.GREEN}[+] Starting to send messages to users.")
        time.sleep(2)
        


        online_users = driver.find_element(By.ID, "usrCap").get_attribute("data-c")
        clear()
        print(Fore.LIGHTMAGENTA_EX + art2)
        print(f"{Fore.LIGHTMAGENTA_EX}Your username [>]: {Fore.CYAN}{username}")
        print(f"{Fore.LIGHTMAGENTA_EX}Target User [>]: {Fore.CYAN}None")
        print(f"{Fore.LIGHTMAGENTA_EX}Online users [>]: {Fore.CYAN}{online_users}")
        print(f"{Fore.LIGHTMAGENTA_EX}Total messages sent so far [>]: {Fore.CYAN}0")
        print(f"{Fore.YELLOW}Press 'q' to stop...")

        stop_thread = threading.Thread(target=stop_check)
        stop_thread.start()
        
        #Selecting random users to send message to in a loop
        while running:
            try:
                online_users = driver.find_element(By.ID, "usrCap").get_attribute("data-c")
                user_buttons = driver.find_elements(By.ID, "usrFill")
                random_user_button = random.choice(user_buttons)
                random_user_button.click()
                time.sleep(1)
                random_user_name = driver.find_element(By.XPATH, '//div[@class="dit" and @data-sub]').get_attribute('title')
                #-------------Live status----------#
                sys.stdout.write("\033[F\033[K")  
                sys.stdout.write("\033[F\033[K")  
                sys.stdout.write("\033[F\033[K")  
                sys.stdout.write("\033[F\033[K") 
                sys.stdout.write("\033[F\033[K") 
                print(f"{Fore.LIGHTMAGENTA_EX}Your username [>]: {Fore.CYAN}{username}")
                print(f"{Fore.LIGHTMAGENTA_EX}Target User [>]: {Fore.CYAN}{random_user_name}")
                print(f"{Fore.LIGHTMAGENTA_EX}Online users [>]: {Fore.CYAN}{online_users}")
                print(f"{Fore.LIGHTMAGENTA_EX}Total messages sent so far [>]: {Fore.CYAN}{message_count}")
                print(f"{Fore.YELLOW}Press 'q' to stop...")
                #----------------------------------#
                user_message_box = driver.find_element(By.ID, "inpMsg")
                time.sleep(0.5)
                user_message_box.send_keys(message)
                time.sleep(1)
                driver.find_element(By.ID, "btnSend").click()
                page_source = driver.page_source
                #Check 1
                if "Catch אוסרת ומזהירה מפני שליחת מספרי טלפון!" in page_source:
                    user_message_box.send_keys(Keys.CONTROL, 'a')
                    time.sleep(1)
                    user_message_box.send_keys(Keys.BACKSPACE)

                message_count += 1
                
                #Checking if someone blocked you and if they did it will click ok
                try:
                    blocked_ok_button = driver.find_element(By.ID, "ok")
                    time.sleep(1)
                    blocked_ok_button.click()
                except NoSuchElementException:
                    pass

            except Exception as inner_e:
                if not running:
                    break
    except Exception as e:
        print(f"{Fore.RED}An Error occurred: {e}")
        print()
        print(f"{Fore.RED}Contact no1se.")
        exit(0)



#Second option
def send_msg_to_general():
    def stop_check():
        keyboard.wait('q')
        print(f"{Fore.RED} Stopping...")
        global running
        running = False
        driver.quit()
        time.sleep(2)
        

    global running
    running = True
    message_count = 0

    try:
        clear()
        print(Fore.LIGHTMAGENTA_EX + art2)
        # ------------setting the chromedriver------------------#
        if platform.system() == "Windows":
            PATH = "C:\\Windows\\chromedriver-win64\\chromedriver.exe"
        else:
            PATH = "/usr/local/bin/chromedriver-linux64/chromedriver"

        options = Options()
        options.headless = False
        options.add_argument('--log-level=3')
        options.add_argument('--silent')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-logging')


        service = Service(log_path=os.devnull)
        
        message = input(Fore.YELLOW + "[?] Enter the message you want to send: ")
        print()
        username = input(Fore.YELLOW + "[?] Enter username: ")
        print()
        #Asking the user if he wants to see the chromedriver or not...
        gui_or_not = input(Fore.YELLOW + "[?] Would you like to see the chrome tab? [y/n]: ")
        if gui_or_not.lower() == "n":
            options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")


        #-----The usual first step in automating catch chat---------#
        clear()
        print(Fore.LIGHTMAGENTA_EX + art2)

        
        driver = webdriver.Chrome(options=options,service=service)
        if gui_or_not.lower() == "n":
            print(f"{Fore.GREEN}[+] Resolution set to 1920x1080")
        else:
            driver.set_window_size(1280, 800)

        driver.get("https://catch-chat.com/")

        print(f"{Fore.GREEN}[+] Opening Catch Chat...")
        
        tos = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/button')
        time.sleep(2)
        tos.click()
        
        print(f"{Fore.GREEN}[+] Accepting the terms of service...")

        time.sleep(1)
        name = driver.find_element(By.ID, "inpNick")
        time.sleep(1)
        name.send_keys(username)
        
        print(f"{Fore.GREEN}[+] Setting up {username} as the username...")

        age = driver.find_element(By.ID, "inpAge")
        time.sleep(0.5)
        age.send_keys(18)

        print(f"{Fore.GREEN}[+] Setting up the age to 18")
        
        sex = driver.find_element(By.ID, "btnSex")
        time.sleep(0.5)
        sex.click()

        print(f"{Fore.GREEN}[+] Changing gender to female")
        
        time.sleep(0.5)
        sex.click()

        driver.find_element(By.XPATH, '/html/body/main/header/div[1]/button[4]').click()

        catchin = driver.find_element(By.ID, "btnCatchIn")
        time.sleep(0.5)
        catchin.click()
        print(f"{Fore.GREEN}[+] Starting to send messages in general chat.")
        time.sleep(2)
        


        online_users = driver.find_element(By.ID, "usrCap").get_attribute("data-c")
        clear()
        print(Fore.LIGHTMAGENTA_EX + art2)
        print(f"{Fore.LIGHTMAGENTA_EX}Your username [>]: {Fore.CYAN}{username}")
        print(f"{Fore.LIGHTMAGENTA_EX}Target Channel [>]: {Fore.CYAN}דיבורים")
        print(f"{Fore.LIGHTMAGENTA_EX}Online users [>]: {Fore.CYAN}{online_users}")
        print(f"{Fore.LIGHTMAGENTA_EX}[!] Sending message every {Fore.CYAN}8 {Fore.LIGHTMAGENTA_EX}seconds...")
        print(f"{Fore.LIGHTMAGENTA_EX}Total messages sent so far [>]: {Fore.CYAN}0")
        print(f"{Fore.YELLOW}Press 'q' to stop...")

        stop_thread = threading.Thread(target=stop_check)
        stop_thread.start()
        
        
        while running:
            try:
                online_users = driver.find_element(By.ID, "usrCap").get_attribute("data-c")
                channel_message_box = driver.find_element(By.ID, "inpMsg")
                time.sleep(8)
                channel_message_box.send_keys(message)
                
                driver.find_element(By.ID, "btnSend").click()
                
                #-------------Live status----------#
                sys.stdout.write("\033[F\033[K")  
                sys.stdout.write("\033[F\033[K")  
                sys.stdout.write("\033[F\033[K")  
                sys.stdout.write("\033[F\033[K") 
                sys.stdout.write("\033[F\033[K")
                sys.stdout.write("\033[F\033[K") 
                print(f"{Fore.LIGHTMAGENTA_EX}Your username [>]: {Fore.CYAN}{username}")
                print(f"{Fore.LIGHTMAGENTA_EX}Target Channel [>]: {Fore.CYAN}דיבורים")
                print(f"{Fore.LIGHTMAGENTA_EX}Online users [>]: {Fore.CYAN}{online_users}")
                print(f"{Fore.LIGHTMAGENTA_EX}[!] Sending message every {Fore.CYAN}8 {Fore.LIGHTMAGENTA_EX}seconds...")
                print(f"{Fore.LIGHTMAGENTA_EX}Total messages sent so far [>]: {Fore.CYAN}{message_count}")
                print(f"{Fore.YELLOW}Press 'q' to stop...")
                #----------------------------------#
 
                message_count += 1
            except Exception as inner_e:
                if not running:
                    break
    except Exception as e:
        print(f"{Fore.RED}An Error occurred: {e}")
        print()
        print(f"{Fore.RED}Contact no1se.")
        exit(0)

        
def random_pedo():
    def countdowntothelegalage(stop_event, estimated_time):
        while not stop_event.is_set() and estimated_time > 0:
            print(f"{Fore.LIGHTMAGENTA_EX}**Showing message in: {Fore.LIGHTCYAN_EX}{int(estimated_time)} {Fore.LIGHTMAGENTA_EX}seconds...**", end="\r")
            time.sleep(1)
            estimated_time -= 1
        print("\n")


    try:
        clear()
        print(Fore.LIGHTMAGENTA_EX + art2)
        # ------------setting the chromedriver------------------#
        if platform.system() == "Windows":
            PATH = "C:\\Windows\\chromedriver-win64\\chromedriver.exe"
        else:
            PATH = "/usr/local/bin/chromedriver-linux64/chromedriver"

        options = Options()
        options.headless = False
        options.add_argument('--log-level=3')
        options.add_argument('--silent')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-logging')
        options.add_argument("--headless")
        


        service = Service(log_path=os.devnull)

        driver = webdriver.Chrome(options=options,service=service)

        estimated_time = 4
        stop_event = threading.Event()
        countdowntothelegalage_thread = threading.Thread(target=countdowntothelegalage, args=(stop_event, estimated_time))
        countdowntothelegalage_thread.start()

        driver.get("https://catch-chat.com/")
        time.sleep(1)
        #tos
        driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/button').click()
        time.sleep(2)
        #close button
        driver.find_element(By.XPATH, '/html/body/div[1]/button').click()
        time.sleep(1)
        name_element = driver.find_element("xpath", '/html/body/main/div[2]/div[1]/div[2]/div[9]/button').get_attribute("title")
        message_element = driver.find_element(By.CSS_SELECTOR, '.bub').text

        stop_event.set()
        countdowntothelegalage_thread.join()

        root = tk.Tk()
        root.withdraw()

        message = f"{name_element}: {message_element}"
        print(f"{Fore.GREEN}[+] Click ok!")
        messagebox.showinfo("Fun fact: ניקי אוהב בנות 14", message)
        root.destroy()
        print(f"{Fore.YELLOW}[!] Returning to main_menu...")
        driver.quit()
        
    except Exception as e:
        print(f"{Fore.RED}An Error occurred: {e}")
        print()
        print(f"{Fore.RED}Contact no1se.")
        exit(0)



def main_menu():
    while True:
        width = 120
        print(Fore.LIGHTMAGENTA_EX)
        #Squidward
        clear()
        print("        .--'''''''''--.  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀#####################################(*.        .(##############################")
        print("     .'      .---.      '.                 #############################,                        .#########################")
        print("    /    .-----------.    \'               ########################.                                 ######################")
        print("   /        .-----.        \'              ####################*                                       ####################")
        print("   |       .-.   .-.       |               #################(                .##############/            ##################")
        print("   |      /   \ /   \      |               ###############*              ,#######################         (################")
        print("    \    | .-. | .-. |    /                ##############              #########################           .###############")
        print("     '-._| | | | | | |_.-'⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   #############             #########(            *##/             .##############")
        print("         | '-' | '-' |⠀⠀⠀⠀⠀⠀⠀⠀⠀         ⠀#############            ########                                 /#############")
        print("          \___/ \___/⠀                     ############(           #######(                                   #############")
        print("       _.-'  /   \  `-._⠀                  #############          *######(                                    ,############")
        print("     .' _.--|     |--._ '.⠀                #############          /######/                                     ############")
        print("     ' _...-|     |-..._ '                 #############,         ,#######                                     ############")
        print("            |     |                       ⠀##############          ########                                    ############")
        print("            '.___.'                        ##############/          ########*                                 .############")
        print("                                           ###############,          /#########/          .####               #############")
        print("                                           ################.           (########################,            (#############")
        print("                                           #################*             ######################,          .###############")
        print("                                           ###################                ,############/             ,#################")
        print("                                           ####################(                                      .####################")
        print("                                           #######################                                .########################")
        print("                                           ##########################.                       (#############################")
        #Squidward
        print(Fore.CYAN + "Welcome to no1seCatchMenu - to no1se a predator.".center(width))
        print(Fore.MAGENTA + "Please select an option:".center(width))
        print(f"{Fore.BLUE}1. Send a message to every user on the site.{Style.RESET_ALL}".center(width))
        print(f"{Fore.GREEN}2. Send a repeated message in the general chat.".center(width))
        print(f"{Fore.LIGHTYELLOW_EX}3. Receive a random message from a predator".center(width))
        print(f"{Fore.RED}4. Exit{Style.RESET_ALL}".center(width))
        choice = input(f"{Fore.YELLOW}Enter your choice [>]{Fore.WHITE} ")
        
        if choice == "1":
            msg_every_user()

        elif choice == "2":
            send_msg_to_general()

        elif choice == "3":
            random_pedo()
        elif choice == "4":
            print(f"{Fore.LIGHTYELLOW_EX}Bye! :(".center(width))
            exit(1)
        else:
            print("")
            print(f"{Fore.RED}Please select a valid option!".center(width))
            time.sleep(2)
        

intro()
check_if_chromedriver_installed()
main_menu()
