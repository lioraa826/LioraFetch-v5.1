import os
import sys
import time
import platform
import subprocess
import shutil
import termios
import tty

# --- TONY STARK ANIMASYONU ---
def print_typing(text, speed=0.02, color='\033[96m'):
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print('\033[0m')

def tony_stark_boot():
    os.system('clear')
    print_typing("INITIALIZING STARK INDUSTRIES MAINFRAME...", 0.03, '\033[1;36m')
    print_typing("BYPASSING SECURITY PROTOCOLS... [OK]", 0.01)
    print_typing("LOADING CORE SYSTEM MODULES... [OK]", 0.01)
    print_typing("ESTABLISHING NEURAL LINK...", 0.02)
    print_typing("WAKING UP LIORAFETCH ENGINE...", 0.04, '\033[1;33m')
    time.sleep(0.5)
    os.system('clear')

# --- SİSTEM BİLGİSİ TOPLAMA ---
def get_sys_info():
    info = {}
    
    # Kullanıcı ve Host
    info['User'] = f"\033[1;36m{os.environ.get('USER')}@{platform.node()}\033[0m"
    
    # İşletim Sistemi
    try:
        with open('/etc/os-release') as f:
            for line in f:
                if line.startswith('PRETTY_NAME='):
                    info['OS'] = line.split('=')[1].strip().strip('"')
                    break
    except:
        info['OS'] = platform.system()

    # Kernel
    info['Kernel'] = platform.release()

    # Çalışma Süresi (Uptime)
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            info['Uptime'] = f"{hours} hours, {minutes} mins"
    except:
        info['Uptime'] = "Unknown"

    # Paketler (dpkg, pacman, rpm destekli)
    packages = 0
    try:
        if shutil.which("dpkg"):
            packages = int(subprocess.check_output("dpkg-query -f '.\n' -W | wc -l", shell=True))
            info['Packages'] = f"{packages} (dpkg)"
        elif shutil.which("pacman"):
            packages = int(subprocess.check_output("pacman -Qq | wc -l", shell=True))
            info['Packages'] = f"{packages} (pacman)"
        elif shutil.which("rpm"):
            packages = int(subprocess.check_output("rpm -qa | wc -l", shell=True))
            info['Packages'] = f"{packages} (rpm)"
        else:
            info['Packages'] = "Unknown"
    except:
        info['Packages'] = "Unknown"

    # Shell
    info['Shell'] = os.environ.get('SHELL', 'Unknown').split('/')[-1]

    # Masaüstü Ortamı (DE / WM)
    info['DE/WM'] = os.environ.get('XDG_CURRENT_DESKTOP') or os.environ.get('DESKTOP_SESSION') or "Terminal"

    # CPU
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('model name'):
                    info['CPU'] = line.split(':')[1].strip()
                    break
    except:
        info['CPU'] = platform.processor()

    # GPU
    try:
        gpu_info = subprocess.check_output("lspci | grep -i vga", shell=True).decode('utf-8')
        info['GPU'] = gpu_info.split(':')[2].split(' (')[0].strip()
    except:
        info['GPU'] = "Unknown"

    # Bellek (RAM)
    try:
        with open('/proc/meminfo', 'r') as f:
            meminfo = f.readlines()
            total = int(meminfo[0].split()[1]) // 1024
            available = int(meminfo[2].split()[1]) // 1024
            used = total - available
            info['Memory'] = f"{used}MiB / {total}MiB"
    except:
        info['Memory'] = "Unknown"

    return info

# --- EKRANA BASTIRMA VE ASCII ART ---
def display_fetch(info):
    # LioraFetch Özel Logosu
    ascii_art = [
        "\033[96m      __    _                 \033[0m",
        "\033[96m     / /   (_)___  _________  \033[0m",
        "\033[96m    / /   / / __ \\/ ___/ __ \\ \033[0m",
        "\033[96m   / /___/ / /_/ / /  / /_/ / \033[0m",
        "\033[96m  /_____/_/\\____/_/   \\__,_/  \033[0m",
        "\033[1;36m       F E T C H   O S        \033[0m"
    ]

    keys = list(info.keys())
    # Sadece ilk satırı ayırıcı çizgi olarak kullanacağız, diğerleri data
    max_lines = max(len(ascii_art), len(keys))

    print()
    for i in range(max_lines):
        left_side = ascii_art[i] if i < len(ascii_art) else " " * 30
        
        if i < len(keys):
            k = keys[i]
            v = info[k]
            if k == 'User':
                right_side = f"{v}"
            else:
                right_side = f"\033[1;33m{k}:\033[0m {v}"
        else:
            right_side = ""
            
        print(f"{left_side}   {right_side}")
    print()

# --- ETKİLEŞİM ('C' TUŞU) ---
def listen_for_c():
    print("\033[90m[Kapatmak için herhangi bir tuşa, geliştiriciyi görmek için 'c' ye bas]\033[0m")
    
    # Unix sistemlerinde tuş vuruşunu anında yakalamak için
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch.lower() == 'c':
            # Satır başına dönüp eski yazıyı temizleyerek Liora mesajını bas
            sys.stdout.write('\r' + ' ' * 70 + '\r') 
            sys.stdout.write("\033[1;35m>>> Co-Developer: Liora - Core Systems AI <<<\033[0m\r\n")
        else:
            sys.stdout.write('\r\n')
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

if __name__ == "__main__":
    tony_stark_boot()
    sys_data = get_sys_info()
    display_fetch(sys_data)
    listen_for_c()
