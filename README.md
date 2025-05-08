## 🧠 How Krilin Works

Krilin operates through a sophisticated multi-stage process:

1. **System Analysis**: First, Krilin performs comprehensive system detection to identify your OS details, architecture, kernel version, CPU, RAM, and Debian version to ensure compatibility.

2. **Environment Preparation**: Before any installations, Krilin:
   - Verifies root privileges
   - Ensures all required dependencies are installed
   - Fixes any existing package management issues
   - Creates necessary configurations to prevent conflicts

3. **Repository Management**: When installing tools, Krilin:
   - Downloads and installs the official Kali archive keyring
   - Creates temporary repository configuration files
   - Updates package lists with proper error handling
   - Implements APT preferences to prevent unwanted package installations

4. **Installation Process**: During installation, Krilin:
   - Displays progress with dynamic visual feedback
   - Handles package installations with multiple retry attempts
   - Resolves dependencies and conflicts automatically
   - Implements batch processing for large installations to prevent system overload

5. **System Cleanup**: After completing installations, Krilin:
   - Removes temporary repository configurations
   - Updates package lists to reflect system changes
   - Runs comprehensive package management fixes
   - Ensures your system remains stable and clean

This approach allows Krilin to integrate powerful security tools while maintaining system integrity and stability.# Krilin v0.2

<div align="center">
  <img src="https://raw.githubusercontent.com/0xb0rn3/krilin/main/assets/krilin-logo.png" alt="Krilin Logo" width="200">
  <h3>Weaponize Your Debian System with Kali Linux Arsenal</h3>
  
  ![Version](https://img.shields.io/badge/Version-0.2-success.svg)
  ![Status](https://img.shields.io/badge/Status-Stable-success.svg)
  ![License](https://img.shields.io/badge/License-MIT-blue.svg)
  ![Python](https://img.shields.io/badge/Python-3.6+-green.svg)
  ![Platform](https://img.shields.io/badge/Platform-Debian-red.svg)
</div>

## 🔥 Overview

**Krilin** transforms your Debian-based system into a powerful penetration testing platform by seamlessly integrating selected Kali Linux tools and kernels. It preserves your user environment without rebranding your system into Kali Linux, providing a safe and efficient way to access professional security tools.

The tool intelligently handles repository management, package dependencies, and system compatibility to ensure a smooth integration process. With its dramatic visual interface and robust error handling, Krilin makes setting up a penetration testing environment both effective and enjoyable.

## ✨ Key Features

- **🛠️ Comprehensive Tool Selection**: Access a wide range of security tools organized by purpose
- **🔍 Intelligent System Detection**: Automatically identifies OS, architecture, hardware details, and Debian version
- **👨‍💻 Interactive Tool Selection**: Choose from pre-defined categories or select individual Kali tools
- **🚀 Modern User Interface**: Dramatic color-coded interface with dynamic text effects
- **🔧 Advanced Kernel Management**: Install specialized kernels from Kali or Debian Backports
- **🔐 Secure Repository Integration**: Manages Kali repositories and official keyrings for maximum security
- **🧹 System Integrity Protection**: Automatically removes repositories after installation to maintain system stability
- **🛡️ Conflict Prevention**: Proactively handles package conflicts and prevents common installation issues
- **♻️ Robust Error Recovery**: Implements multiple retries and fixes package management problems automatically

## 📷 Screenshots

<div align="center">
  <img src="https://raw.githubusercontent.com/0xb0rn3/krilin/main/assets/krilin-demo.png" alt="Krilin Demo" width="600">
</div>

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/0xb0rn3/krilin.git

# Navigate to the directory
cd krilin

# Make the script executable
chmod +x run

# Run with root privileges
sudo ./run
```

## 🎯 Usage

Run the script with root privileges:

```bash
sudo ./run
```

Select from the available categories:

1. Information Gathering - Install reconnaissance tools like nmap, dnsrecon, and theharvester
2. Vulnerability Analysis - Install assessment tools like nikto, sqlmap, and lynis
3. Exploitation Tools - Install metasploit-framework, exploitdb, and SET
4. Wireless Attacks - Install aircrack-ng, reaver, wifite, and kismet
5. Web Application Analysis - Install burpsuite, zaproxy, wfuzz, and dirb
6. Password Attacks - Install hydra, john, hashcat, crunch, and wordlists
7. Individual Kali Tools - Select specific tools to install from the complete Kali arsenal
8. Debian Backports Kernel - Install the latest kernel from Debian Backports
9. Kali Linux Kernel - Install the specialized Kali Linux kernel
10. Complete Kali Linux Toolkit + Kernel - Install all available Kali hacking tools (10+ GB)

## ⚙️ System Requirements

- Debian-based system (Debian, Ubuntu, Linux Mint, etc.)
- Python 3.6 or higher
- Root privileges (sudo)
- Active internet connection
- Required Python packages (auto-installed if missing):
  - python3-requests
  - python3-bs4 (BeautifulSoup)
- Required system utilities (auto-installed if missing):
  - wget
  - apt-transport-https
  - gnupg

## 🔐 Security Considerations

Krilin temporarily adds Kali Linux repositories to your system during tool installation. These repositories are automatically removed after installation to maintain system integrity. The script uses the official Kali archive keyring for maximum security.

The tool implements several security measures to protect your system:

- **Official Keyring Integration**: Downloads and installs the official Kali archive keyring to verify package authenticity
- **Package Conflict Resolution**: Proactively removes problematic packages like rpcbind that can cause installation issues
- **Repository Isolation**: Creates temporary repository files that are automatically removed after use
- **APT Preferences Management**: Configures APT preferences to prevent unwanted package installations
- **Thorough Cleanup Procedures**: Executes comprehensive system cleanup after installations

## ⚠️ Important Warning

Installing certain tools or kernels may affect system stability. Always understand the implications before installing, especially:

- Kali Linux kernel on Debian systems
- Full penetration testing toolsets on production machines

Krilin implements safeguards to minimize risks, including:

- Batch installation for large tool collections to prevent system overload
- Multiple installation retries with automatic error recovery
- Package management issue detection and resolution
- Confirmation prompts for potentially disruptive operations
- Detailed warnings before installing all Kali tools (option 10)

## 🤝 Contributing

Contributions are welcome and appreciated! Please follow these steps:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## 👨‍💻 Author

**0xb0rn3** - [GitHub Profile](https://github.com/0xb0rn3)

## 🙏 Acknowledgements

- [Kali Linux](https://www.kali.org/) for their exceptional security tools
- [Debian](https://www.debian.org/) for the stable base system
- All open-source security tool developers who make this project possible

---

<div align="center">
  <sub>Built with ❤️ by 0xb0rn3</sub>
</div>
