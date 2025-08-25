#!/usr/bin/env python3
"""
Krilin Core - Security Framework v0.2
Author: 0xb0rn3 | 0xbv1
"""

import os
import subprocess
import sys
import platform
import random
import time
import re
import tempfile
import shutil
import json
from pathlib import Path

# Try importing optional dependencies with fallbacks
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("[WARNING] requests module not available. Some features may be limited.")

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    print("[WARNING] BeautifulSoup module not available. Web scraping features disabled.")

# Color and style codes for dramatic vibe
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
BLINK = '\033[5m'
NORMAL = '\033[0m'

# Kali repository URL
KALI_REPO = "deb http://http.kali.org/kali kali-rolling main contrib non-free non-free-firmware"

# Kali tools list URL
KALI_TOOLS_URL = "https://www.kali.org/tools/all-tools/"

# Version info
VERSION = "0.2 Stable"

# Developer info
DEVINFO = "By: 0xbv1(0xb0rn3) Mail: q4n0@proton.me X & DISCORD: oxbv1 IG: theehiv3"

# Categories including tools and kernels
CATEGORIES = {
    "1": ("Information Gathering", ["nmap", "dnsrecon", "theharvester", "recon-ng", "maltego", "shodan", "spiderfoot"], False, "kali"),
    "2": ("Vulnerability Analysis", ["nikto", "sqlmap", "lynis", "openvas", "wapiti", "davtest"], False, "kali"),
    "3": ("Exploitation Tools", ["metasploit-framework", "exploitdb", "set", "beef-xss", "armitage"], False, "kali"),
    "4": ("Wireless Attacks", ["aircrack-ng", "reaver", "wifite", "kismet", "pixiewps", "bully", "cowpatty"], False, "kali"),
    "5": ("Web Application Analysis", ["burpsuite", "zaproxy", "wfuzz", "dirb", "gobuster", "ffuf", "sqlmap"], False, "kali"),
    "6": ("Password Attacks", ["hydra", "john", "hashcat", "crunch", "wordlists", "cewl", "medusa"], False, "kali"),
    "7": ("Individual Kali Tools", [], False, "kali"),  # Will prompt for specific tools
    "8": ("Debian Backports Kernel", ["linux-image-amd64"], True, "backports"),
    "9": ("Kali Linux Kernel", ["linux-image-amd64"], True, "kali"),
    "10": ("All Kali Hacking Tools", [], False, "kali")  # Option for all tools
}

# Dependency check function
def check_python_dependencies():
    """Check and install required Python dependencies."""
    missing_deps = []
    
    if not REQUESTS_AVAILABLE:
        missing_deps.append("requests")
    if not BS4_AVAILABLE:
        missing_deps.append("beautifulsoup4")
    
    if missing_deps:
        print(f"{YELLOW}{BOLD}[!] Missing Python dependencies: {', '.join(missing_deps)}{NORMAL}")
        print(f"{CYAN}[*] Attempting to install missing dependencies...{NORMAL}")
        
        for dep in missing_deps:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", dep], check=True)
                print(f"{GREEN}[+] Successfully installed {dep}{NORMAL}")
            except subprocess.CalledProcessError:
                try:
                    # Try with --break-system-packages flag for newer systems
                    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "--break-system-packages", dep], check=True)
                    print(f"{GREEN}[+] Successfully installed {dep}{NORMAL}")
                except:
                    print(f"{RED}[!] Failed to install {dep}. Some features may not work.{NORMAL}")

def check_system_dependencies():
    """Check for required system utilities."""
    required_tools = {
        "wget": "wget",
        "curl": "curl",
        "git": "git",
        "gpg": "gnupg",
        "lsb_release": "lsb-release"
    }
    
    missing_tools = []
    for tool, package in required_tools.items():
        if not shutil.which(tool):
            missing_tools.append(package)
    
    if missing_tools:
        print(f"{YELLOW}{BOLD}[!] Missing system tools: {', '.join(missing_tools)}{NORMAL}")
        print(f"{CYAN}[*] Installing missing system dependencies...{NORMAL}")
        
        try:
            subprocess.run(["apt-get", "update", "-qq"], check=False)
            subprocess.run(["apt-get", "install", "-y", "-qq"] + missing_tools, check=True)
            print(f"{GREEN}[+] System dependencies installed successfully.{NORMAL}")
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Failed to install system dependencies: {e}{NORMAL}")
            print(f"{YELLOW}[!] You may need to manually install: {' '.join(missing_tools)}{NORMAL}")

def dramatic_print(text, color=GREEN, delay=0.01):
    """Print text with dramatic effect."""
    for char in text:
        print(f"{color}{char}{NORMAL}", end='', flush=True)
        time.sleep(delay)
    print()

def display_banner():
    """Display a dramatic ASCII art banner."""
    banner = f"""
{CYAN}{BOLD}██╗  ██╗{RED}██████╗ {YELLOW}██╗{GREEN}██╗     {BLUE}██╗{MAGENTA}███╗   ██╗{NORMAL}
{CYAN}{BOLD}██║ ██╔╝{RED}██╔══██╗{YELLOW}██║{GREEN}██║     {BLUE}██║{MAGENTA}████╗  ██║{NORMAL}
{CYAN}{BOLD}█████╔╝ {RED}██████╔╝{YELLOW}██║{GREEN}██║     {BLUE}██║{MAGENTA}██╔██╗ ██║{NORMAL}
{CYAN}{BOLD}██╔═██╗ {RED}██╔══██╗{YELLOW}██║{GREEN}██║     {BLUE}██║{MAGENTA}██║╚██╗██║{NORMAL}
{CYAN}{BOLD}██║  ██╗{RED}██║  ██║{YELLOW}██║{GREEN}███████╗{BLUE}██║{MAGENTA}██║ ╚████║{NORMAL}
{CYAN}{BOLD}╚═╝  ╚═╝{RED}╚═╝  ╚═╝{YELLOW}╚═╝{GREEN}╚══════╝{BLUE}╚═╝{MAGENTA}╚═╝  ╚═══╝{NORMAL}
                                                 
{BLUE}{BOLD}╔═════════════════════════════════════════════════╗{NORMAL}
{BLUE}{BOLD}║{GREEN} KRILIN - TOOLS AND KERNEL ARSENAL {DEVINFO} {BLUE}║{NORMAL}
{BLUE}{BOLD}║{GREEN} Pentest Machine Setup v{VERSION}                {BLUE}║{NORMAL}
{BLUE}{BOLD}╚═════════════════════════════════════════════════╝{NORMAL}
"""
    print(banner)

