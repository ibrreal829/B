# -*- coding: utf-8 -*-
"""
Instagram-HUnting(VIP).py - Ultimate Version

This script hunts for usernames that are available on both Instagram and Gmail.
It uses an advanced (but fragile) Gmail checking method and improved username generation.

Disclaimer:
Finding a "HIT" is extremely rare. This tool's success is not guaranteed.
Use a VPN to avoid IP blocks from Instagram and Google.
"""

import os
import sys
import time
import json
import random
import re
import uuid
import threading
import string
from secrets import token_hex

# --- Attempt to install required libraries ---
try:
    import requests
    from faker import Faker
    from user_agent import generate_user_agent
    import pycountry
except ImportError:
    print("One or more required libraries are not installed. Attempting to install...")
    os.system(f"{sys.executable} -m pip install requests faker user_agent pycountry")
    print("Libraries installed. Please restart the script.")
    sys.exit()

# --- Global Variables & Constants ---

# Console Colors
E = '\033[1;31m'
F = '\033[2;32m'
X = '\033[1;33m'
A = '\033[2;34m'
C = '\033[2;35m'
B = '\x1b[38;5;208m'
Y = '\033[1;34m'
U = '\x1b[1;37m'

# --- Counters & Threading Lock ---
stats = {
    "hit": 0,
    "ig_available": 0,
    "ig_taken": 0,
    "gmail_available": 0,
    "gmail_taken": 0,
}
stats_lock = threading.Lock()
current_email_checked = ""

# --- Initial Setup ---
fake = Faker()
session = requests.Session()

# --- Banner and User Input ---
def print_banner():
    banner = f'''{B}{E}=============================={B}
|{F}[+] YouTube    : {B}I Am Hacker Alok
|{F}[+] TeleGram   : {B}GrayHacker_Bot
|{F}[+] Instagram  : {B}HackerAlok2.0
|{F}[+] Tool       : {B}Available Hunter (Ultimate)
{E}=============================='''
    print(banner)

def get_user_input():
    try:
        token = input(f' {F}({C}1{F}) {Y}Enter Telegram Bot Token{F} : ' + E)
        chat_id = input(f' {F}({C}2{F}) {Y}Enter Your Telegram Chat ID{F} : ' + E)
        print(X + ' ═════════════════════════════════')
        return token, chat_id
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit()

# --- Core Functions ---
def display_stats():
    os.system('cls' if os.name == 'nt' else 'clear')
    with stats_lock:
        stats_display = f'''
{U}━━━━━━━━━━━━━━━━━━━━━━━━━
 Dev: @Hackeralokgray | @RdpFreeBot | The Ultimate Hunter
━━━━━━━━━━━━━━━━━━━━━━━━━
{F}[🎯] HITS (IG & Gmail Available)   » 「{stats["hit"]}」
━━━━━━━━━━━━━━━━━━━━━━━━━
{B}[✔] Instagram Available           » 「{stats["ig_available"]}」
{E}[✘] Instagram Taken               » 「{stats["ig_taken"]}」
{A}[✔] Gmail Available               » 「{stats["gmail_available"]}」
{X}[✘] Gmail Taken / Check Failed    » 「{stats["gmail_taken"]}」
━━━━━━━━━━━━━━━━━━━━━━━━━
{U}[i] Current Check » 「{current_email_checked}」
━━━━━━━━━━━━━━━━━━━━━━━━━'''
    print(stats_display)

def send_telegram_message(email, user):
    global TOKEN, CHAT_ID
    message = f'''
⋘─────━*HACKERALOK*━─────⋙
[🔥] ULTIMATE HIT!
[💌] Email ==> {email}
[👻] Username ==> {user}
[✅] Instagram and Gmail both are available!
[➡️] Register the Gmail, then reset the Instagram password.
⋘─────━❤️🌚━─────⋙
𝐁𝐘 : @hackeralokkahagaye
'''
    print(F + message)
    with stats_lock:
        stats["hit"] += 1

    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": message}
        session.post(url, data=data)
    except Exception as e:
        print(f"{E}Failed to send message to Telegram: {e}")

    with open('hits.txt', 'a', encoding='utf-8') as f:
        f.write(message + '\n\n')

