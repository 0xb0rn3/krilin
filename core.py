#!/usr/bin/env python3
import os
import subprocess
import sys
import platform
import random
import time
import re
import tempfile
import shutil
import requests
from bs4 import BeautifulSoup

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

# Categories including tools and kernels
CATEGORIES = {
    "1": ("Information Gathering", ["nmap", "kali-menu", "dnsrecon", "theharvester", "recon-ng"], False, "kali"),
    "2": ("Vulnerability Analysis", ["nikto", "kali-menu", "sqlmap", "lynis"], False, "kali"),
    "3": ("Exploitation Tools", ["metasploit-framework", "kali-menu", "exploitdb", "set"], False, "kali"),
    "4": ("Wireless Attacks", ["aircrack-ng", "kali-menu", "reaver", "wifite", "kismet"], False, "kali"),
    "5": ("Web Application Analysis", ["burpsuite", "kali-menu", "zaproxy", "wfuzz", "dirb"], False, "kali"),
    "6": ("Password Attacks", ["hydra", "john", "kali-menu", "hashcat", "crunch", "wordlists"], False, "kali"),
    "7": ("Individual Kali Tools", [], False, "kali"),  # Will prompt for specific tools
    "8": ("Debian Backports Kernel", ["linux-image-amd64"], True, "backports"),
    "9": ("Kali Linux Kernel", ["linux-image-amd64"], True, "kali"),
    "10": ("All Kali Hacking Tools", [], False, "kali")  # New option for all tools
}

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
                                                 
