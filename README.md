# Krilin v0.2

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

## ✨ Key Features

- **🛠️ Comprehensive Tool Selection**: Access a wide range of security tools organized by purpose
- **🔍 Intelligent System Detection**: Automatically identifies OS, architecture, and hardware details
- **🚀 Modern User Interface**: Clean, color-coded interface with intuitive navigation
- **🔧 Advanced Kernel Management**: Easily install specialized kernels from Kali or Debian Backports
- **🔐 Secure Repository Integration**: Properly manages Kali repositories and keys for maximum security
- **🧹 System Integrity Protection**: Automatically removes repositories after installation to maintain system stability

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

1. Information Gathering
2. Vulnerability Analysis
3. Exploitation Tools
4. Wireless Attacks
5. Web Application Analysis
6. Password Attacks
7. Individual Kali Tools
8. Debian Backports Kernel
9. Kali Linux Kernel
10. Complete Kali Linux Toolkit + Kernel

## ⚙️ System Requirements

- Debian-based system (Debian, Ubuntu, Linux Mint, etc.)
- Python 3.6 or higher
- Root privileges (sudo)
- Active internet connection

## 🔐 Security Considerations

Krilin temporarily adds Kali Linux repositories to your system during tool installation. These repositories are automatically removed after installation to maintain system integrity. The script uses the official Kali archive keyring for maximum security.

## ⚠️ Important Warning

Installing certain tools or kernels may affect system stability. Always understand the implications before installing, especially:

- Kali Linux kernel on Debian systems
- Full penetration testing toolsets on production machines

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
