import psutil
import time
import platform
import socket
import os
from datetime import datetime

RED = "\033[1;91m"
GREEN = "\033[1;92m"
YELLOW = "\033[1;93m"
RESET = "\033[0m"
old_net = psutil.net_io_counters()

def get_cpu_status(cpu):
    if cpu > 80:
        return RED, "HIGH"
    elif cpu > 50:
        return YELLOW, "MODERATE"
    else:
        return GREEN, "OK"

try:
    while True:
        print("\033[2J\033[H", end="")

        # Uptime
        uptime_seconds = time.time() - psutil.boot_time()
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        battery = psutil.sensors_battery()
        
        # System Information
        hostname = socket.gethostname()
        os_platform = platform.freedesktop_os_release()["PRETTY_NAME"]
        kernel = platform.release()
        disk = psutil.disk_usage("/")
        used_disk = disk.used / (1024 ** 3)
        total_disk = disk.total / (1024 ** 3)
        disk_text = f"{used_disk:.1f} / {total_disk:.1f} GiB ({disk.percent:.0f}%)"
        
        # CPU
        cpu = psutil.cpu_percent()
        temps = psutil.sensors_temperatures()
        
        cpu_temp = "N/A"
        for sensor_list in temps.values():
            if len(sensor_list) > 0:
                cpu_temp = f"{sensor_list[0].current:.1f}°C"
                break
            
        # Memory
        ram = psutil.virtual_memory()
        used_ram = ram.used / (1024 ** 3)
        total_ram = ram.total / (1024 ** 3)
        ram_text = f"{used_ram:.1f} / {total_ram:.1f} GiB ({ram.percent:.0f}%)"

        # Network
        new_net = psutil.net_io_counters()
        download = new_net.bytes_recv - old_net.bytes_recv
        upload = new_net.bytes_sent - old_net.bytes_sent
        old_net = new_net
        interval = 1.5
        download_mb = (download / interval) / 1024 / 1024
        upload_mb = (upload / interval) / 1024 / 1024

        cpu_color, cpu_text = get_cpu_status(cpu)
            
        print("=== SYSTEM DASHBOARD ===")
        print()
        current_time = datetime.now().strftime("%H:%M:%S")
        LABEL_WIDTH = 15
        print(f"{'TIME:':<{LABEL_WIDTH}}{current_time}")
        print(f"{'UPTIME:':<{LABEL_WIDTH}}{hours:02d}:{minutes:02d}")
        if battery:
            print(f"{'BATTERY:':<{LABEL_WIDTH}}{battery.percent:.0f}%")
        print(f"{'HOST:':<{LABEL_WIDTH}}{hostname:<29}")
        print(f"{'OS:':<{LABEL_WIDTH}}{os_platform:<31}")
        print(f"{'KERNEL:':<{LABEL_WIDTH}}{kernel}")
        print()
        print(f"{'DISK:':<{LABEL_WIDTH}}{disk_text:<29}")
        print(f"{'CPU:':<{LABEL_WIDTH}}{cpu_color}{cpu}% ({cpu_text}){RESET}")
        print(f"{'CPU TEMP:':<{LABEL_WIDTH}}{cpu_temp}°C")
        print(f"{'RAM:':<{LABEL_WIDTH}}{ram_text:<30}")
        print()
        print(f"{'NET RX:':<{LABEL_WIDTH}}{download_mb:.2f} MB/s")
        print(f"{'NET TX:':<{LABEL_WIDTH}}{upload_mb:.2f} MB/s")
        print()
        print("=" * 24)
        print()
        
        time.sleep(1.0)

except KeyboardInterrupt:
    print(" EXITING DASHBOARD...")