{BLUE}{BOLD}╔══════════════════════════════════╗{NORMAL}
{BLUE}{BOLD}║{GREEN} KRILIN - TOOLS AND KERNEL ARSENAL {BLUE}║{NORMAL}
{BLUE}{BOLD}║{GREEN} Pentest Machine Setup v{VERSION}           {BLUE}║{NORMAL}
{BLUE}{BOLD}╚══════════════════════════════════╝{NORMAL}
"""
    print(banner)

def detect_system():
    """Detect and display system information."""
    # Get system information
    os_name = platform.system()
    os_release = platform.release()
    os_version = platform.version()
    machine_arch = platform.machine()
    
    # Get kernel information
    kernel_info = subprocess.check_output("uname -r", shell=True).decode().strip()
    
    # Get CPU information
    cpu_info = "Unknown"
    if os.path.exists("/proc/cpuinfo"):
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if "model name" in line:
                    cpu_info = line.split(":")[1].strip()
                    break
    
    # Get RAM information
    ram_info = "Unknown"
    if os.path.exists("/proc/meminfo"):
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if "MemTotal" in line:
                    ram_info = line.split(":")[1].strip()
                    break
    
    # Format and display system information
    print(f"\n{BOLD}{BLUE}[*] System Detection Results:{NORMAL}")
    print(f"{BOLD}{GREEN}[+] OS:{NORMAL} {os_name} {os_release}")
    print(f"{BOLD}{GREEN}[+] OS Version:{NORMAL} {os_version}")
    print(f"{BOLD}{GREEN}[+] Architecture:{NORMAL} {machine_arch}")
    print(f"{BOLD}{GREEN}[+] Kernel:{NORMAL} {kernel_info}")
    print(f"{BOLD}{GREEN}[+] CPU:{NORMAL} {cpu_info}")
    print(f"{BOLD}{GREEN}[+] Memory:{NORMAL} {ram_info}")
    
    # Check if it's a Debian-based system
    is_debian = False
    if os.path.exists("/etc/debian_version"):
        with open("/etc/debian_version", "r") as f:
            debian_version = f.read().strip()
            print(f"{BOLD}{GREEN}[+] Debian Version:{NORMAL} {debian_version}")
            is_debian = True
    
    if not is_debian:
        print(f"{BOLD}{RED}[!] Warning: This script is designed for Debian-based systems.{NORMAL}")
        answer = input(f"{BOLD}{YELLOW}[?] Continue anyway? (y/n):{NORMAL} ").lower()
        if answer != 'y':
            sys.exit(1)

def check_root():
    """Ensure the script runs with root privileges."""
    if os.geteuid() != 0:
        print(f"{RED}{BOLD}[!] This script must be run as root. Use 'sudo'.{NORMAL}")
        sys.exit(1)

def get_debian_codename():
    """Retrieve Debian codename from /etc/os-release."""
    try:
        with open("/etc/os-release", "r") as f:
            for line in f:
                if line.startswith("VERSION_CODENAME="):
                    return line.split("=")[1].strip().strip('"')
    except Exception as e:
        print(f"{YELLOW}{BOLD}[!] Warning: Could not determine Debian codename: {e}{NORMAL}")
        # Fallback to using lsb_release
        try:
            result = subprocess.run(["lsb_release", "-cs"], stdout=subprocess.PIPE, text=True, check=True)
            return result.stdout.strip()
        except Exception:
            print(f"{RED}{BOLD}[!] Could not determine Debian codename.{NORMAL}")
            codename = input(f"{BOLD}{YELLOW}[?] Please enter your Debian codename (e.g., bookworm, bullseye):{NORMAL} ")
            if codename:
                return codename
            sys.exit(1)

def add_kali_keyring():
    """Download and install the Kali archive keyring package."""
    keyring_url = "https://archive.kali.org/kali/pool/main/k/kali-archive-keyring/kali-archive-keyring_2025.1_all.deb"
    keyring_file = "/tmp/kali-archive-keyring.deb"
    
    print(f"{CYAN}{BOLD}[*] Downloading and installing Kali archive keyring...{NORMAL}")
    
    try:
        # Download the keyring package
        subprocess.run(["wget", "-q", "-O", keyring_file, keyring_url], check=True)
        
        # Install the keyring package
        subprocess.run(["dpkg", "-i", keyring_file], check=True)
        
        # Clean up
        if os.path.exists(keyring_file):
            os.remove(keyring_file)
            
        print(f"{GREEN}{BOLD}[+] Kali archive keyring installed successfully.{NORMAL}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"{RED}{BOLD}[!] Error installing Kali keyring: {e}{NORMAL}")
        print(f"{YELLOW}[!] Continuing without official Kali keyring. This may cause trust issues.{NORMAL}")
        return False

def add_repo(repo_type):
    """Add a temporary repository based on type."""
    print(f"{CYAN}{BOLD}[*] Adding {repo_type} repository...{NORMAL}")
    
    if repo_type == "kali":
        # Add Kali Linux GPG key via the keyring package
        add_kali_keyring()
        
        # Add repository
        with open("/etc/apt/sources.list.d/kali.list", "w") as f:
            f.write(f"{KALI_REPO}\n")
            
    elif repo_type == "backports":
        codename = get_debian_codename()
        with open("/etc/apt/sources.list.d/backports.list", "w") as f:
            f.write(f"deb http://deb.debian.org/debian {codename}-backports main contrib non-free non-free-firmware\n")
    
    # Update apt cache
    print(f"{CYAN}{BOLD}[*] Updating package lists...{NORMAL}")
    try:
        subprocess.run(["apt-get", "update"], check=True)
        print(f"{GREEN}{BOLD}[+] Repository added and package list updated.{NORMAL}")
    except subprocess.CalledProcessError:
        print(f"{RED}{BOLD}[!] Failed to update package lists. Continuing anyway...{NORMAL}")

def proactively_remove_rpcbind():
    """Proactively remove rpcbind before any installations to prevent issues."""
    print(f"{CYAN}{BOLD}[*] Proactively handling rpcbind package to prevent installation issues...{NORMAL}")
    
    # First check if it's installed
    if check_for_rpcbind():
        print(f"{YELLOW}{BOLD}[!] rpcbind detected - removing to prevent installation issues...{NORMAL}")
        # Stop and disable the service
        try:
            subprocess.run(["systemctl", "stop", "rpcbind"], check=False)
            subprocess.run(["systemctl", "disable", "rpcbind"], check=False)
            subprocess.run(["systemctl", "stop", "rpcbind.socket"], check=False)
            subprocess.run(["systemctl", "disable", "rpcbind.socket"], check=False)
        except Exception as e:
            print(f"{YELLOW}{BOLD}[!] Warning when stopping rpcbind service: {e}{NORMAL}")
        
        # Remove the package with force
        try:
            subprocess.run(["dpkg", "--remove", "--force-all", "rpcbind"], check=False)
            subprocess.run(["apt-get", "remove", "--purge", "-y", "rpcbind"], check=False)
            print(f"{GREEN}{BOLD}[+] rpcbind removed.{NORMAL}")
        except Exception as e:
            print(f"{YELLOW}{BOLD}[!] Warning when removing rpcbind: {e}{NORMAL}")
    
    # Create and apply diversion for rpcbind
    create_rpcbind_diversion()

def create_rpcbind_diversion():
    """Create a diversion for rpcbind to prevent its installation."""
    try:
        # Create a dummy rpcbind package to divert and prevent installation
        dummy_dir = "/tmp/dummy-rpcbind"
        os.makedirs(dummy_dir, exist_ok=True)
        
        # Create a simple postinst script that succeeds immediately
        with open(f"{dummy_dir}/postinst", "w") as f:
            f.write("#!/bin/sh\nexit 0\n")
        os.chmod(f"{dummy_dir}/postinst", 0o755)
        
        # Create a dummy rpcbind binary
        os.makedirs(f"{dummy_dir}/usr/sbin", exist_ok=True)
        with open(f"{dummy_dir}/usr/sbin/rpcbind", "w") as f:
            f.write("#!/bin/sh\necho 'Dummy rpcbind - not functional'\nexit 0\n")
        os.chmod(f"{dummy_dir}/usr/sbin/rpcbind", 0o755)
        
        # Set up the diversion
        if os.path.exists("/var/lib/dpkg/info/rpcbind.postinst"):
            subprocess.run(["dpkg-divert", "--local", "--rename", "--add", "/var/lib/dpkg/info/rpcbind.postinst"], check=False)
            shutil.copy2(f"{dummy_dir}/postinst", "/var/lib/dpkg/info/rpcbind.postinst")
            print(f"{GREEN}{BOLD}[+] Created diversion for rpcbind postinst script.{NORMAL}")
        
        # Also divert the binary itself
        subprocess.run(["dpkg-divert", "--local", "--rename", "--add", "/usr/sbin/rpcbind"], check=False)
        shutil.copy2(f"{dummy_dir}/usr/sbin/rpcbind", "/usr/sbin/rpcbind")
        
        print(f"{GREEN}{BOLD}[+] Created diversions to prevent rpcbind issues.{NORMAL}")
        
        # Clean up
        shutil.rmtree(dummy_dir, ignore_errors=True)
        
    except Exception as e:
        print(f"{YELLOW}{BOLD}[!] Warning when creating diversions: {e}{NORMAL}")

def check_for_rpcbind():
    """Check if rpcbind is installed."""
    try:
        # Use dpkg-query to check if rpcbind is installed
        result = subprocess.run(
            ["dpkg-query", "-W", "-f='${Status}'", "rpcbind"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            universal_newlines=True,
            check=False
        )
        return "install ok installed" in result.stdout
    except Exception:
        return False

def fix_dpkg_issues():
    """Fix any interrupted dpkg installations."""
    print(f"{CYAN}{BOLD}[*] Fixing any interrupted package installations...{NORMAL}")
    
    try:
        # First try standard dpkg configure
        subprocess.run(["dpkg", "--configure", "-a"], check=False)
        
        # Then try apt --fix-broken install
        subprocess.run(["apt-get", "install", "-f", "-y"], check=False)
        
        print(f"{GREEN}{BOLD}[+] Package configuration fixed.{NORMAL}")
    except Exception as e:
        print(f"{YELLOW}{BOLD}[!] Warning when fixing package configuration: {e}{NORMAL}")

def create_apt_preferences():
    """Create proper APT preferences to prevent rpcbind installation."""
    prefs_dir = "/etc/apt/preferences.d"
    os.makedirs(prefs_dir, exist_ok=True)
    
    with open(f"{prefs_dir}/block-rpcbind", "w") as f:
        f.write("Package: rpcbind\n")
        f.write("Pin: release *\n")
        f.write("Pin-Priority: -1\n")
    
    print(f"{GREEN}{BOLD}[+] Created APT preferences to block rpcbind installation.{NORMAL}")

def remove_repo(repo_type):
    """Remove the temporary repository."""
    print(f"{CYAN}{BOLD}[*] Cleaning up {repo_type} repository...{NORMAL}")
    
    # Fix any interrupted dpkg operations
    fix_dpkg_issues()
    
    # Then remove the repository files
    if repo_type == "kali" and os.path.exists("/etc/apt/sources.list.d/kali.list"):
        os.remove("/etc/apt/sources.list.d/kali.list")
    elif repo_type == "backports" and os.path.exists("/etc/apt/sources.list.d/backports.list"):
        os.remove("/etc/apt/sources.list.d/backports.list")
    
    # Update apt cache
    try:
        subprocess.run(["apt-get", "update"], check=True)
        print(f"{GREEN}{BOLD}[+] Repository removed and package list updated.{NORMAL}")
    except subprocess.CalledProcessError:
        print(f"{YELLOW}{BOLD}[!] Warning: Cleanup incomplete. You may need to manually fix your repositories.{NORMAL}")

def select_specific_tools():
    """Allow the user to select specific Kali tools."""
    print(f"{CYAN}{BOLD}[*] Enter the names of Kali tools you want to install (separated by spaces):{NORMAL}")
    print(f"{YELLOW}{BOLD}[!] Example: nmap dirb nikto sqlmap{NORMAL}")
    tools_input = input(f"{BOLD}{GREEN}[?] Tools to install:{NORMAL} ")
    
    if tools_input.strip():
        return tools_input.strip().split()
    else:
        print(f"{RED}{BOLD}[!] No tools specified. Returning to menu.{NORMAL}")
        return []

def fetch_all_kali_tools():
    """Fetch all available Kali tools from the website."""
    print(f"{CYAN}{BOLD}[*] Fetching list of all Kali tools from {KALI_TOOLS_URL}...{NORMAL}")
    
    try:
        # Check if requests and BeautifulSoup are available
        try:
            import requests
            from bs4 import BeautifulSoup
        except ImportError:
            print(f"{YELLOW}{BOLD}[!] Required libraries not found. Installing...{NORMAL}")
            subprocess.run(["apt-get", "install", "-y", "python3-requests", "python3-bs4"], check=True)
            import requests
            from bs4 import BeautifulSoup
        
        # Fetch the webpage content
        response = requests.get(KALI_TOOLS_URL)
        if response.status_code != 200:
            print(f"{RED}{BOLD}[!] Failed to fetch the tools list from website. HTTP status: {response.status_code}{NORMAL}")
            return []
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all tool links - looking for links to tool pages
        tool_packages = []
        
        # Find the table containing the tools list
        tools_table = soup.find('table', class_='contenttable')
        if tools_table:
            # Process each row in the table
            rows = tools_table.find_all('tr')
            for row in rows:
                # Skip the header row
                if row.find('th'):
                    continue
                
                # Find the package name column
                cells = row.find_all('td')
                if len(cells) >= 2:  # At least 2 columns for name and package
                    # The second column usually contains the package name
                    package_name = cells[1].text.strip()
                    if package_name and package_name != "N/A":
                        tool_packages.append(package_name)
        
        # If we didn't find tools in the expected format, try an alternative approach
        if not tool_packages:
            # Look for all links to tool pages
            for link in soup.find_all('a'):
                href = link.get('href', '')
                if '/tools/' in href and href.endswith('/'):
                    # Extract the package name from the URL
                    package_name = href.split('/')[-2]
                    if package_name and package_name not in tool_packages:
                        tool_packages.append(package_name)
        
        print(f"{GREEN}{BOLD}[+] Found {len(tool_packages)} Kali tools.{NORMAL}")
        
        return tool_packages
        
    except Exception as e:
        print(f"{RED}{BOLD}[!] Error fetching Kali tools list: {e}{NORMAL}")
        print(f"{YELLOW}{BOLD}[!] Falling back to apt-cache method...{NORMAL}")
        return fetch_kali_tools_from_apt()

def fetch_kali_tools_from_apt():
    """Alternative method to get Kali tools using apt-cache after adding the repository."""
    print(f"{CYAN}{BOLD}[*] Fetching Kali tools from repository...{NORMAL}")
    
    try:
        # First add the Kali repository temporarily
        add_repo("kali")
        
        # Use apt-cache to search for metapackages containing "kali-"
        cmd = ["apt-cache", "search", "kali-"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        
        # Parse the output to get package names
        kali_tools = []
        for line in result.stdout.split("\n"):
            if line.strip():
                # Extract package name (first part before the dash)
                package_name = line.split(" - ")[0].strip()
                if package_name.startswith("kali-") or "tools" in package_name:
                    kali_tools.append(package_name)
        
        # Also add some common individual tools not in meta-packages
        common_tools = [
            "nmap", "dirb", "nikto", "sqlmap", "hydra", "john", "hashcat", 
            "metasploit-framework", "burpsuite", "wireshark", "aircrack-ng",
            "exploitdb", "recon-ng", "wfuzz", "wpscan", "lynis", "crackmapexec"
        ]
        kali_tools.extend(common_tools)
        
        # Remove duplicates
        kali_tools = list(set(kali_tools))
        
        print(f"{GREEN}{BOLD}[+] Found {len(kali_tools)} Kali tools and metapackages.{NORMAL}")
        return kali_tools
    
    except Exception as e:
        print(f"{RED}{BOLD}[!] Error fetching Kali tools from repository: {e}{NORMAL}")
        # Return a minimal default set of tools
        print(f"{YELLOW}{BOLD}[!] Using minimal default tool set.{NORMAL}")
        return [
            "kali-tools-top10", "kali-linux-default", "nmap", "dirb", "nikto", 
            "sqlmap", "hydra", "john", "metasploit-framework", "burpsuite"
        ]

def install_all_kali_tools():
    """Install all available Kali tools."""
    print(f"{MAGENTA}{BOLD}[*] Preparing to install all Kali hacking tools...{NORMAL}")
    
    # Fetch the list of all tools
    tool_packages = fetch_all_kali_tools()
    
    if not tool_packages:
        print(f"{RED}{BOLD}[!] Could not retrieve the list of Kali tools. Aborting.{NORMAL}")
        return
    
    # Show the number of tools to be installed
    print(f"{CYAN}{BOLD}[*] Found {len(tool_packages)} tools to install.{NORMAL}")
    
    # Warn about disk space and time
    print(f"{YELLOW}{BOLD}[!] WARNING: Installing all tools will require significant disk space (10+ GB){NORMAL}")
    print(f"{YELLOW}{BOLD}[!] and may take several hours to complete.{NORMAL}")
    
    # Confirm installation
    confirmation = input(f"{BOLD}{RED}[?] Are you sure you want to install ALL Kali tools? (y/n):{NORMAL} ").lower()
    if confirmation != 'y':
        print(f"{YELLOW}{BOLD}[!] All tools installation cancelled.{NORMAL}")
        return
    
    # Offer to install in batches
    batch_option = input(f"{BOLD}{YELLOW}[?] Install in batches of 10 tools (recommended) or all at once? (b/a):{NORMAL} ").lower()
    
    try:
        # Proactively handle rpcbind before adding repositories
        proactively_remove_rpcbind()
        create_apt_preferences()
        
        # Add Kali repository
        add_repo("kali")
        fix_dpkg_issues()
        
        # First try to install metapackages if available
        metapackages = [pkg for pkg in tool_packages if pkg.startswith("kali-")]
        if metapackages:
            print(f"{CYAN}{BOLD}[*] First installing meta-packages...{NORMAL}")
            for meta in metapackages:
                try:
                    print(f"{CYAN}[*] Installing {meta}...{NORMAL}")
                    subprocess.run(['apt-get', 'install', '-y', '--no-install-recommends', meta], check=True, timeout=300)
                    print(f"{GREEN}[+] Successfully installed {meta}{NORMAL}")
                except Exception as e:
                    print(f"{YELLOW}[!] Failed to install {meta}: {e}{NORMAL}")
        
        # Install individual tools
        individual_tools = [pkg for pkg in tool_packages if not pkg.startswith("kali-")]
        failed_packages = []
        
        if batch_option == 'b':
            # Install in batches of 10
            batch_size = 10
            total_batches = (len(individual_tools) + batch_size - 1) // batch_size
            
            for i in range(0, len(individual_tools), batch_size):
                batch = individual_tools[i:i+batch_size]
                batch_num = i // batch_size + 1
                
                print(f"{CYAN}{BOLD}[*] Installing batch {batch_num}/{total_batches}: {', '.join(batch)}{NORMAL}")
                
                try:
                    # Install the batch with a timeout (10 minutes per batch)
                    subprocess.run(['apt-get', 'install', '-y', '--no-install-recommends'] + batch, check=True, timeout=600)
                    print(f"{GREEN}[+] Successfully installed batch {batch_num}{NORMAL}")
                except Exception as e:
                    print(f"{RED}[!] Error in batch {batch_num}: {e}{NORMAL}")
                    # Try installing one by one if batch fails
                    for package in batch:
                        try:
                            print(f"{CYAN}[*] Retry: Installing {package}...{NORMAL}")
                            subprocess.run(['apt-get', 'install', '-y', '--no-install-recommends', package], check=True, timeout=300)
                            print(f"{GREEN}[+] Successfully installed {package}{NORMAL}")
                        except Exception as e:
                            print(f"{RED}[!] Failed to install {package}: {e}{NORMAL}")
                            failed_packages.append(package)
                
                # Fix any issues after each batch
                fix_dpkg_issues()
        else:
            # Install all at once (not recommended for large numbers of packages)
            for package in individual_tools:
                try:
                    print(f"{CYAN}[*] Installing {package}...{NORMAL}")
                    subprocess.run(['apt-get', 'install', '-y', '--no-install-recommends', package], check=True, timeout=300)
                    print(f"{GREEN}[+] Successfully installed {package}{NORMAL}")
                except Exception as e:
                    print(f"{RED}[!] Failed to install {package}: {e}{NORMAL}")
                    failed_packages.append(package)
                    # Try to fix broken packages after each failure
                    fix_dpkg_issues()
        
        if failed_packages:
            print(f"{YELLOW}{BOLD}[!] The following packages failed to install: {', '.join(failed_packages)}{NORMAL}")
            # Save failed packages to a file for reference
            with open("/tmp/krilin_failed_packages.txt", "w") as f:
                f.write("\n".join(failed_packages))
            print(f"{YELLOW}[*] Failed packages list saved to /tmp/krilin_failed_packages.txt{NORMAL}")
        else:
            print(f"{GREEN}{BOLD}[+] All packages successfully installed. Your complete arsenal is ready.{NORMAL}")
    
    except Exception as e:
        print(f"{RED}{BOLD}[!] Unexpected error: {e}{NORMAL}")
    
    finally:
        # Fix any remaining package issues
        fix_dpkg_issues()
        
        # Remove the repo
        remove_repo("kali")

def install_tools_or_kernel(category, packages, is_kernel, repo_type):
    """Install selected tools or kernel with dramatic flair."""
    weapons = ["arsenal", "weaponry", "armaments", "firepower", "ordnance"]
    power_words = ["unleashing", "deploying", "activating", "arming", "initializing"]
    
    chosen_weapon = random.choice(weapons)
    power_word = random.choice(power_words)
    
    # Special handling for different categories
    if category == "All Kali Hacking Tools":
        # For category 10, call dedicated function
        install_all_kali_tools()
        return
    elif category == "Individual Kali Tools" and not packages:
        # For category 7, prompt for specific tools
        packages = select_specific_tools()
        if not packages:
            return
    
    dramatic_print(f"\n{BOLD}{RED}[*] {power_word.upper()} {category} {chosen_weapon}...{NORMAL}", RED, 0.02)
    
    try:
        # Proactively handle rpcbind before adding repositories
        proactively_remove_rpcbind()
        create_apt_preferences()
        
        add_repo(repo_type)
        fix_dpkg_issues()
        
        # Show installation progress
        print(f"{CYAN}{BOLD}[*] Installing packages: {', '.join(packages)}{NORMAL}")
        
        # Install the packages one by one to better handle errors
        failed_packages = []
        for package in packages:
            try:
                print(f"{CYAN}[*] Installing {package}...{NORMAL}")
                
                if repo_type == "backports":
                    codename = get_debian_codename()
                    cmd = ['apt-get', 'install', '-y', '-t', f"{codename}-backports", package]
                else:
                    cmd = ['apt-get', 'install', '-y', '--no-install-recommends', package]
                
                # Run the installation with timeout (5 minutes per package)
                subprocess.run(cmd, check=True, timeout=300)
                print(f"{GREEN}[+] Successfully installed {package}{NORMAL}")
                
            except subprocess.TimeoutExpired:
                print(f"{RED}[!] Installation of {package} timed out after 5 minutes.{NORMAL}")
                failed_packages.append(package)
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Failed to install {package}: {e}{NORMAL}")
                failed_packages.append(package)
                # Try to fix broken packages after each failure
                subprocess.run(["apt-get", "install", "-f", "-y"], check=False)
        
        if failed_packages:
            print(f"{YELLOW}{BOLD}[!] The following packages failed to install: {', '.join(failed_packages)}{NORMAL}")
            print(f"{YELLOW}[*] You may want to try installing them individually later.{NORMAL}")
        else:
            print(f"{GREEN}{BOLD}[+] All packages successfully installed. Your pentesting arsenal is ready.{NORMAL}")
        
        if is_kernel:
            print(f"{YELLOW}{BOLD}[!] Please reboot to activate the new kernel.{NORMAL}")
    
    except Exception as e:
        print(f"{RED}{BOLD}[!] Unexpected error: {e}{NORMAL}")
    
    finally:
        # Fix any remaining package issues
        fix_dpkg_issues()
        
        # Remove the repo
        remove_repo(repo_type)

def display_menu():
    """Display the menu with dramatic styling."""
    print(f"\n{BOLD}{BLUE}╔══════════════════════════════════╗{NORMAL}")
    print(f"{BOLD}{BLUE}║{YELLOW} KRILIN - TOOLS AND KERNEL ARSENAL {BLUE}║{NORMAL}")
    print(f"{BOLD}{BLUE}╚══════════════════════════════════╝{NORMAL}")
    
    print(f"\n{BOLD}{GREEN}[*] Choose your weapon:{NORMAL}")
    
    for key, (category, _, is_kernel, _) in CATEGORIES.items():
        if is_kernel and key == "9":
            print(f"{BOLD}{RED}[{key}] {category} {RED}(Warning: may cause instability on Debian){NORMAL}")
        elif key == "10":
            print(f"{BOLD}{MAGENTA}[{key}] {category} {MAGENTA}(Warning: large download, 10+ GB){NORMAL}")
        else:
            print(f"{BOLD}{CYAN}[{key}] {category}{NORMAL}")
    
    print(f"{BOLD}{YELLOW}[0] Exit{NORMAL}")

def check_required_packages():
    """Check and install required packages for Krilin."""
    required_packages = ["python3-requests", "python3-bs4", "wget", "apt-transport-https", "gnupg"]
    
    for pkg in required_packages:
        try:
            subprocess.run(["dpkg", "-s", pkg], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        except Exception:
            print(f"{YELLOW}{BOLD}[!] Required package {pkg} not found. Installing...{NORMAL}")
            try:
                subprocess.run(["apt-get", "install", "-y", pkg], check=True)
            except Exception as e:
                print(f"{RED}{BOLD}[!] Failed to install {pkg}: {e}{NORMAL}")

def main():
    """Main function to run the Krilin tool."""
    check_root()
    display_banner()
    detect_system()
    
    # Check for required packages
    check_required_packages()
    
    # Fix any existing package issues
    fix_dpkg_issues()
    
    # Handle rpcbind globally at startup
    proactively_remove_rpcbind()
    create_apt_preferences()
    
    while True:
        display_menu()
        choice = input(f"\n{BOLD}{GREEN}[?] Select an option (0-{len(CATEGORIES)}):{NORMAL} ").strip()
        
        if choice == "0":
            dramatic_print(f"{BOLD}{BLUE}[*] Exiting Krilin. Happy hunting.{NORMAL}", BLUE, 0.02)
            break
        elif choice in CATEGORIES:
            category, packages, is_kernel, repo_type = CATEGORIES[choice]
            install_tools_or_kernel(category, packages, is_kernel, repo_type)
        else:
            print(f"{RED}{BOLD}[!] Invalid option. Please try again.{NORMAL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}{BOLD}[!] Operation cancelled by user.{NORMAL}")
        sys.exit(0)
