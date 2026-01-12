#!/usr/bin/env python3
"""
Krilin Core v1.0
Author: 0xb0rn3 (0xbv1)
Mail: q4n0@proton.me | X & Discord: 0xbv1 | IG: theehiv3
"""

import os
import sys
import subprocess
import time
import shutil
from pathlib import Path

try:
    import requests
    HAS_REQ = True
except ImportError:
    HAS_REQ = False

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
C = '\033[96m'
M = '\033[95m'
N = '\033[0m'
BOLD = '\033[1m'

VERSION = "1.0"
KALI_REPO = "deb http://http.kali.org/kali kali-rolling main contrib non-free non-free-firmware"
PARROT_REPO = "deb https://deb.parrot.sh/parrot/ parrot main contrib non-free non-free-firmware"

class Logger:
    @staticmethod
    def info(msg): print(f"{C}[*]{N} {msg}")
    
    @staticmethod
    def ok(msg): print(f"{G}[+]{N} {msg}")
    
    @staticmethod
    def warn(msg): print(f"{Y}[!]{N} {msg}")
    
    @staticmethod
    def err(msg): print(f"{R}[✗]{N} {msg}")

class System:
    @staticmethod
    def is_root():
        return os.geteuid() == 0
    
    @staticmethod
    def is_debian():
        return os.path.exists("/etc/debian_version")
    
    @staticmethod
    def is_docker():
        if os.path.exists("/.dockerenv"):
            return True
        try:
            with open("/proc/1/cgroup") as f:
                return "docker" in f.read() or "containerd" in f.read()
        except:
            return False
    
    @staticmethod
    def get_space():
        stat = os.statvfs('/')
        return (stat.f_bavail * stat.f_frsize) / (1024**3)
    
    @staticmethod
    def info():
        data = {}
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if "=" in line:
                        k, v = line.strip().split("=", 1)
                        data[k] = v.strip('"')
        except:
            pass
        
        data['kernel'] = os.uname().release
        data['arch'] = os.uname().machine
        
        try:
            with open("/proc/meminfo") as f:
                for line in f:
                    if "MemTotal" in line:
                        ram_kb = int(line.split()[1])
                        data['ram'] = round(ram_kb / 1024 / 1024, 1)
                        break
        except:
            data['ram'] = 0
        
        return data

