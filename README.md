
# 🥷 ninjasweep — Python Port Scanner 🛰️

Welcome to **ninjasweep**, a fast, sleek, and stealthy Python-based port scanner built for power and simplicity!  
Whether you're exploring your own network or learning the ropes of cybersecurity, this tool's got your back 💻🔓

![banner](https://img.shields.io/badge/python-3.6%2B-blue?logo=python)
![License](https://img.shields.io/badge/license-MIT-green)
![Author](https://img.shields.io/badge/author-SnipeAB-informational)

---

## 🎯 Features

✅ Multi-threaded TCP port scanning (blazing fast ⚡)  
✅ Stealth SYN scan (`-S`) using Scapy for half-open scanning (requires root) 🥷  
✅ Banner grabbing for live service detection on open ports 🛠️  
✅ Nmap-style timing profiles (`-T0` to `-T5`) for flexible speed vs stealth ⏱️  
✅ Optional advanced scan mode `-A`:
   - OS fingerprinting via TTL 📡  
   - Deep banner inspection on live ports  
✅ Custom port range support  
✅ Cross-platform (Linux / Windows / MacOS)  
✅ No dependencies outside standard libraries + Scapy  
✅ Clean, modern terminal UI with progress tracking 📊  

---

## 📦 Requirements

- Python **3.6 or higher**
- **Scapy** for stealth scanning:  
  Install via pip:

  ```bash
  pip install scapy
  ```

- For stealth mode (`-S`), you **must run as root/admin**:

  - Linux/macOS: `sudo python3 ninjasweep.py ...`
  - Windows: Run your terminal as Administrator

---

## ⚙️ Usage

```bash
python3 ninjasweep.py <target> [start_port] [end_port] [options]
```

### 📘 Options

| Option      | Description                                      |
|-------------|--------------------------------------------------|
| `<target>`  | IP address or domain to scan                     |
| `start_port`| (Optional) Port to start scanning from (default: 1) |
| `end_port`  | (Optional) Port to stop scanning at (default: 10000) |
| `-A`        | Run advanced scan (OS detection + banners)       |
| `-S`        | Stealth SYN scan (half-open, root required)      |
| `-T<0-5>`   | Set timing profile (0 = slowest, 5 = fastest)    |

---

## 🚀 Examples

### Basic Scan (default ports 1–10000)
```bash
python3 ninjasweep.py scanme.nmap.org
```

### Scan custom range
```bash
python3 ninjasweep.py 192.168.1.1 20 1024
```

### Run stealth (SYN) scan with max stealth (`-T0`)
```bash
sudo python3 ninjasweep.py 192.168.1.1 -S -T0
```

### Advanced scan with OS detection & banners
```bash
python3 ninjasweep.py 192.168.1.1 1 1000 -A
```

---

## 🧠 Timing Profiles (`-T`)

| Profile | Description        | Threads | Delay  |
|---------|--------------------|---------|--------|
| `-T0`   | Paranoid (stealthy)| 1       | 5s     |
| `-T1`   | Sneaky             | 5       | 1s     |
| `-T2`   | Polite             | 20      | 0.4s   |
| `-T3`   | Normal (default)   | 100     | 0.05s  |
| `-T4`   | Aggressive         | 200     | 0.01s  |
| `-T5`   | Insane (max speed) | 500     | 0s     |

---

## 🔐 Legal Disclaimer

This tool is intended **only for educational and authorized testing** on networks you own or have permission to scan. Unauthorized scanning is illegal and unethical.

---

## 👨‍💻 Author

**SnipeAB**  
Twitter: [@snipeab](https://twitter.com/snipeab)  
GitHub: [github.com/snipeab](https://github.com/snipeab)

---

## 🧾 License

This project is licensed under the [MIT License](LICENSE)
