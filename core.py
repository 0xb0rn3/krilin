#!/usr/bin/env python3
"""
Krilin Core v0.3 - Unified Security Framework
Author: 0xbv1(0xb0rn3) | q4n0@proton.me | X/Discord: oxbv1 | IG: theehiv3
"""

import os
import subprocess
import sys
import shutil
import time
import re
from pathlib import Path

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
BOLD = '\033[1m'
NORMAL = '\033[0m'

KALI_REPO = "deb http://http.kali.org/kali kali-rolling main contrib non-free non-free-firmware"

LOG_FILE = "/var/log/krilin_operations.log"

KALI_CATEGORIES = {
    "1": ("Information Gathering", ["nmap", "dnsrecon", "theharvester", "recon-ng", "maltego"]),
    "2": ("Vulnerability Analysis", ["nikto", "sqlmap", "lynis", "openvas", "wapiti"]),
    "3": ("Exploitation Tools", ["metasploit-framework", "exploitdb", "set", "beef-xss"]),
    "4": ("Wireless Attacks", ["aircrack-ng", "reaver", "wifite", "kismet", "pixiewps"]),
    "5": ("Web Application", ["burpsuite", "zaproxy", "wfuzz", "dirb", "gobuster"]),
    "6": ("Password Attacks", ["hydra", "john", "hashcat", "crunch", "medusa"]),
    "7": ("Individual Tools", []),
    "8": ("All Kali Tools", [])
}

PARROT_EDITIONS = {
    "1": ("Core Edition", ["bash", "wget", "gnupg", "parrot-core"]),
    "2": ("Home Edition", ["parrot-interface-home", "parrot-desktop-mate", "parrot-wallpapers", 
                          "firefox-esr", "parrot-firefox-profiles", "vscodium"]),
    "3": ("Security Edition", ["parrot-interface-home", "parrot-desktop-mate", "parrot-tools-full",
                               "firefox-esr", "parrot-firefox-profiles", "vscodium"]),
    "4": ("HTB Edition", ["parrot-interface-home", "parrot-desktop-mate", "parrot-tools-full",
                         "hackthebox-icon-theme", "win10-icon-theme", "firefox-esr", "vscodium"])
}

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"{CYAN}[*]{NORMAL} {msg}")

def log_ok(msg):
    print(f"{GREEN}[+]{NORMAL} {msg}")

def log_warn(msg):
    print(f"{YELLOW}[!]{NORMAL} {msg}")

def log_err(msg):
    print(f"{RED}[-]{NORMAL} {msg}")

