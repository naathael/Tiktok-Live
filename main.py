import pyautogui
from pynput.keyboard import Controller
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, DisconnectEvent, ViewerUpdateEvent, GiftEvent
import time
import logging
import psutil
import colorama
import os
import difflib
import re

pyautogui.FAILSAFE = False
keyboard = Controller()
username_color = colorama.Fore.CYAN
ram_color = colorama.Fore.GREEN
time_color = colorama.Fore.YELLOW
spectator_color = colorama.Fore.MAGENTA
message_color = colorama.Fore.BLUE
status_online_color = colorama.Fore.GREEN
status_offline_color = colorama.Fore.RED
gift_color = colorama.Fore.RED
money_color = colorama.Fore.YELLOW  
message_count = 0
spectator_count = 0
online_status = False
last_gift = None
cumulated_gift_count = 0



def connect_to_tiktok(client, account):
    global online_status
    try:
        client.run()
        online_status = True
    except Exception as e:
        online_status = False
        logging.error(f"Erreur de connexion : {e}")
        time.sleep(0.1)

def print_interface(account):
    os.system('clear' if os.name == 'posix' else 'cls')

    if online_status:
        current_time = time.time() - start_time if start_time else 0
        spectator_info = f"Spectateur : {colored_fade(spectator_count, spectator_color)}"
        message_info = f"Message : {colored_fade(message_count, message_color)}"
        ram_percent = psutil.virtual_memory().percent
        ram_info = f"Ram : {ram_percent}%"
        username_info = colored_fade(account, username_color)
        time_info = f"Temps depuis le lancement : {format_time(current_time)}"

        status_info = f"Status : {colored_fade('En ligne', status_online_color)}"
        gift_info = f"Cadeau : {colored_fade(last_gift, gift_color) if last_gift else 'Aucun'}"
        cumulated_gift_info = f"Cumulation cadeau : {colored_fade(cumulated_gift_count, gift_color)}"
        

        print("---------------------------")
        print(colored_fade(username_info, username_color))
        print(f"{ram_color}{ram_info}{colorama.Fore.RESET}")
        print(f"{time_color}{time_info}{colorama.Fore.RESET}")
        print(f"{spectator_color}{spectator_info}{colorama.Fore.RESET}")
        print(f"{message_color}{message_info}{colorama.Fore.RESET}")
        print(status_info)
        print(gift_info)
        print(cumulated_gift_info)
        print("---------------------------")
    else:
        print(colored_fade(account, username_color))
        print(f"Erreur de connexion. Veuillez réessayer.")
        logging.error("Erreur de connexion. Veuillez réessayer.")

def colored_fade(text, color):
    return f"{color}{text}{colorama.Fore.RESET}"


def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)}:{int(minutes)}:{int(seconds)}"


actions = {

    'example1': lambda: example1('', duration=0.1),
    'example2': lambda: example2(''),

}


gift_actions = {
    'rose': lambda: example1('z', duration=10),
}

keys = list(actions.keys()) + list(gift_actions.keys())

def is_typo(word1, word2):
    return sum(a != b for a, b in zip(word1, word2)) <= 1

def find_closest_action(misspelled_key):
    return difflib.get_close_matches(misspelled_key, keys, n=1, cutoff=0.8)

def example1(key, duration):
    try:
        keyboard.press(key)
        time.sleep(duration)
        keyboard.release(key)
    except ValueError as e:
        logging.error(f"Touche non reconnue : {e}")

def example2(key):
    try:
        keyboard.press(key)
        keyboard.release(key)
    except ValueError as e:
        logging.error(f"Touche non reconnue : {e}")



def is_typo(word1, word2):
    return sum(a != b for a, b in zip(word1, word2)) <= 1

def find_closest_action(misspelled_key):
    return next((key for key in keys if is_typo(misspelled_key, key)), None)

account = input("Entrez votre pseudo TikTok : ")

client = TikTokLiveClient(unique_id=account)

@client.on("connect")
async def on_connect(_: ConnectEvent):
    global start_time, online_status
    start_time = time.time()
    online_status = True
    print_interface(account)

@client.on("disconnect")
async def on_disconnect(event: DisconnectEvent):
    global online_status
    online_status = False
    print_interface(account)
    print("Déconnexion. Reconnexion en cours...")

@client.on("comment")
async def on_comment(event: CommentEvent):
    global message_count
    message_count += 1

    key = event.comment
    closest_action = find_closest_action(key)
    if closest_action:
        actions[closest_action]()
    print_interface(account)

@client.on("viewer_update")
async def on_viewer_update(event: ViewerUpdateEvent):
    global spectator_count
    spectator_count = event.viewer_count
    print_interface(account)

@client.on("gift")
async def on_gift(event: GiftEvent):
    global cumulated_gift_count

    
    count_match = re.search(r'count=(\d+)', event.gift.info.description)
    count = int(count_match.group(1)) if count_match else 0


    cumulated_gift_count += count


    gift_name = event.gift.info.name.lower()
    if gift_name in gift_actions:
        gift_actions[gift_name]()

    print_interface(account)
while not online_status:
    connect_to_tiktok(client, account)
    print_interface(account)