class Package:
    def __init__(self):
        self.failed = []
    
    def fix(self):
        Logger.info("Fixing package system...")
        
        locks = [
            "/var/lib/apt/lists/lock",
            "/var/cache/apt/archives/lock",
            "/var/lib/dpkg/lock",
            "/var/lib/dpkg/lock-frontend"
        ]
        
        for lock in locks:
            if os.path.exists(lock):
                try:
                    os.remove(lock)
                except:
                    pass
        
        subprocess.run(["killall", "-9", "apt-get"], stderr=subprocess.DEVNULL, check=False)
        subprocess.run(["killall", "-9", "dpkg"], stderr=subprocess.DEVNULL, check=False)
        subprocess.run(["dpkg", "--configure", "-a"], stderr=subprocess.DEVNULL, check=False)
        subprocess.run(["apt-get", "install", "-f", "-y"], stderr=subprocess.DEVNULL, check=False)
        subprocess.run(["apt-get", "clean"], check=False)
        subprocess.run(["apt-get", "update", "-qq"], stderr=subprocess.DEVNULL, check=False)
        
        Logger.ok("Package system ready")
    
    def block_rpcbind(self):
        Logger.info("Blocking rpcbind...")
        
        if self.installed("rpcbind"):
            subprocess.run(["systemctl", "stop", "rpcbind"], stderr=subprocess.DEVNULL, check=False)
            subprocess.run(["apt-get", "remove", "--purge", "-y", "rpcbind"], stderr=subprocess.DEVNULL, check=False)
        
        prefs = "/etc/apt/preferences.d/krilin-block"
        with open(prefs, "w") as f:
            f.write("Package: rpcbind\nPin: release *\nPin-Priority: -1\n\n")
            f.write("Package: nfs-common\nPin: release *\nPin-Priority: -1\n")
        
        Logger.ok("rpcbind blocked")
    
    def installed(self, pkg):
        result = subprocess.run(
            ["dpkg", "-l", pkg],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        return f"ii  {pkg}" in result.stdout
    
    def install(self, pkg, retries=3):
        if self.installed(pkg):
            return True
        
        for attempt in range(1, retries + 1):
            Logger.info(f"Installing {pkg} ({attempt}/{retries})...")
            
            result = subprocess.run(
                ["apt-get", "install", "-y", "-qq", "--no-install-recommends", pkg],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False
            )
            
            if result.returncode == 0:
                Logger.ok(f"Installed: {pkg}")
                return True
            
            if attempt < retries:
                time.sleep(2)
                self.fix()
        
        Logger.err(f"Failed: {pkg}")
        self.failed.append(pkg)
        return False
    
    def install_batch(self, pkgs):
        success = sum(1 for pkg in pkgs if self.install(pkg))
        failed = len(pkgs) - success
        Logger.info(f"Results: {success} installed, {failed} failed")
        return success, failed

class Repo:
    @staticmethod
    def add_kali():
        Logger.info("Adding Kali repository...")
        
        urls = [
            "https://archive.kali.org/kali/pool/main/k/kali-archive-keyring/kali-archive-keyring_2025.1_all.deb",
            "https://http.kali.org/kali/pool/main/k/kali-archive-keyring/kali-archive-keyring_2024.3_all.deb",
        ]
        
        for url in urls:
            try:
                subprocess.run(
                    ["wget", "-q", "-O", "/tmp/kali-key.deb", url],
                    timeout=30,
                    check=True
                )
                subprocess.run(["dpkg", "-i", "/tmp/kali-key.deb"], check=True)
                break
            except:
                continue
        
        with open("/etc/apt/sources.list.d/krilin-kali.list", "w") as f:
            f.write(f"{KALI_REPO}\n")
        
        subprocess.run(["apt-get", "update", "-qq"], stderr=subprocess.DEVNULL, check=False)
        Logger.ok("Kali repository ready")
    
    @staticmethod
    def add_parrot():
        Logger.info("Adding Parrot repository...")
        
        urls = [
            "https://deb.parrot.sh/parrot/pool/main/p/parrot-archive-keyring/parrot-archive-keyring_2024.12_all.deb",
            "https://deb.parrotsec.org/parrot/pool/main/p/parrot-archive-keyring/parrot-archive-keyring_2024.12_all.deb",
        ]
        
        for url in urls:
            try:
                subprocess.run(
                    ["wget", "-q", "-O", "/tmp/parrot-key.deb", url],
                    timeout=30,
                    check=True
                )
                subprocess.run(["dpkg", "-i", "/tmp/parrot-key.deb"], check=True)
                break
            except:
                continue
        
        with open("/etc/apt/sources.list.d/krilin-parrot.list", "w") as f:
            f.write(f"{PARROT_REPO}\n")
        
        subprocess.run(["apt-get", "update", "-qq"], stderr=subprocess.DEVNULL, check=False)
        Logger.ok("Parrot repository ready")
    
    @staticmethod
    def cleanup():
        Logger.info("Removing repositories...")
        
        for repo in ["/etc/apt/sources.list.d/krilin-kali.list", "/etc/apt/sources.list.d/krilin-parrot.list"]:
            if os.path.exists(repo):
                try:
                    os.remove(repo)
                except:
                    pass
        
        subprocess.run(["apt-get", "update", "-qq"], stderr=subprocess.DEVNULL, check=False)
        Logger.ok("Repositories cleaned")

def banner():
    print(f"""
{C}{BOLD}██╗  ██╗{R}██████╗ {Y}██╗{G}██╗     {B}██╗{M}███╗   ██╗{N}
{C}{BOLD}██║ ██╔╝{R}██╔══██╗{Y}██║{G}██║     {B}██║{M}████╗  ██║{N}
{C}{BOLD}█████╔╝ {R}██████╔╝{Y}██║{G}██║     {B}██║{M}██╔██╗ ██║{N}
{C}{BOLD}██╔═██╗ {R}██╔══██╗{Y}██║{G}██║     {B}██║{M}██║╚██╗██║{N}
{C}{BOLD}██║  ██╗{R}██║  ██║{Y}██║{G}███████╗{B}██║{M}██║ ╚████║{N}
{C}{BOLD}╚═╝  ╚═╝{R}╚═╝  ╚═╝{Y}╚═╝{G}╚══════╝{B}╚═╝{M}╚═╝  ╚═══╝{N}

{B}{BOLD}Security Framework v{VERSION}{N}
{G}Kali Linux & Parrot Security OS Support{N}

{M}By: 0xb0rn3 (0xbv1){N}
{M}Mail: q4n0@proton.me | X & Discord: 0xbv1{N}
{M}Instagram: theehiv3{N}
""")

def show_system():
    info = System.info()
    Logger.info(f"OS: {info.get('PRETTY_NAME', 'Unknown')}")
    Logger.info(f"Kernel: {info['kernel']}")
    Logger.info(f"Arch: {info['arch']}")
    Logger.info(f"RAM: {info['ram']}GB")
    Logger.info(f"Space: {System.get_space():.1f}GB free")

def main_menu():
    print(f"\n{C}Main Menu:{N}\n")
    print(f"{G}[1]{N} Kali Linux Tools")
    print(f"{G}[2]{N} Parrot Security OS")
    print(f"{G}[3]{N} Advanced Options")
    print(f"{G}[0]{N} Exit\n")

def kali_menu():
    print(f"\n{C}Kali Categories:{N}\n")
    print(f"{G}[1]{N} Information Gathering")
    print(f"{G}[2]{N} Vulnerability Analysis")
    print(f"{G}[3]{N} Exploitation")
    print(f"{G}[4]{N} Wireless")
    print(f"{G}[5]{N} Web Apps")
    print(f"{G}[6]{N} Passwords")
    print(f"{G}[7]{N} Full Install {Y}(10+ GB){N}")
    print(f"{G}[0]{N} Back\n")

def parrot_menu():
    print(f"\n{C}Parrot Editions:{N}\n")
    print(f"{G}[1]{N} Core")
    print(f"{G}[2]{N} Home")
    print(f"{G}[3]{N} Security")
    print(f"{G}[0]{N} Back\n")

def install_kali(cat, pkg):
    tools = {
        1: ["nmap", "dnsrecon", "theharvester", "recon-ng"],
        2: ["nikto", "sqlmap", "lynis", "openvas"],
        3: ["metasploit-framework", "exploitdb", "set"],
        4: ["aircrack-ng", "reaver", "wifite", "kismet"],
        5: ["burpsuite", "zaproxy", "wfuzz", "dirb"],
        6: ["hydra", "john", "hashcat", "crunch"],
        7: ["kali-linux-large"]
    }
    
    if cat not in tools:
        Logger.err("Invalid category")
        return
    
    pkg.block_rpcbind()
    Repo.add_kali()
    pkg.install_batch(tools[cat])
    Repo.cleanup()

def install_parrot(ed, pkg):
    editions = {
        1: ["parrot-core"],
        2: ["parrot-core", "parrot-interface-home", "parrot-desktop-mate"],
        3: ["parrot-core", "parrot-interface-home", "parrot-desktop-mate", "parrot-tools-full"]
    }
    
    if ed not in editions:
        Logger.err("Invalid edition")
        return
    
    pkg.block_rpcbind()
    Repo.add_parrot()
    pkg.install_batch(editions[ed])
    Repo.cleanup()

def main():
    if not System.is_root():
        Logger.err("Root access required. Run with sudo.")
        sys.exit(1)
    
    if not System.is_debian():
        Logger.err("Debian-based system required")
        sys.exit(1)
    
    banner()
    show_system()
    
    if System.get_space() < 5:
        Logger.warn(f"Low disk space: {System.get_space():.1f}GB")
        ans = input(f"{Y}Continue? (y/n):{N} ").lower()
        if ans != 'y':
            sys.exit(0)
    
    pkg = Package()
    pkg.fix()
    
    while True:
        main_menu()
        choice = input("Choice: ").strip()
        
        if choice == "0":
            Repo.cleanup()
            Logger.ok("Done")
            if pkg.failed:
                Logger.warn(f"Failed: {', '.join(pkg.failed)}")
            break
        elif choice == "1":
            while True:
                kali_menu()
                kcat = input("Choice: ").strip()
                if kcat == "0":
                    break
                try:
                    install_kali(int(kcat), pkg)
                except:
                    Logger.err("Invalid choice")
        elif choice == "2":
            while True:
                parrot_menu()
                ped = input("Choice: ").strip()
                if ped == "0":
                    break
                try:
                    install_parrot(int(ped), pkg)
                except:
                    Logger.err("Invalid choice")
        elif choice == "3":
            Logger.info("Coming soon")
        else:
            Logger.err("Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Y}Interrupted{N}")
        Repo.cleanup()
        sys.exit(130)
    except Exception as e:
        Logger.err(f"Error: {e}")
        sys.exit(1)