def detect_system():
    """Detect and display system information with enhanced error handling."""
    os_name = platform.system()
    os_release = platform.release()
    os_version = platform.version()
    machine_arch = platform.machine()
    
    # Get kernel info safely
    try:
        kernel_info = subprocess.check_output("uname -r", shell=True, stderr=subprocess.DEVNULL).decode().strip()
    except:
        kernel_info = "Unknown"
    
    # Get CPU info
    cpu_info = "Unknown"
    if os.path.exists("/proc/cpuinfo"):
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        cpu_info = line.split(":")[1].strip()
                        break
        except:
            pass
    
    # Get RAM info
    ram_info = "Unknown"
    if os.path.exists("/proc/meminfo"):
        try:
            with open("/proc/meminfo", "r") as f:
                for line in f:
                    if "MemTotal" in line:
                        ram_kb = int(line.split()[1])
                        ram_gb = round(ram_kb / 1024 / 1024, 1)
                        ram_info = f"{ram_gb} GB"
                        break
        except:
            pass
    
    # Get disk space
    try:
        disk_stat = os.statvfs('/')
        disk_total = (disk_stat.f_blocks * disk_stat.f_frsize) / (1024**3)
        disk_free = (disk_stat.f_bavail * disk_stat.f_frsize) / (1024**3)
        disk_info = f"{disk_free:.1f}GB free of {disk_total:.1f}GB"
    except:
        disk_info = "Unknown"
    
    print(f"\n{BOLD}{BLUE}[*] System Detection Results:{NORMAL}")
    print(f"{BOLD}{GREEN}[+] OS:{NORMAL} {os_name} {os_release}")
    print(f"{BOLD}{GREEN}[+] Architecture:{NORMAL} {machine_arch}")
    print(f"{BOLD}{GREEN}[+] Kernel:{NORMAL} {kernel_info}")
    print(f"{BOLD}{GREEN}[+] CPU:{NORMAL} {cpu_info}")
    print(f"{BOLD}{GREEN}[+] Memory:{NORMAL} {ram_info}")
    print(f"{BOLD}{GREEN}[+] Disk Space:{NORMAL} {disk_info}")
    
    # Check if Debian-based
    is_debian = False
    if os.path.exists("/etc/debian_version"):
        try:
            with open("/etc/debian_version", "r") as f:
                debian_version = f.read().strip()
                print(f"{BOLD}{GREEN}[+] Debian Version:{NORMAL} {debian_version}")
                is_debian = True
        except:
            pass
    
    # Try to get distribution info
    try:
        result = subprocess.run(["lsb_release", "-ds"], capture_output=True, text=True, check=False)
        if result.returncode == 0:
            print(f"{BOLD}{GREEN}[+] Distribution:{NORMAL} {result.stdout.strip()}")
    except:
        pass
    
    if not is_debian:
        print(f"{BOLD}{RED}[!] Warning: This script is designed for Debian-based systems.{NORMAL}")
        answer = input(f"{BOLD}{YELLOW}[?] Continue anyway? (y/n):{NORMAL} ").lower()
        if answer != 'y':
            sys.exit(1)
    
    # Check for required disk space
    if disk_info != "Unknown" and disk_free < 5:
        print(f"{BOLD}{YELLOW}[!] Warning: Low disk space ({disk_free:.1f}GB free).{NORMAL}")
        print(f"{BOLD}{YELLOW}[!] Some installations may require 10+ GB of space.{NORMAL}")

def check_root():
    """Ensure the script runs with root privileges."""
    if os.geteuid() != 0:
        print(f"{RED}{BOLD}[!] This script must be run as root. Use 'sudo'.{NORMAL}")
        sys.exit(1)