# --- Advanced Gmail Availability Checker ---
def get_google_token():
    """Fetches a session token from Google. This is fragile."""
    try:
        headers = {"Accept-Language": "en-US,en;q=0.9", "User-Agent": generate_user_agent()}
        res = session.get('https://accounts.google.com/signup/v2/createaccount?flowName=GlifWebSignIn&flowEntry=SignUp', headers=headers)
        tok_match = re.search(r'data-initial-setup-data="%.@.null,null,null,null,null,null,null,null,null,&quot;(.*?)&quot;,null,null,null,&quot;(.*?)&', res.text)
        if not tok_match: return None, None
        tok = tok_match.group(2)
        host_cookie = res.cookies.get_dict().get('__Host-GAPS')
        if not host_cookie or not tok: return None, None
        with open("Tokenz.txt", "w") as f: f.write(f"{host_cookie}${tok}")
        return host_cookie, tok
    except Exception:
        return None, None

def check_gmail_availability(email, username):
    """Checks if a Gmail address is available using the advanced method."""
    try:
        with open("Tokenz.txt", "r") as f:
            line = f.readline().strip().split("$")
            host, tl = line[0], line[1]
    except (FileNotFoundError, IndexError):
        host, tl = get_google_token()
        if not host:
            with stats_lock: stats['gmail_taken'] += 1
            return

    headers = {
        'authority': 'accounts.google.com',
        'origin': 'https://accounts.google.com',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': generate_user_agent(),
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    data = f'f.req=%5B%22TL%3A{tl}%22%2C%22{username}%22%2C0%2C0%2C1%2Cnull%2C0%2C5167%5D'
    
    try:
        response = session.post(f'https://accounts.google.com/_/signup/usernameavailability?TL={tl}', headers=headers, data=data, cookies={'__Host-GAPS': host})
        if '"gf.uar",1' in response.text: # Code for "available"
            with stats_lock: stats['gmail_available'] += 1
            send_telegram_message(email, username)
        else:
            with stats_lock: stats['gmail_taken'] += 1
    except Exception:
        with stats_lock: stats['gmail_taken'] += 1


# --- Instagram Account Checker ---
def check_instagram_availability(email):
    global current_email_checked
    with stats_lock:
        current_email_checked = email

    username = email.split('@')[0]
    url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = session.get(url, headers=headers)
        if response.status_code == 404:
            # 404 means the user does not exist - it's available!
            with stats_lock:
                stats['ig_available'] += 1
            print(F + f"[✔] Instagram Available: @{username}. Now checking Gmail...")
            check_gmail_availability(email, username)
        else:
            # Any other status code (like 200) means the user exists
            with stats_lock:
                stats['ig_taken'] += 1
    except requests.exceptions.RequestException:
        # Network error
        with stats_lock:
            stats['ig_taken'] += 1
    
    display_stats()

# --- Main Worker ---
def worker():
    """Generates and checks potential usernames."""
    common_words = ['king', 'queen', 'prince', 'devil', 'angel', 'khan', 'sharma', 'singh', 'kumar', 'boss', 'player', 'gamer', 'rocky', 'boy', 'girl', 'love', 'official', 'star', 'guru']
    
    while True:
        try:
            # Generate a more realistic username
            name = fake.first_name().lower().replace(" ", "")
            word = random.choice(common_words)
            separator = random.choice(['.', '_', ''])
            number = random.choice([random.randint(1, 99), random.randint(1990, 2015)])
            
            patterns = [
                f"{name}{separator}{number}",
                f"{name}{separator}{word}",
                f"{word}{separator}{name}",
                f"{name}{word}{number}",
            ]
            username = random.choice(patterns)
            
            if len(username) < 6 or len(username) > 22:
                continue

            email = f"{username}@gmail.com"
            check_instagram_availability(email)
            time.sleep(random.uniform(1, 2.5))

        except Exception:
            time.sleep(5)


# --- Main Execution Block ---
if __name__ == "__main__":
    print_banner()
    TOKEN, CHAT_ID = get_user_input()
    if not TOKEN or not CHAT_ID:
        print(f"{E}Token and Chat ID cannot be empty. Exiting.")
        sys.exit()

    num_threads = 10 # You can increase this if you have a strong connection and VPN
    threads = []
    print(f"\n{F}Starting {num_threads} threads... Use a good VPN to avoid blocks.")
    print(f"{X}Remember: Hits are very rare. Let the script run for a long time.{U}")
    
    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        thread.daemon = True
        threads.append(thread)
        thread.start()

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print(f"\n{X}Stopping threads... Please wait.")
        sys.exit()