def run_cmd(cmd, silent=False):
    try:
        if silent:
            subprocess.run(cmd, shell=True, check=True, 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def check_root():
    if os.geteuid() != 0:
        log_err("Root access required")
        sys.exit(1)

def is_docker():
    return os.path.exists("/.dockerenv") or \
           os.path.exists("/proc/1/cgroup") and \
           "docker" in open("/proc/1/cgroup").read()

def fix_dpkg():
    log("Fixing package system...")
    
    lock_files = [
        "/var/lib/apt/lists/lock",
        "/var/cache/apt/archives/lock",
        "/var/lib/dpkg/lock",
        "/var/lib/dpkg/lock-frontend"
    ]
    
    for lock in lock_files:
        if os.path.exists(lock):
            try:
                os.remove(lock)
            except:
                pass
    
    run_cmd("dpkg --configure -a", silent=True)
    run_cmd("apt-get install -f -y", silent=True)
    run_cmd("apt-get clean", silent=True)
    run_cmd("apt-get update --fix-missing", silent=True)

def add_kali_repo():
    log("Adding Kali repository...")
    
    keyring_urls = [
        "https://archive.kali.org/kali/pool/main/k/kali-archive-keyring/kali-archive-keyring_2025.1_all.deb",
        "https://http.kali.org/kali/pool/main/k/kali-archive-keyring/kali-archive-keyring_2022.1_all.deb"
    ]
    
    keyring_file = "/tmp/kali-keyring.deb"
    
    for url in keyring_urls:
        if run_cmd(f"wget -q -O {keyring_file} {url}", silent=True):
            if run_cmd(f"dpkg -i {keyring_file}", silent=True):
                os.remove(keyring_file)
                break
    
    with open("/etc/apt/sources.list.d/kali-temp.list", "w") as f:
        f.write(f"{KALI_REPO}\n")
    
    run_cmd("apt-get update", silent=True)
    log_ok("Kali repository added")

def add_parrot_repo():
    log("Adding Parrot repository...")
    
    keyring_url = "https://deb.parrot.sh/parrot/pool/main/p/parrot-archive-keyring/parrot-archive-keyring_2024.12_all.deb"
    keyring_file = "/tmp/parrot-keyring.deb"
    
    if run_cmd(f"wget -q -O {keyring_file} {keyring_url}", silent=True):
        run_cmd(f"apt install -y {keyring_file}", silent=True)
        if os.path.exists(keyring_file):
            os.remove(keyring_file)
    
    parrot_list = """## Parrot Security Repositories - Managed by Krilin
deb https://deb.parrot.sh/parrot echo main contrib non-free non-free-firmware
deb https://deb.parrot.sh/direct/parrot echo-security main contrib non-free non-free-firmware
deb https://deb.parrot.sh/parrot echo-backports main contrib non-free non-free-firmware
"""
    
    with open("/etc/apt/sources.list.d/parrot.list", "w") as f:
        f.write(parrot_list)
    
    sources_list = """# This file is empty, feel free to
# add here your custom APT repositories

# The default Parrot repositories
# are NOT here. If you want to
# edit them, take a look into
#    /etc/apt/sources.list.d/parrot.list
"""
    
    with open("/etc/apt/sources.list", "w") as f:
        f.write(sources_list)
    
    listchanges_conf = """[apt]
frontend=pager
which=news
email_address=root
email_format=text
confirm=false
headers=false
reverse=false
save_seen=/var/lib/apt/listchanges.db
"""
    
    with open("/etc/apt/listchanges.conf", "w") as f:
        f.write(listchanges_conf)
    
    os_release = """PRETTY_NAME="Parrot Security 7.0 (echo)"
NAME="Parrot Security"
VERSION_ID="7.0"
VERSION="7.0 (echo)"
VERSION_CODENAME=echo
ID=debian
HOME_URL="https://www.parrotsec.org/"
SUPPORT_URL="https://www.parrotsec.org/community/"
BUG_REPORT_URL="https://gitlab.com/parrotsec/"
"""
    
    with open("/etc/os-release", "w") as f:
        f.write(os_release)
    
    run_cmd("apt-get update", silent=True)
    log_ok("Parrot repository configured")

def remove_repo(repo_type):
    log(f"Removing {repo_type} repository...")
    
    fix_dpkg()
    
    if repo_type == "kali":
        repo_file = "/etc/apt/sources.list.d/kali-temp.list"
    elif repo_type == "parrot":
        repo_file = "/etc/apt/sources.list.d/parrot.list"
    else:
        return
    
    if os.path.exists(repo_file):
        os.remove(repo_file)
    
    run_cmd("apt-get update", silent=True)
    log_ok("Repository removed")

def install_package(package, max_retries=3):
    for attempt in range(1, max_retries + 1):
        result = subprocess.run(
            ["dpkg", "-l", package],
            capture_output=True,
            text=True
        )
        
        if f"ii  {package}" in result.stdout:
            log_ok(f"{package} already installed")
            return True
        
        log(f"Installing {package} (attempt {attempt}/{max_retries})...")
        
        if run_cmd(f"apt-get install -y -qq --no-install-recommends {package}", silent=True):
            log_ok(f"{package} installed")
            return True
        
        if attempt < max_retries:
            fix_dpkg()
            time.sleep(2)
    
    log_err(f"Failed to install {package}")
    return False

def install_packages(packages):
    failed = []
    success = []
    
    for pkg in packages:
        if install_package(pkg):
            success.append(pkg)
        else:
            failed.append(pkg)
    
    print(f"\n{BOLD}{BLUE}{'='*50}{NORMAL}")
    if success:
        log_ok(f"Installed: {len(success)} packages")
    if failed:
        log_warn(f"Failed: {len(failed)} packages")
        for pkg in failed[:10]:
            print(f"  - {pkg}")
    print(f"{BOLD}{BLUE}{'='*50}{NORMAL}\n")

def select_custom_tools():
    print(f"{CYAN}Enter tool names separated by spaces:{NORMAL}")
    print(f"{YELLOW}Example: nmap dirb nikto sqlmap metasploit-framework{NORMAL}")
    tools = input(f"{GREEN}Tools: {NORMAL}").strip().split()
    return tools if tools else []

def fetch_all_kali_tools():
    fallback_tools = [
        "nmap", "masscan", "dnsrecon", "theharvester", "nikto", "sqlmap",
        "wpscan", "lynis", "openvas", "metasploit-framework", "exploitdb",
        "set", "beef-xss", "aircrack-ng", "wifite", "reaver", "kismet",
        "burpsuite", "zaproxy", "dirb", "gobuster", "ffuf", "hydra",
        "john", "hashcat", "crunch", "medusa", "wireshark", "ettercap-text-only",
        "responder", "mitmproxy", "bettercap", "autopsy", "binwalk",
        "foremost", "volatility", "radare2", "gdb"
    ]
    
    try:
        add_kali_repo()
        result = subprocess.run(
            ["apt-cache", "search", "kali-"],
            stdout=subprocess.PIPE,
            text=True,
            check=False
        )
        
        if result.stdout:
            tools = []
            for line in result.stdout.split("\n"):
                if line.strip():
                    pkg = line.split(" - ")[0].strip()
                    if pkg:
                        tools.append(pkg)
            
            if tools:
                return list(set(tools + fallback_tools))
    except:
        pass
    
    return fallback_tools

def install_all_kali_tools():
    print(f"\n{RED}{BOLD}{'='*60}{NORMAL}")
    print(f"{RED}{BOLD}              WARNING{NORMAL}")
    print(f"{RED}{BOLD}{'='*60}{NORMAL}")
    print(f"{YELLOW}  * 10+ GB download size{NORMAL}")
    print(f"{YELLOW}  * Several hours installation time{NORMAL}")
    print(f"{YELLOW}  * May cause system conflicts{NORMAL}")
    print(f"{RED}{BOLD}{'='*60}{NORMAL}\n")
    
    confirm = input(f"{RED}Type 'I ACCEPT' to continue: {NORMAL}").strip()
    if confirm != "I ACCEPT":
        log_warn("Installation cancelled")
        return
    
    tools = fetch_all_kali_tools()
    log(f"Found {len(tools)} tools")
    
    try:
        add_kali_repo()
        fix_dpkg()
        install_packages(tools)
    finally:
        remove_repo("kali")

def install_kali_tools(category, packages):
    if category == "All Kali Tools":
        install_all_kali_tools()
        return
    elif category == "Individual Tools":
        packages = select_custom_tools()
        if not packages:
            return
    
    log(f"Installing {category}...")
    
    try:
        add_kali_repo()
        fix_dpkg()
        install_packages(packages)
    finally:
        remove_repo("kali")

def install_parrot_edition(edition, packages):
    log(f"Installing Parrot {edition}...")
    
    if is_docker() and "Home" in edition:
        log_warn("Desktop environment in Docker may have limited functionality")
    
    try:
        add_parrot_repo()
        fix_dpkg()
        
        run_cmd("apt-get update", silent=True)
        run_cmd("apt-get upgrade -y", silent=True)
        
        if os.uname().machine == "aarch64":
            run_cmd("apt-mark hold broadcom-sta-dkms", silent=True)
        
        install_packages(packages)
        
        log_ok(f"Parrot {edition} installation complete")
        
        if "Home" in edition or "Security" in edition or "HTB" in edition:
            log_warn("Reboot required for desktop environment")
    finally:
        pass

def display_main_menu():
    print(f"\n{BOLD}{BLUE}╔{'═'*55}╗{NORMAL}")
    print(f"{BOLD}{BLUE}║{CYAN}     KRILIN SECURITY FRAMEWORK - MAIN MENU{BLUE}      ║{NORMAL}")
    print(f"{BOLD}{BLUE}╠{'═'*55}╣{NORMAL}")
    print(f"{BOLD}{BLUE}║{YELLOW} [1] Kali Linux Tools{' '*33}{BLUE}║{NORMAL}")
    print(f"{BOLD}{BLUE}║{YELLOW} [2] Parrot Security Conversion{' '*24}{BLUE}║{NORMAL}")
    print(f"{BOLD}{BLUE}║{YELLOW} [0] Exit{' '*45}{BLUE}║{NORMAL}")
    print(f"{BOLD}{BLUE}╚{'═'*55}╝{NORMAL}")

def display_kali_menu():
    print(f"\n{BOLD}{BLUE}╔{'═'*55}╗{NORMAL}")
    print(f"{BOLD}{BLUE}║{CYAN}     KALI LINUX TOOLS INSTALLATION{BLUE}              ║{NORMAL}")
    print(f"{BOLD}{BLUE}╠{'═'*55}╣{NORMAL}")
    
    for key, (category, _) in KALI_CATEGORIES.items():
        icon = "[!]" if key == "8" else "[*]"
        warning = f" {MAGENTA}(10+ GB){NORMAL}" if key == "8" else ""
        padding = ' ' * (40 - len(category))
        print(f"{BOLD}{BLUE}║{CYAN} [{key}] {icon} {category}{padding}{warning}{BLUE}║{NORMAL}")
    
    print(f"{BOLD}{BLUE}║{YELLOW} [0] Back{' '*45}{BLUE}║{NORMAL}")
    print(f"{BOLD}{BLUE}╚{'═'*55}╝{NORMAL}")

def display_parrot_menu():
    print(f"\n{BOLD}{BLUE}╔{'═'*55}╗{NORMAL}")
    print(f"{BOLD}{BLUE}║{CYAN}     PARROT SECURITY CONVERSION{BLUE}                 ║{NORMAL}")
    print(f"{BOLD}{BLUE}╠{'═'*55}╣{NORMAL}")
    
    for key, (edition, _) in PARROT_EDITIONS.items():
        icon = "[>]" if "Core" in edition else "[*]"
        padding = ' ' * (42 - len(edition))
        print(f"{BOLD}{BLUE}║{CYAN} [{key}] {icon} {edition}{padding}{BLUE}║{NORMAL}")
    
    print(f"{BOLD}{BLUE}║{YELLOW} [0] Back{' '*45}{BLUE}║{NORMAL}")
    print(f"{BOLD}{BLUE}╚{'═'*55}╝{NORMAL}")

def main():
    check_root()
    
    Path(LOG_FILE).touch(exist_ok=True)
    
    log("Krilin Security Framework v0.3 started")
    
    while True:
        display_main_menu()
        
        try:
            choice = input(f"\n{GREEN}Select option: {NORMAL}").strip()
            
            if choice == "0":
                log("Session ended")
                print(f"{BLUE}Stay tactical!{NORMAL}")
                break
            
            elif choice == "1":
                while True:
                    display_kali_menu()
                    kali_choice = input(f"\n{GREEN}Select option: {NORMAL}").strip()
                    
                    if kali_choice == "0":
                        break
                    elif kali_choice in KALI_CATEGORIES:
                        category, packages = KALI_CATEGORIES[kali_choice]
                        install_kali_tools(category, packages)
                    else:
                        log_err("Invalid option")
            
            elif choice == "2":
                while True:
                    display_parrot_menu()
                    parrot_choice = input(f"\n{GREEN}Select option: {NORMAL}").strip()
                    
                    if parrot_choice == "0":
                        break
                    elif parrot_choice in PARROT_EDITIONS:
                        edition, packages = PARROT_EDITIONS[parrot_choice]
                        install_parrot_edition(edition, packages)
                    else:
                        log_err("Invalid option")
            
            else:
                log_err("Invalid option")
        
        except KeyboardInterrupt:
            print(f"\n{YELLOW}[!]{NORMAL} Interrupted")
            continue
        except EOFError:
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!]{NORMAL} Terminated")
        sys.exit(0)
    except Exception as e:
        log_err(f"Error: {e}")
        sys.exit(1)