def get_debian_codename():
    """Retrieve Debian codename from /etc/os-release with enhanced error handling."""
    try:
        # Try /etc/os-release first
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("VERSION_CODENAME="):
                        codename = line.split("=")[1].strip().strip('"')
                        if codename:
                            return codename
    except Exception as e:
        print(f"{YELLOW}{BOLD}[!] Warning: Could not read /etc/os-release: {e}{NORMAL}")
    
    # Try lsb_release
    try:
        result = subprocess.run(["lsb_release", "-cs"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, check=True)
        codename = result.stdout.strip()
        if codename:
            return codename
    except:
        pass
    
    # Manual fallback
    print(f"{RED}{BOLD}[!] Could not automatically determine Debian codename.{NORMAL}")
    print(f"{YELLOW}Common codenames: bookworm (12), bullseye (11), buster (10){NORMAL}")
    codename = input(f"{BOLD}{YELLOW}[?] Please enter your Debian codename:{NORMAL} ").strip()
    
    if codename:
        return codename
    else:
        print(f"{RED}{BOLD}[!] Codename required for backports. Exiting.{NORMAL}")
        sys.exit(1)

def add_kali_keyring():
    """Download and install the Kali archive keyring package with retry logic."""
    keyring_urls = [
        "https://archive.kali.org/kali/pool/main/k/kali-archive-keyring/kali-archive-keyring_2025.1_all.deb",
        "https://archive.kali.org/kali/pool/main/k/kali-archive-keyring/kali-archive-keyring_2024.3_all.deb",
        "https://http.kali.org/kali/pool/main/k/kali-archive-keyring/kali-archive-keyring_2022.1_all.deb"
    ]
    
    keyring_file = "/tmp/kali-archive-keyring.deb"
    
    print(f"{CYAN}{BOLD}[*] Downloading and installing Kali archive keyring...{NORMAL}")
    
    for url in keyring_urls:
        try:
            # Try wget first
            if shutil.which("wget"):
                subprocess.run(["wget", "-q", "-O", keyring_file, url], check=True, timeout=30)
            elif shutil.which("curl"):
                subprocess.run(["curl", "-s", "-L", "-o", keyring_file, url], check=True, timeout=30)
            elif REQUESTS_AVAILABLE:
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    with open(keyring_file, "wb") as f:
                        f.write(response.content)
                else:
                    continue
            else:
                print(f"{RED}{BOLD}[!] No download tool available (wget/curl/requests){NORMAL}")
                return False
            
            # Install the keyring
            subprocess.run(["dpkg", "-i", keyring_file], check=True)
            
            # Clean up
            if os.path.exists(keyring_file):
                os.remove(keyring_file)
            
            print(f"{GREEN}{BOLD}[+] Kali archive keyring installed successfully.{NORMAL}")
            return True
            
        except Exception as e:
            continue
    
    print(f"{RED}{BOLD}[!] Failed to install Kali keyring from all sources.{NORMAL}")
    print(f"{YELLOW}[!] Continuing without official Kali keyring. This may cause trust issues.{NORMAL}")
    return False

def add_repo(repo_type):
    """Add a temporary repository based on type."""
    print(f"{CYAN}{BOLD}[*] Adding {repo_type} repository...{NORMAL}")
    
    if repo_type == "kali":
        # Add Kali keyring
        add_kali_keyring()
        
        # Create repository file
        repo_file = "/etc/apt/sources.list.d/kali-temp.list"
        try:
            with open(repo_file, "w") as f:
                f.write(f"{KALI_REPO}\n")
            print(f"{GREEN}[+] Kali repository added to {repo_file}{NORMAL}")
        except Exception as e:
            print(f"{RED}[!] Failed to add Kali repository: {e}{NORMAL}")
            return False
            
    elif repo_type == "backports":
        codename = get_debian_codename()
        repo_file = "/etc/apt/sources.list.d/backports-temp.list"
        try:
            with open(repo_file, "w") as f:
                f.write(f"deb http://deb.debian.org/debian {codename}-backports main contrib non-free non-free-firmware\n")
            print(f"{GREEN}[+] Backports repository added to {repo_file}{NORMAL}")
        except Exception as e:
            print(f"{RED}[!] Failed to add backports repository: {e}{NORMAL}")
            return False
    
    # Update package lists
    print(f"{CYAN}{BOLD}[*] Updating package lists...{NORMAL}")
    try:
        subprocess.run(["apt-get", "update"], check=True, timeout=120)
        print(f"{GREEN}{BOLD}[+] Repository added and package list updated.{NORMAL}")
        return True
    except subprocess.CalledProcessError:
        print(f"{RED}{BOLD}[!] Failed to update package lists. Continuing anyway...{NORMAL}")
        return False
    except subprocess.TimeoutExpired:
        print(f"{RED}{BOLD}[!] Update timed out. Continuing anyway...{NORMAL}")
        return False

def proactively_remove_rpcbind():
    """Proactively remove rpcbind before any installations to prevent issues."""
    print(f"{CYAN}{BOLD}[*] Proactively handling rpcbind package to prevent installation issues...{NORMAL}")
    
    if check_for_rpcbind():
        print(f"{YELLOW}{BOLD}[!] rpcbind detected - removing to prevent installation issues...{NORMAL}")
        
        # Stop services
        services = ["rpcbind", "rpcbind.socket", "rpcbind.target"]
        for service in services:
            try:
                subprocess.run(["systemctl", "stop", service], check=False, stderr=subprocess.DEVNULL)
                subprocess.run(["systemctl", "disable", service], check=False, stderr=subprocess.DEVNULL)
            except:
                pass
        
        # Remove package
        try:
            subprocess.run(["apt-get", "remove", "--purge", "-y", "rpcbind"], check=False, stderr=subprocess.DEVNULL)
            print(f"{GREEN}{BOLD}[+] rpcbind removed.{NORMAL}")
        except:
            pass
    
    create_rpcbind_diversion()

def create_rpcbind_diversion():
    """Create a diversion for rpcbind to prevent its installation."""
    try:
        # Create dummy directory
        dummy_dir = "/tmp/dummy-rpcbind"
        os.makedirs(dummy_dir, exist_ok=True)
        
        # Create dummy postinst script
        postinst_path = os.path.join(dummy_dir, "postinst")
        with open(postinst_path, "w") as f:
            f.write("#!/bin/sh\nexit 0\n")
        os.chmod(postinst_path, 0o755)
        
        # Create dummy rpcbind binary
        os.makedirs(os.path.join(dummy_dir, "usr", "sbin"), exist_ok=True)
        rpcbind_path = os.path.join(dummy_dir, "usr", "sbin", "rpcbind")
        with open(rpcbind_path, "w") as f:
            f.write("#!/bin/sh\necho 'Dummy rpcbind - not functional'\nexit 0\n")
        os.chmod(rpcbind_path, 0o755)
        
        # Create diversions
        subprocess.run(["dpkg-divert", "--local", "--rename", "--add", "/usr/sbin/rpcbind"], 
                      check=False, stderr=subprocess.DEVNULL)
        
        # Copy dummy files if originals don't exist
        if not os.path.exists("/usr/sbin/rpcbind"):
            shutil.copy2(rpcbind_path, "/usr/sbin/rpcbind")
        
        print(f"{GREEN}{BOLD}[+] Created diversions to prevent rpcbind issues.{NORMAL}")
        
        # Clean up
        shutil.rmtree(dummy_dir, ignore_errors=True)
        
    except Exception as e:
        print(f"{YELLOW}{BOLD}[!] Warning when creating diversions: {e}{NORMAL}")

def check_for_rpcbind():
    """Check if rpcbind is installed."""
    try:
        result = subprocess.run(
            ["dpkg-query", "-W", "-f='${Status}'", "rpcbind"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            universal_newlines=True,
            check=False
        )
        return "install ok installed" in result.stdout
    except:
        return False

def fix_dpkg_issues_thoroughly():
    """Fix package management issues thoroughly."""
    print(f"{CYAN}{BOLD}[*] Fixing package management issues...{NORMAL}")
    
    try:
        # Remove lock files
        lock_files = [
            "/var/lib/apt/lists/lock",
            "/var/cache/apt/archives/lock", 
            "/var/lib/dpkg/lock",
            "/var/lib/dpkg/lock-frontend"
        ]
        
        for lock_file in lock_files:
            if os.path.exists(lock_file):
                print(f"{YELLOW}[!] Removing lock file: {lock_file}{NORMAL}")
                try:
                    os.remove(lock_file)
                except:
                    pass
        
        # Kill any apt/dpkg processes
        try:
            subprocess.run(["killall", "-9", "apt-get"], check=False, stderr=subprocess.DEVNULL)
            subprocess.run(["killall", "-9", "dpkg"], check=False, stderr=subprocess.DEVNULL)
        except:
            pass
        
        # Configure packages
        print(f"{CYAN}[*] Configuring unpacked packages...{NORMAL}")
        subprocess.run(["dpkg", "--configure", "-a"], check=False, stderr=subprocess.DEVNULL)
        
        # Fix broken dependencies
        print(f"{CYAN}[*] Fixing broken dependencies...{NORMAL}")
        subprocess.run(["apt-get", "install", "-f", "-y"], check=False, stderr=subprocess.DEVNULL)
        
        # Clean package cache
        print(f"{CYAN}[*] Cleaning package cache...{NORMAL}")
        subprocess.run(["apt-get", "clean"], check=False)
        subprocess.run(["apt-get", "autoclean"], check=False)
        
        # Update with fix-missing
        print(f"{CYAN}[*] Updating package lists with fix-missing...{NORMAL}")
        subprocess.run(["apt-get", "update", "--fix-missing"], check=False)
        
        # Remove unnecessary packages
        print(f"{CYAN}[*] Removing unnecessary packages...{NORMAL}")
        subprocess.run(["apt-get", "autoremove", "-y"], check=False, stderr=subprocess.DEVNULL)
        
        print(f"{GREEN}{BOLD}[+] Package management issues fixed.{NORMAL}")
        
    except Exception as e:
        print(f"{RED}{BOLD}[!] Error during package fixing: {e}{NORMAL}")

def create_apt_preferences():
    """Create proper APT preferences to prevent rpcbind installation."""
    prefs_dir = "/etc/apt/preferences.d"
    os.makedirs(prefs_dir, exist_ok=True)
    
    prefs_file = os.path.join(prefs_dir, "block-rpcbind")
    try:
        with open(prefs_file, "w") as f:
            f.write("Package: rpcbind\n")
            f.write("Pin: release *\n")
            f.write("Pin-Priority: -1\n\n")
            f.write("Package: nfs-common\n")
            f.write("Pin: release *\n")
            f.write("Pin-Priority: -1\n")
        
        print(f"{GREEN}{BOLD}[+] Created APT preferences to block problematic packages.{NORMAL}")
    except Exception as e:
        print(f"{YELLOW}[!] Could not create APT preferences: {e}{NORMAL}")

def remove_repo(repo_type):
    """Remove the temporary repository."""
    print(f"{CYAN}{BOLD}[*] Cleaning up {repo_type} repository...{NORMAL}")
    
    # Fix any issues first
    fix_dpkg_issues_thoroughly()
    
    # Remove repository files
    if repo_type == "kali":
        repo_file = "/etc/apt/sources.list.d/kali-temp.list"
    elif repo_type == "backports":
        repo_file = "/etc/apt/sources.list.d/backports-temp.list"
    else:
        return
    
    if os.path.exists(repo_file):
        try:
            os.remove(repo_file)
            print(f"{GREEN}[+] Removed {repo_file}{NORMAL}")
        except Exception as e:
            print(f"{YELLOW}[!] Could not remove {repo_file}: {e}{NORMAL}")
    
    # Update package lists
    try:
        subprocess.run(["apt-get", "update"], check=True, timeout=60)
        print(f"{GREEN}{BOLD}[+] Repository removed and package list updated.{NORMAL}")
    except:
        print(f"{YELLOW}{BOLD}[!] Warning: Cleanup incomplete. You may need to manually fix your repositories.{NORMAL}")

def select_specific_tools():
    """Allow the user to select specific Kali tools."""
    print(f"{CYAN}{BOLD}[*] Enter the names of Kali tools you want to install (separated by spaces):{NORMAL}")
    print(f"{YELLOW}{BOLD}[!] Example: nmap dirb nikto sqlmap metasploit-framework{NORMAL}")
    print(f"{GREEN}[*] Popular tools: {NORMAL}")
    print(f"    - Network: nmap, masscan, zmap, netcat")
    print(f"    - Web: burpsuite, zaproxy, dirb, gobuster, ffuf")
    print(f"    - Exploitation: metasploit-framework, exploitdb, searchsploit")
    print(f"    - Password: hydra, john, hashcat, medusa")
    print(f"    - Wireless: aircrack-ng, wifite, reaver, bully")
    
    tools_input = input(f"{BOLD}{GREEN}[?] Tools to install:{NORMAL} ")
    
    if tools_input.strip():
        return tools_input.strip().split()
    else:
        print(f"{RED}{BOLD}[!] No tools specified. Returning to menu.{NORMAL}")
        return []

def fetch_all_kali_tools():
    """Fetch all available Kali tools from the website or fallback methods."""
    print(f"{CYAN}{BOLD}[*] Fetching list of all Kali tools...{NORMAL}")
    
    # Predefined comprehensive tool list as fallback
    fallback_tools = [
        # Information Gathering
        "nmap", "masscan", "zmap", "dnsrecon", "dnsenum", "fierce", "theharvester",
        "maltego", "recon-ng", "shodan", "spiderfoot", "amass", "subfinder",
        
        # Vulnerability Analysis  
        "nikto", "sqlmap", "wpscan", "lynis", "openvas", "wapiti", "davtest",
        "skipfish", "arachni", "vega", "w3af",
        
        # Exploitation
        "metasploit-framework", "exploitdb", "searchsploit", "set", "beef-xss",
        "armitage", "crackmapexec", "empire", "powersploit", "mimikatz",
        
        # Wireless
        "aircrack-ng", "wifite", "reaver", "bully", "pixiewps", "kismet",
        "cowpatty", "fern-wifi-cracker", "wifi-honey", "mdk3", "mdk4",
        
        # Web Applications
        "burpsuite", "zaproxy", "dirb", "dirbuster", "gobuster", "ffuf",
        "wfuzz", "sqlmap", "xsser", "cadaver", "commix",
        
        # Password Attacks
        "hydra", "john", "hashcat", "medusa", "ncrack", "ophcrack",
        "crunch", "cewl", "rsmangler", "wordlists", "seclists",
        
        # Sniffing & Spoofing
        "wireshark", "tcpdump", "ettercap-text-only", "responder", "mitmproxy",
        "bettercap", "dsniff", "netsniff-ng", "scapy",
        
        # Post Exploitation
        "powershell-empire", "post-exploitation", "laudanum", "weevely",
        "dbd", "sbd", "u3-pwn", "gsocket",
        
        # Forensics
        "autopsy", "binwalk", "bulk-extractor", "foremost", "volatility",
        "sleuthkit", "ddrescue", "dc3dd", "dcfldd",
        
        # Reporting
        "dradis", "faraday", "magictree", "metagoofil", "pipal",
        
        # Social Engineering
        "social-engineer-toolkit", "ghost-phisher", "fluxion",
        
        # Reverse Engineering
        "gdb", "radare2", "ollydbg", "apktool", "dex2jar", "jd-gui",
        
        # Stress Testing
        "slowhttptest", "goldeneye", "hping3", "siege", "thc-ssl-dos",
        
        # VoIP
        "sipvicious", "voiphopper", "sipp", "rtpflood",
        
        # Database
        "sqlninja", "sqlsus", "oscanner", "tnscmd10g", "sidguesser"
    ]
    
    # Try to fetch from website if available
    if REQUESTS_AVAILABLE and BS4_AVAILABLE:
        try:
            response = requests.get(KALI_TOOLS_URL, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                tool_packages = []
                
                # Try to parse the tools page
                tools_sections = soup.find_all(['a', 'td', 'li'])
                for element in tools_sections:
                    text = element.get_text().strip()
                    # Look for package-like names
                    if re.match(r'^[a-z0-9][a-z0-9\-\.]+$', text) and len(text) > 2:
                
                if tool_packages:
                    # Combine with fallback list
                    all_tools = list(set(tool_packages + fallback_tools))
                    print(f"{GREEN}{BOLD}[+] Found {len(all_tools)} Kali tools.{NORMAL}")
                    return all_tools
        except Exception as e:
            print(f"{YELLOW}[!] Could not fetch from website: {e}{NORMAL}")
    
    # Try apt-cache method
    try:
        add_repo("kali")
        result = subprocess.run(["apt-cache", "search", "kali-"], 
                              stdout=subprocess.PIPE, text=True, check=False)
        
        if result.stdout:
            apt_tools = []
            for line in result.stdout.split("\n"):
                if line.strip():
                    package_name = line.split(" - ")[0].strip()
                    if package_name:
                        apt_tools.append(package_name)
            
            if apt_tools:
                all_tools = list(set(apt_tools + fallback_tools))
                print(f"{GREEN}{BOLD}[+] Found {len(all_tools)} tools from repository.{NORMAL}")
                return all_tools
    except:
        pass
    
    # Return fallback list
    print(f"{YELLOW}[!] Using predefined tool list.{NORMAL}")
    print(f"{GREEN}{BOLD}[+] {len(fallback_tools)} tools available.{NORMAL}")
    return fallback_tools

def install_all_kali_tools():
    """Install all available Kali tools with a strict warning."""
    print(f"{MAGENTA}{BOLD}[*] Preparing to install all Kali hacking tools...{NORMAL}")
    
    tool_packages = fetch_all_kali_tools()
    
    if not tool_packages:
        print(f"{RED}{BOLD}[!] Could not retrieve the list of Kali tools. Aborting.{NORMAL}")
        return
    
    print(f"{CYAN}{BOLD}[*] Found {len(tool_packages)} tools to install.{NORMAL}")
    
    # Display warning
    print(f"\n{RED}{BLINK}{BOLD}{'='*60}{NORMAL}")
    print(f"{RED}{BOLD}              ⚠️  CRITICAL WARNING ⚠️{NORMAL}")
    print(f"{RED}{BOLD}{'='*60}{NORMAL}")
    print(f"{RED}{BOLD}Installing ALL Kali tools will:{NORMAL}")
    print(f"{YELLOW}  • Download and install 10+ GB of software{NORMAL}")
    print(f"{YELLOW}  • Take several hours to complete{NORMAL}")
    print(f"{YELLOW}  • May cause system instability{NORMAL}")
    print(f"{YELLOW}  • Could create software conflicts{NORMAL}")
    print(f"{YELLOW}  • Consume significant system resources{NORMAL}")
    print(f"{RED}{BOLD}{'='*60}{NORMAL}")
    print(f"{RED}{BOLD}STRONGLY RECOMMENDED:{NORMAL} Use option 7 to install")
    print(f"individual packages instead of everything at once.")
    print(f"{RED}{BOLD}{'='*60}{NORMAL}\n")
    
    confirmation = input(f"{BOLD}{RED}[?] Type 'I UNDERSTAND THE RISKS' to proceed or 'n' to cancel:{NORMAL} ").strip()
    if confirmation != "I UNDERSTAND THE RISKS":
        print(f"{YELLOW}{BOLD}[!] Installation cancelled. Good choice!{NORMAL}")
        print(f"{GREEN}[*] Consider using option 7 to install specific tools.{NORMAL}")
        return
    
    # Ask about batch installation
    batch_option = input(f"{BOLD}{YELLOW}[?] Install in batches (recommended) or all at once? (b/a):{NORMAL} ").lower()
    
    try:
        # Prepare system
        proactively_remove_rpcbind()
        create_apt_preferences()
        add_repo("kali")
        fix_dpkg_issues_thoroughly()
        
        # Separate metapackages and individual tools
        metapackages = [pkg for pkg in tool_packages if pkg.startswith("kali-")]
        individual_tools = [pkg for pkg in tool_packages if not pkg.startswith("kali-")]
        
        failed_packages = []
        installed_count = 0
        
        # Install metapackages first
        if metapackages:
            print(f"\n{CYAN}{BOLD}[*] Installing Kali metapackages...{NORMAL}")
            for meta in metapackages[:5]:  # Limit metapackages to avoid conflicts
                if install_with_retries(meta, repo_type="kali"):
                    installed_count += 1
                else:
                    failed_packages.append(meta)
        
        # Install individual tools
        if batch_option == 'b':
            batch_size = 10
            total_batches = (len(individual_tools) + batch_size - 1) // batch_size
            
            for i in range(0, len(individual_tools), batch_size):
                batch = individual_tools[i:i+batch_size]
                batch_num = i // batch_size + 1
                
                print(f"\n{CYAN}{BOLD}[*] Installing batch {batch_num}/{total_batches}:{NORMAL}")
                print(f"    {', '.join(batch)}")
                
                for package in batch:
                    if install_with_retries(package, repo_type="kali"):
                        installed_count += 1
                    else:
                        failed_packages.append(package)
                
                # Progress update
                progress = (i + len(batch)) * 100 // len(individual_tools)
                print(f"{GREEN}[*] Progress: {progress}% complete ({installed_count} tools installed){NORMAL}")
        else:
            # Install all at once (not recommended)
            print(f"\n{CYAN}{BOLD}[*] Installing all tools (this will take a long time)...{NORMAL}")
            for idx, package in enumerate(individual_tools):
                print(f"{CYAN}[*] Installing {package} ({idx+1}/{len(individual_tools)})...{NORMAL}")
                if install_with_retries(package, repo_type="kali"):
                    installed_count += 1
                else:
                    failed_packages.append(package)
        
        # Report results
        print(f"\n{BOLD}{BLUE}{'='*60}{NORMAL}")
        print(f"{BOLD}{GREEN}Installation Summary:{NORMAL}")
        print(f"  • Tools installed successfully: {installed_count}")
        print(f"  • Tools failed: {len(failed_packages)}")
        
        if failed_packages:
            print(f"\n{YELLOW}{BOLD}[!] The following packages failed to install:{NORMAL}")
            for pkg in failed_packages[:20]:  # Show first 20 failures
                print(f"    - {pkg}")
            if len(failed_packages) > 20:
                print(f"    ... and {len(failed_packages) - 20} more")
            
            # Save failed packages to file
            with open("/tmp/krilin_failed_packages.txt", "w") as f:
                f.write("\n".join(failed_packages))
            print(f"{YELLOW}[*] Complete list saved to /tmp/krilin_failed_packages.txt{NORMAL}")
        else:
            print(f"{GREEN}{BOLD}[+] All packages successfully installed!{NORMAL}")
            print(f"{GREEN}[+] Your complete Kali arsenal is ready.{NORMAL}")
    
    except KeyboardInterrupt:
        print(f"\n{YELLOW}{BOLD}[!] Installation interrupted by user.{NORMAL}")
    except Exception as e:
        print(f"{RED}{BOLD}[!] Unexpected error: {e}{NORMAL}")
    finally:
        fix_dpkg_issues_thoroughly()
        remove_repo("kali")

def install_with_retries(package, repo_type=None, max_retries=3, timeout=300):
    """Install a package with retries on failure."""
    for attempt in range(1, max_retries + 1):
        try:
            # Skip if already installed
            check_cmd = ["dpkg", "-l", package]
            result = subprocess.run(check_cmd, capture_output=True, text=True, check=False)
            if "ii  " + package in result.stdout:
                print(f"{GREEN}[+] {package} is already installed{NORMAL}")
                return True
            
            print(f"{CYAN}[*] Installing {package} (attempt {attempt}/{max_retries})...{NORMAL}")
            
            # Build install command
            if repo_type == "backports":
                codename = get_debian_codename()
                cmd = ['apt-get', 'install', '-y', '-qq', '-t', f"{codename}-backports", package]
            else:
                cmd = ['apt-get', 'install', '-y', '-qq', '--no-install-recommends', package]
            
            # Try installation
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            
            if result.returncode == 0:
                print(f"{GREEN}[+] Successfully installed {package}{NORMAL}")
                return True
            else:
                raise subprocess.CalledProcessError(result.returncode, cmd)
                
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
            print(f"{YELLOW}[!] Attempt {attempt} failed for {package}{NORMAL}")
            
            if attempt < max_retries:
                # Try to fix issues before next attempt
                fix_dpkg_issues_thoroughly()
                time.sleep(2)
            else:
                # Last attempt - try force install
                print(f"{YELLOW}[!] Trying force install for {package}...{NORMAL}")
                try:
                    # Download package
                    subprocess.run(["apt-get", "download", package], check=False, timeout=60)
                    
                    # Find downloaded .deb file
                    deb_files = [f for f in os.listdir(".") if f.startswith(package) and f.endswith(".deb")]
                    if deb_files:
                        # Force install
                        subprocess.run(["dpkg", "--force-all", "-i", deb_files[0]], check=False)
                        # Fix dependencies
                        subprocess.run(["apt-get", "install", "-f", "-y"], check=False)
                        
                        # Clean up
                        for deb_file in deb_files:
                            os.remove(deb_file)
                        
                        print(f"{GREEN}[+] Force installed {package}{NORMAL}")
                        return True
                except:
                    pass
    
    print(f"{RED}[!] Failed to install {package} after {max_retries} attempts.{NORMAL}")
    return False

def install_tools_or_kernel(category, packages, is_kernel, repo_type):
    """Install selected tools or kernel with dramatic flair."""
    weapons = ["arsenal", "weaponry", "armaments", "firepower", "ordnance", "toolkit"]
    power_words = ["Unleashing", "Deploying", "Activating", "Arming", "Initializing", "Loading"]
    
    chosen_weapon = random.choice(weapons)
    power_word = random.choice(power_words)
    
    # Handle special cases
    if category == "All Kali Hacking Tools":
        install_all_kali_tools()
        return
    elif category == "Individual Kali Tools" and not packages:
        packages = select_specific_tools()
        if not packages:
            return
    
    # Dramatic intro
    dramatic_print(f"\n{BOLD}{RED}[*] {power_word} {category} {chosen_weapon}...{NORMAL}", RED, 0.02)
    
    try:
        # Prepare system
        proactively_remove_rpcbind()
        create_apt_preferences()
        
        # Add repository
        if not add_repo(repo_type):
            print(f"{RED}[!] Failed to add {repo_type} repository.{NORMAL}")
            return
        
        # Fix any existing issues
        fix_dpkg_issues_thoroughly()
        
        # Install packages
        print(f"{CYAN}{BOLD}[*] Installing packages: {', '.join(packages)}{NORMAL}")
        
        failed_packages = []
        successful_packages = []
        
        for package in packages:
            if install_with_retries(package, repo_type=repo_type):
                successful_packages.append(package)
            else:
                failed_packages.append(package)
        
        # Report results
        print(f"\n{BOLD}{BLUE}{'='*50}{NORMAL}")
        if successful_packages:
            print(f"{GREEN}{BOLD}[+] Successfully installed:{NORMAL}")
            for pkg in successful_packages:
                print(f"    ✓ {pkg}")
        
        if failed_packages:
            print(f"{YELLOW}{BOLD}[!] Failed to install:{NORMAL}")
            for pkg in failed_packages:
                print(f"    ✗ {pkg}")
        else:
            print(f"{GREEN}{BOLD}[+] All packages installed successfully!{NORMAL}")
            print(f"{GREEN}[+] Your {category.lower()} is ready for action.{NORMAL}")
        
        if is_kernel:
            print(f"\n{YELLOW}{BOLD}[!] IMPORTANT: Please reboot to activate the new kernel.{NORMAL}")
            print(f"{CYAN}[*] Run: sudo reboot{NORMAL}")
    
    except KeyboardInterrupt:
        print(f"\n{YELLOW}{BOLD}[!] Installation interrupted by user.{NORMAL}")
    except Exception as e:
        print(f"{RED}{BOLD}[!] Unexpected error: {e}{NORMAL}")
    finally:
        # Clean up
        fix_dpkg_issues_thoroughly()
        remove_repo(repo_type)

def display_menu():
    """Display the menu with dramatic styling."""
    print(f"\n{BOLD}{BLUE}╔{'═'*55}╗{NORMAL}")
    print(f"{BOLD}{BLUE}║{YELLOW}     KRILIN - SECURITY TOOLS & KERNEL ARSENAL{BLUE}        ║{NORMAL}")
    print(f"{BOLD}{BLUE}╠{'═'*55}╣{NORMAL}")
    
    for key, (category, tools, is_kernel, _) in CATEGORIES.items():
        # Format category name
        if is_kernel:
            icon = "🔧"
            color = RED if key == "9" else YELLOW
        elif key == "10":
            icon = "⚠️"
            color = MAGENTA
        else:
            icon = "📦"
            color = CYAN
        
        # Special warnings
        if key == "9":
            warning = f" {RED}(May affect stability){NORMAL}"
        elif key == "10":
            warning = f" {MAGENTA}(10+ GB download){NORMAL}"
        else:
            warning = ""
        
        print(f"{BOLD}{BLUE}║{NORMAL} {BOLD}{color}[{key:2}] {icon} {category:<30}{warning}{BLUE}║{NORMAL}")
    
    print(f"{BOLD}{BLUE}║{NORMAL} {BOLD}{YELLOW}[0 ] ❌ Exit{' '*40}{BLUE}║{NORMAL}")
    print(f"{BOLD}{BLUE}╚{'═'*55}╝{NORMAL}")
    
    if os.path.exists("/tmp/krilin_failed_packages.txt"):
        print(f"\n{YELLOW}[!] Previous failed installations detected.{NORMAL}")
        print(f"    View with: cat /tmp/krilin_failed_packages.txt")

def check_disk_space():
    """Check available disk space before installation."""
    try:
        stat = os.statvfs('/')
        free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
        
        if free_gb < 5:
            print(f"{RED}{BOLD}[!] WARNING: Only {free_gb:.1f}GB free disk space available.{NORMAL}")
            print(f"{RED}[!] At least 5GB recommended for tool installation.{NORMAL}")
            answer = input(f"{YELLOW}[?] Continue anyway? (y/n):{NORMAL} ").lower()
            if answer != 'y':
                return False
    except:
        pass
    return True

def main():
    """Main function to run the Krilin tool."""
    # Initial checks
    check_root()
    
    # Check and install dependencies
    check_system_dependencies()
    check_python_dependencies()
    
    # Re-import if they were just installed
    global REQUESTS_AVAILABLE, BS4_AVAILABLE
    try:
        import requests
        REQUESTS_AVAILABLE = True
    except:
        pass
    try:
        from bs4 import BeautifulSoup
        BS4_AVAILABLE = True
    except:
        pass
    
    # Display banner and system info
    display_banner()
    detect_system()
    
    # Check disk space
    if not check_disk_space():
        print(f"{YELLOW}[!] Exiting due to insufficient disk space.{NORMAL}")
        sys.exit(1)
    
    # Fix any initial issues
    fix_dpkg_issues_thoroughly()
    
    # Proactive rpcbind handling
    proactively_remove_rpcbind()
    create_apt_preferences()
    
    # Main menu loop
    while True:
        display_menu()
        
        try:
            choice = input(f"\n{BOLD}{GREEN}[?] Select an option (0-{len(CATEGORIES)}):{NORMAL} ").strip()
            
            if choice == "0":
                dramatic_print(f"{BOLD}{BLUE}[*] Exiting Krilin. Stay safe, stay ethical!{NORMAL}", BLUE, 0.02)
                print(f"{GREEN}[*] Thank you for using Krilin Security Framework.{NORMAL}")
                break
            elif choice in CATEGORIES:
                category, packages, is_kernel, repo_type = CATEGORIES[choice]
                install_tools_or_kernel(category, packages, is_kernel, repo_type)
            else:
                print(f"{RED}{BOLD}[!] Invalid option. Please select 0-{len(CATEGORIES)}.{NORMAL}")
        
        except KeyboardInterrupt:
            print(f"\n{YELLOW}{BOLD}[!] Interrupted. Returning to menu...{NORMAL}")
            continue
        except EOFError:
            print(f"\n{YELLOW}{BOLD}[!] Input terminated. Exiting...{NORMAL}")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}{BOLD}[!] Operation cancelled by user.{NORMAL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}{BOLD}[!] Fatal error: {e}{NORMAL}")
        print(f"{YELLOW}[*] Please report this issue at: https://github.com/0xb0rn3/krilin/issues{NORMAL}")
        sys.exit(1), text) and len(text) > 2:
                        tool_packages.append(text)
                
                if tool_packages:
                    # Combine with fallback list
                    all_tools = list(set(tool_packages + fallback_tools))
                    print(f"{GREEN}{BOLD}[+] Found {len(all_tools)} Kali tools.{NORMAL}")
                    return all_tools
        except Exception as e:
            print(f"{YELLOW}[!] Could not fetch from website: {e}{NORMAL}")
    
    # Try apt-cache method
    try:
        add_repo("kali")
        result = subprocess.run(["apt-cache", "search", "kali-"], 
                              stdout=subprocess.PIPE, text=True, check=False)
        
        if result.stdout:
            apt_tools = []
            for line in result.stdout.split("\n"):
                if line.strip():
                    package_name = line.split(" - ")[0].strip()
                    if package_name:
                        apt_tools.append(package_name)
            
            if apt_tools:
                all_tools = list(set(apt_tools + fallback_tools))
                print(f"{GREEN}{BOLD}[+] Found {len(all_tools)} tools from repository.{NORMAL}")
                return all_tools
    except:
        pass
    
    # Return fallback list
    print(f"{YELLOW}[!] Using predefined tool list.{NORMAL}")
    print(f"{GREEN}{BOLD}[+] {len(fallback_tools)} tools available.{NORMAL}")
    return fallback_tools

def install_all_kali_tools():
    """Install all available Kali tools with a strict warning."""
    print(f"{MAGENTA}{BOLD}[*] Preparing to install all Kali hacking tools...{NORMAL}")
    
    tool_packages = fetch_all_kali_tools()
    
    if not tool_packages:
        print(f"{RED}{BOLD}[!] Could not retrieve the list of Kali tools. Aborting.{NORMAL}")
        return
    
    print(f"{CYAN}{BOLD}[*] Found {len(tool_packages)} tools to install.{NORMAL}")
    
    # Display warning
    print(f"\n{RED}{BLINK}{BOLD}{'='*60}{NORMAL}")
    print(f"{RED}{BOLD}              ⚠️  CRITICAL WARNING ⚠️{NORMAL}")
    print(f"{RED}{BOLD}{'='*60}{NORMAL}")
    print(f"{RED}{BOLD}Installing ALL Kali tools will:{NORMAL}")
    print(f"{YELLOW}  • Download and install 10+ GB of software{NORMAL}")
    print(f"{YELLOW}  • Take several hours to complete{NORMAL}")
    print(f"{YELLOW}  • May cause system instability{NORMAL}")
    print(f"{YELLOW}  • Could create software conflicts{NORMAL}")
    print(f"{YELLOW}  • Consume significant system resources{NORMAL}")
    print(f"{RED}{BOLD}{'='*60}{NORMAL}")
    print(f"{RED}{BOLD}STRONGLY RECOMMENDED:{NORMAL} Use option 7 to install")
    print(f"individual packages instead of everything at once.")
    print(f"{RED}{BOLD}{'='*60}{NORMAL}\n")
    
    confirmation = input(f"{BOLD}{RED}[?] Type 'I UNDERSTAND THE RISKS' to proceed or 'n' to cancel:{NORMAL} ").strip()
    if confirmation != "I UNDERSTAND THE RISKS":
        print(f"{YELLOW}{BOLD}[!] Installation cancelled. Good choice!{NORMAL}")
        print(f"{GREEN}[*] Consider using option 7 to install specific tools.{NORMAL}")
        return
    
    # Ask about batch installation
    batch_option = input(f"{BOLD}{YELLOW}[?] Install in batches (recommended) or all at once? (b/a):{NORMAL} ").lower()
    
    try:
        # Prepare system
        proactively_remove_rpcbind()
        create_apt_preferences()
        add_repo("kali")
        fix_dpkg_issues_thoroughly()
        
        # Separate metapackages and individual tools
        metapackages = [pkg for pkg in tool_packages if pkg.startswith("kali-")]
        individual_tools = [pkg for pkg in tool_packages if not pkg.startswith("kali-")]
        
        failed_packages = []
        installed_count = 0
        
        # Install metapackages first
        if metapackages:
            print(f"\n{CYAN}{BOLD}[*] Installing Kali metapackages...{NORMAL}")
            for meta in metapackages[:5]:  # Limit metapackages to avoid conflicts
                if install_with_retries(meta, repo_type="kali"):
                    installed_count += 1
                else:
                    failed_packages.append(meta)
        
        # Install individual tools
        if batch_option == 'b':
            batch_size = 10
            total_batches = (len(individual_tools) + batch_size - 1) // batch_size
            
            for i in range(0, len(individual_tools), batch_size):
                batch = individual_tools[i:i+batch_size]
                batch_num = i // batch_size + 1
                
                print(f"\n{CYAN}{BOLD}[*] Installing batch {batch_num}/{total_batches}:{NORMAL}")
                print(f"    {', '.join(batch)}")
                
                for package in batch:
                    if install_with_retries(package, repo_type="kali"):
                        installed_count += 1
                    else:
                        failed_packages.append(package)
                
                # Progress update
                progress = (i + len(batch)) * 100 // len(individual_tools)
                print(f"{GREEN}[*] Progress: {progress}% complete ({installed_count} tools installed){NORMAL}")
        else:
            # Install all at once (not recommended)
            print(f"\n{CYAN}{BOLD}[*] Installing all tools (this will take a long time)...{NORMAL}")
            for idx, package in enumerate(individual_tools):
                print(f"{CYAN}[*] Installing {package} ({idx+1}/{len(individual_tools)})...{NORMAL}")
                if install_with_retries(package, repo_type="kali"):
                    installed_count += 1
                else:
                    failed_packages.append(package)
        
        # Report results
        print(f"\n{BOLD}{BLUE}{'='*60}{NORMAL}")
        print(f"{BOLD}{GREEN}Installation Summary:{NORMAL}")
        print(f"  • Tools installed successfully: {installed_count}")
        print(f"  • Tools failed: {len(failed_packages)}")
        
        if failed_packages:
            print(f"\n{YELLOW}{BOLD}[!] The following packages failed to install:{NORMAL}")
            for pkg in failed_packages[:20]:  # Show first 20 failures
                print(f"    - {pkg}")
            if len(failed_packages) > 20:
                print(f"    ... and {len(failed_packages) - 20} more")
            
            # Save failed packages to file
            with open("/tmp/krilin_failed_packages.txt", "w") as f:
                f.write("\n".join(failed_packages))
            print(f"{YELLOW}[*] Complete list saved to /tmp/krilin_failed_packages.txt{NORMAL}")
        else:
            print(f"{GREEN}{BOLD}[+] All packages successfully installed!{NORMAL}")
            print(f"{GREEN}[+] Your complete Kali arsenal is ready.{NORMAL}")
    
    except KeyboardInterrupt:
        print(f"\n{YELLOW}{BOLD}[!] Installation interrupted by user.{NORMAL}")
    except Exception as e:
        print(f"{RED}{BOLD}[!] Unexpected error: {e}{NORMAL}")
    finally:
        fix_dpkg_issues_thoroughly()
        remove_repo("kali")

def install_with_retries(package, repo_type=None, max_retries=3, timeout=300):
    """Install a package with retries on failure."""
    for attempt in range(1, max_retries + 1):
        try:
            # Skip if already installed
            check_cmd = ["dpkg", "-l", package]
            result = subprocess.run(check_cmd, capture_output=True, text=True, check=False)
            if "ii  " + package in result.stdout:
                print(f"{GREEN}[+] {package} is already installed{NORMAL}")
                return True
            
            print(f"{CYAN}[*] Installing {package} (attempt {attempt}/{max_retries})...{NORMAL}")
            
            # Build install command
            if repo_type == "backports":
                codename = get_debian_codename()
                cmd = ['apt-get', 'install', '-y', '-qq', '-t', f"{codename}-backports", package]
            else:
                cmd = ['apt-get', 'install', '-y', '-qq', '--no-install-recommends', package]
            
            # Try installation
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            
            if result.returncode == 0:
                print(f"{GREEN}[+] Successfully installed {package}{NORMAL}")
                return True
            else:
                raise subprocess.CalledProcessError(result.returncode, cmd)
                
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
            print(f"{YELLOW}[!] Attempt {attempt} failed for {package}{NORMAL}")
            
            if attempt < max_retries:
                # Try to fix issues before next attempt
                fix_dpkg_issues_thoroughly()
                time.sleep(2)
            else:
                # Last attempt - try force install
                print(f"{YELLOW}[!] Trying force install for {package}...{NORMAL}")
                try:
                    # Download package
                    subprocess.run(["apt-get", "download", package], check=False, timeout=60)
                    
                    # Find downloaded .deb file
                    deb_files = [f for f in os.listdir(".") if f.startswith(package) and f.endswith(".deb")]
                    if deb_files:
                        # Force install
                        subprocess.run(["dpkg", "--force-all", "-i", deb_files[0]], check=False)
                        # Fix dependencies
                        subprocess.run(["apt-get", "install", "-f", "-y"], check=False)
                        
                        # Clean up
                        for deb_file in deb_files:
                            os.remove(deb_file)
                        
                        print(f"{GREEN}[+] Force installed {package}{NORMAL}")
                        return True
                except:
                    pass
    
    print(f"{RED}[!] Failed to install {package} after {max_retries} attempts.{NORMAL}")
    return False

def install_tools_or_kernel(category, packages, is_kernel, repo_type):
    """Install selected tools or kernel with dramatic flair."""
    weapons = ["arsenal", "weaponry", "armaments", "firepower", "ordnance", "toolkit"]
    power_words = ["Unleashing", "Deploying", "Activating", "Arming", "Initializing", "Loading"]
    
    chosen_weapon = random.choice(weapons)
    power_word = random.choice(power_words)
    
    # Handle special cases
    if category == "All Kali Hacking Tools":
        install_all_kali_tools()
        return
    elif category == "Individual Kali Tools" and not packages:
        packages = select_specific_tools()
        if not packages:
            return
    
    # Dramatic intro
    dramatic_print(f"\n{BOLD}{RED}[*] {power_word} {category} {chosen_weapon}...{NORMAL}", RED, 0.02)
    
    try:
        # Prepare system
        proactively_remove_rpcbind()
        create_apt_preferences()
        
        # Add repository
        if not add_repo(repo_type):
            print(f"{RED}[!] Failed to add {repo_type} repository.{NORMAL}")
            return
        
        # Fix any existing issues
        fix_dpkg_issues_thoroughly()
        
        # Install packages
        print(f"{CYAN}{BOLD}[*] Installing packages: {', '.join(packages)}{NORMAL}")
        
        failed_packages = []
        successful_packages = []
        
        for package in packages:
            if install_with_retries(package, repo_type=repo_type):
                successful_packages.append(package)
            else:
                failed_packages.append(package)
        
        # Report results
        print(f"\n{BOLD}{BLUE}{'='*50}{NORMAL}")
        if successful_packages:
            print(f"{GREEN}{BOLD}[+] Successfully installed:{NORMAL}")
            for pkg in successful_packages:
                print(f"    ✓ {pkg}")
        
        if failed_packages:
            print(f"{YELLOW}{BOLD}[!] Failed to install:{NORMAL}")
            for pkg in failed_packages:
                print(f"    ✗ {pkg}")
        else:
            print(f"{GREEN}{BOLD}[+] All packages installed successfully!{NORMAL}")
            print(f"{GREEN}[+] Your {category.lower()} is ready for action.{NORMAL}")
        
        if is_kernel:
            print(f"\n{YELLOW}{BOLD}[!] IMPORTANT: Please reboot to activate the new kernel.{NORMAL}")
            print(f"{CYAN}[*] Run: sudo reboot{NORMAL}")
    
    except KeyboardInterrupt:
        print(f"\n{YELLOW}{BOLD}[!] Installation interrupted by user.{NORMAL}")
    except Exception as e:
        print(f"{RED}{BOLD}[!] Unexpected error: {e}{NORMAL}")
    finally:
        # Clean up
        fix_dpkg_issues_thoroughly()
        remove_repo(repo_type)

def display_menu():
    """Display the menu with dramatic styling."""
    print(f"\n{BOLD}{BLUE}╔{'═'*55}╗{NORMAL}")
    print(f"{BOLD}{BLUE}║{YELLOW}     KRILIN - SECURITY TOOLS & KERNEL ARSENAL{BLUE}        ║{NORMAL}")
    print(f"{BOLD}{BLUE}╠{'═'*55}╣{NORMAL}")
    
    for key, (category, tools, is_kernel, _) in CATEGORIES.items():
        # Format category name
        if is_kernel:
            icon = "🔧"
            color = RED if key == "9" else YELLOW
        elif key == "10":
            icon = "⚠️"
            color = MAGENTA
        else:
            icon = "📦"
            color = CYAN
        
        # Special warnings
        if key == "9":
            warning = f" {RED}(May affect stability){NORMAL}"
        elif key == "10":
            warning = f" {MAGENTA}(10+ GB download){NORMAL}"
        else:
            warning = ""
        
        print(f"{BOLD}{BLUE}║{NORMAL} {BOLD}{color}[{key:2}] {icon} {category:<30}{warning}{BLUE}║{NORMAL}")
    
    print(f"{BOLD}{BLUE}║{NORMAL} {BOLD}{YELLOW}[0 ] ❌ Exit{' '*40}{BLUE}║{NORMAL}")
    print(f"{BOLD}{BLUE}╚{'═'*55}╝{NORMAL}")
    
    if os.path.exists("/tmp/krilin_failed_packages.txt"):
        print(f"\n{YELLOW}[!] Previous failed installations detected.{NORMAL}")
        print(f"    View with: cat /tmp/krilin_failed_packages.txt")

def check_disk_space():
    """Check available disk space before installation."""
    try:
        stat = os.statvfs('/')
        free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
        
        if free_gb < 5:
            print(f"{RED}{BOLD}[!] WARNING: Only {free_gb:.1f}GB free disk space available.{NORMAL}")
            print(f"{RED}[!] At least 5GB recommended for tool installation.{NORMAL}")
            answer = input(f"{YELLOW}[?] Continue anyway? (y/n):{NORMAL} ").lower()
            if answer != 'y':
                return False
    except:
        pass
    return True

def main():
    """Main function to run the Krilin tool."""
    # Initial checks
    check_root()
    
    # Check and install dependencies
    check_system_dependencies()
    check_python_dependencies()
    
    # Re-import if they were just installed
    global REQUESTS_AVAILABLE, BS4_AVAILABLE
    try:
        import requests
        REQUESTS_AVAILABLE = True
    except:
        pass
    try:
        from bs4 import BeautifulSoup
        BS4_AVAILABLE = True
    except:
        pass
    
    # Display banner and system info
    display_banner()
    detect_system()
    
    # Check disk space
    if not check_disk_space():
        print(f"{YELLOW}[!] Exiting due to insufficient disk space.{NORMAL}")
        sys.exit(1)
    
    # Fix any initial issues
    fix_dpkg_issues_thoroughly()
    
    # Proactive rpcbind handling
    proactively_remove_rpcbind()
    create_apt_preferences()
    
    # Main menu loop
    while True:
        display_menu()
        
        try:
            choice = input(f"\n{BOLD}{GREEN}[?] Select an option (0-{len(CATEGORIES)}):{NORMAL} ").strip()
            
            if choice == "0":
                dramatic_print(f"{BOLD}{BLUE}[*] Exiting Krilin. Stay safe, stay ethical!{NORMAL}", BLUE, 0.02)
                print(f"{GREEN}[*] Thank you for using Krilin Security Framework.{NORMAL}")
                break
            elif choice in CATEGORIES:
                category, packages, is_kernel, repo_type = CATEGORIES[choice]
                install_tools_or_kernel(category, packages, is_kernel, repo_type)
            else:
                print(f"{RED}{BOLD}[!] Invalid option. Please select 0-{len(CATEGORIES)}.{NORMAL}")
        
        except KeyboardInterrupt:
            print(f"\n{YELLOW}{BOLD}[!] Interrupted. Returning to menu...{NORMAL}")
            continue
        except EOFError:
            print(f"\n{YELLOW}{BOLD}[!] Input terminated. Exiting...{NORMAL}")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}{BOLD}[!] Operation cancelled by user.{NORMAL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}{BOLD}[!] Fatal error: {e}{NORMAL}")
        print(f"{YELLOW}[*] Please report this issue at: https://github.com/0xb0rn3/krilin/issues{NORMAL}")
        sys.exit(1)
