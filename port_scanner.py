import pyfiglet
import sys
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import platform
import subprocess
import re

def print_usage():
    print(f"Usage: python3 {sys.argv[0]} <target> [start_port] [end_port] [-A] [-OS]")
    print("Example: python3 port_scanner.py 192.168.5.65 1 1000 -A -OS")

def scan_port(target_ip, port, timeout=1):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            return port
    return None

def print_scan_header(target, target_ip):
    print("Starting ninjasweep scan at", datetime.now())
    print(f"Scan report for {target} ({target_ip})")
    print("Host is up.\n")

def format_port_table(port_data):
    print("PORT     STATE    SERVICE")
    for port, service in sorted(port_data.items()):
        print(f"{str(port) + '/tcp':<9}open     {service}")

def advanced_scan(target, target_ip, start_port, end_port):
    print(f"Running advanced scan on {target_ip} ports {start_port}-{end_port}...\n")
    open_ports = []
    service_info = {}
    ports = range(start_port, end_port + 1)
    try:
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = {executor.submit(scan_port, target_ip, port, timeout=2): port for port in ports}
            total_ports = len(ports)
            last_percent = -1
            for idx, future in enumerate(as_completed(futures), 1):
                port = futures[future]
                result = future.result()
                percent = int((idx / total_ports) * 100)
                if percent != last_percent:
                    print(f"\rScanning: {percent}% complete", end='', flush=True)
                    last_percent = percent
                if result:
                    open_ports.append(result)
            print("\rScanning: 100% complete\n")
        print_scan_header(target, target_ip)
        if open_ports:
            for port in sorted(open_ports):
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(2)
                        s.connect((target_ip, port))
                        try:
                            banner = s.recv(1024).decode(errors='ignore').strip()
                        except Exception:
                            banner = ''
                        service_info[port] = banner if banner else "unknown"
                except Exception:
                    service_info[port] = "unknown"
            format_port_table(service_info)
        else:
            print("No open ports found.")
        print(f"\nScan completed at: {datetime.now()}")
        print("-" * 60)
        # OS Detection as part of advanced scan
        print("\nOS Detection Results:")
        print("-" * 60)
        try:
            ping_cmd = ["ping", "-c", "1", target_ip] if platform.system() != "Windows" else ["ping", "-n", "1", target_ip]
            output = subprocess.check_output(ping_cmd, stderr=subprocess.DEVNULL).decode()
            ttl_match = re.search(r"ttl[=|:](\d+)", output, re.IGNORECASE)
            if not ttl_match:
                print("Could not determine TTL from ping response.")
            else:
                ttl = int(ttl_match.group(1))
                if ttl <= 64:
                    os_guess = "Linux/Unix"
                elif ttl <= 128:
                    os_guess = "Windows"
                elif ttl <= 255:
                    os_guess = "Cisco/Networking Device"
                else:
                    os_guess = "Unknown OS"
                print(f"Guess based on TTL ({ttl}): {os_guess}")
        except subprocess.CalledProcessError:
            print("Ping failed. Cannot detect OS.")
        except Exception as e:
            print(f"OS detection error: {e}")
        print("-" * 60)
    except KeyboardInterrupt:
        print("\nExiting Program.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

# Title
print(pyfiglet.figlet_format("ninjasweep", font="slant"))
print("Author: SnipeAB\n")

# Argument handling
args = sys.argv[1:]
enable_advanced = False
if '-A' in args:
    enable_advanced = True
    args.remove('-A')

if len(args) < 1 or len(args) > 3:
    print("Invalid number of arguments.")
    print_usage()
    sys.exit(1)

target = args[0]
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print(f"Could not resolve host: {target}")
    sys.exit(1)

try:
    start_port = int(args[1]) if len(args) >= 2 else 1
    end_port = int(args[2]) if len(args) == 3 else 10000
except ValueError:
    print("Start and end ports must be integers.")
    print_usage()
    sys.exit(1)

if start_port < 1 or end_port > 65535 or start_port > end_port:
    print("Invalid port range. Ports must be between 1 and 65535, and start_port <= end_port.")
    print_usage()
    sys.exit(1)

if enable_advanced:
    advanced_scan(target, target_ip, start_port, end_port)
else:
    ports = range(start_port, end_port + 1)
    open_ports = []
    try:
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = {executor.submit(scan_port, target_ip, port): port for port in ports}
            total_ports = len(ports)
            last_percent = -1
            for idx, future in enumerate(as_completed(futures), 1):
                port = futures[future]
                result = future.result()
                percent = int((idx / total_ports) * 100)
                if percent != last_percent:
                    print(f"\rScanning: {percent}% complete", end='', flush=True)
                    last_percent = percent
                if result:
                    open_ports.append(result)
            print("\rScanning: 100% complete\n")
        print_scan_header(target, target_ip)
        if open_ports:
            service_info = {port: "unknown" for port in open_ports}
            format_port_table(service_info)
        else:
            print("No open ports found.")
        print(f"\nScan completed at: {datetime.now()}")
        print("-" * 60)
    except KeyboardInterrupt:
        print("\nExiting Program.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
