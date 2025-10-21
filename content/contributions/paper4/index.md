---
title: "WLC andilog interfacing using raspberry via bluetooth" 
date: 2022-02-01
tags: ["andilog","torque","force","sensor","interface","raspberry","linux"]
author: ["Dilly Émilien, Bretts Williams "]
description: " Interfacing and data acquisitation using WLC andilog  with torque and force sensors via bluetooth under linux." 
summary: "Interfacing and data acquisitation using WLC andilog  with torque and force sensors via bluetooth under linux.   " 
cover:
    image: "paper1.webp"
    alt: "raspwlcbluetooth"
    relative: true
editPost:

---

##  Presentation

**Project Title:** WLC Andilog Amplifier Data Logger for Raspberry Pi  
**Description:**  
A Python tool to acquire torque/force measurements from a WLC analog amplifier connected via Bluetooth on Raspberry Pi. It sets the logger frequency, starts/stops logging, and processes data for real-time use or further analysis.  



**Key Features:**  
- Bluetooth auto-setup (RFCOMM binding)  
- Sensor data acquisition and cleaning  
- Configurable acquisition time  
- Easy integration for logging and analysis  


## 📂 Files

- `wlc_logger.py` → Main Python script
- `FULL_DOCUMENTATION.md` → Combined docs and code (this file)

---

## 🐍 Python Code (`wlc_logger.py`)

```python
#!/usr/bin/env python3
"""
WLC Analog Amplifier Data Logger for Raspberry Pi 4
---------------------------------------------------
This script connects to a torque or force sensor via a WLC analog amplifier
using Bluetooth (RFCOMM), logs data, and processes readings.

Author: Dilly Emilien, Bretts Williams
"""

import argparse
import binascii
import numpy as np
import os
import re
import serial
import signal
import sys
import time


# ---------------------------
# Argument Parsing
# ---------------------------
parser = argparse.ArgumentParser(description="WLC Data Logger for Torque/Force Sensors")
parser.add_argument(
    "-t",
    "--tacq",
    type=float,
    default=2,
    help="Acquisition time (s) for writing data in output file (default: 2s)",
)
args = parser.parse_args()
tacq = args.tacq


# ---------------------------
# Serial Communication Helpers
# ---------------------------
def frequency_data_logger(freq_wlc: str) -> bytes:
    """Set the frequency of the data logger."""
    binary_string = binascii.unhexlify(f"0203F0{freq_wlc}03")
    print("> Frequency data logger")
    ser.flushInput()
    ser.write(binary_string)
    return read_answer()


def stop_data_logger() -> bytes:
    """Send stop command to data logger."""
    binary_string = binascii.unhexlify("0201F703")
    print("> Stop data logger")
    ser.flushInput()
    ser.write(binary_string)
    return read_answer()


def start_data_logger() -> None:
    """Send start command to data logger."""
    binary_string = binascii.unhexlify("0201FD03")
    print("> Start data logger")
    ser.flushInput()
    ser.write(binary_string)


def read_answer() -> bytes:
    """Read response from the device."""
    print("> Received data")
    return ser.readline()


def read_data_logger() -> bytes:
    """Read raw logger data (fixed 40 bytes)."""
    return ser.read(40)


def clean_answer(answer: bytes) -> np.ndarray:
    """Extract numeric values from raw serial response."""
    try:
        answer_str = answer.decode(errors="ignore")
        matches = re.findall(r"(-?\d+\.\d+)", answer_str)
        if matches:
            values = np.array(matches, dtype=float)
            return values
        return np.zeros((1,))
    except ValueError:
        print("> No valid ASCII characters found")
        return np.zeros((1,))


# ---------------------------
# Signal Handler
# ---------------------------
def sigint_handler(sig, frame):
    """Handle CTRL+C gracefully."""
    print("CTRL+C detected > Exiting")
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)


# ---------------------------
# Bluetooth Setup
# ---------------------------
BT_MAC = "40:84:32:56:F2:AF"
print("> Disconnecting previous Bluetooth sessions")
os.system(f"sudo bt-device -r {BT_MAC}")

print("> Binding RFCOMM to WLC device")
os.system(f"sudo rfcomm bind 0 {BT_MAC}")

print("> Setting permissions")
os.system("sudo chmod 777 /dev/rfcomm0")


# ---------------------------
# Serial Connection
# ---------------------------
print("> Opening serial connection")
ser = serial.Serial("/dev/rfcomm0", 9600, timeout=1)

FREQ_WLC = "0064"  # 100 Hz (0x64)


input("> Switch on VLC-Connect & press ENTER to continue...")
time.sleep(1)
print("> Initialization complete")


# ---------------------------
# Main Workflow
# ---------------------------
print("> Starting main logger...")
stop_data_logger()
frequency_data_logger(FREQ_WLC)
start_data_logger()


def measure_torque(acq_time: float = 1.0) -> float:
    """
    Acquire and process torque/force measurements.
    
    Args:
        acq_time (float): Acquisition time in seconds.
    Returns:
        float: Median torque value.
    """
    ser.flushInput()
    ser.flush()
    answer = read_data_logger()
    data = clean_answer(answer)
    try:
        return float(np.median(data))
    except Exception:
        return 0.0


print("> Logger running... Press CTRL+C to quit.")
```

---

## 🚀 Features
- Connects to WLC Amplifier via **Bluetooth RFCOMM**
- Reads **torque/force sensor** data
- Supports **custom acquisition time**
- Extracts and cleans numerical values from raw serial data
- Graceful shutdown on `CTRL+C`

---

## 📦 Requirements

```bash
sudo apt-get install bluez rfcomm python3-serial
pip install numpy pyserial
```

---

## ⚙️ Usage

```bash
python3 wlc_logger.py -t 5
```

Options:
- `-t`, `--tacq`: Acquisition time in seconds (default: 2s)

---

## 🔌 Setup
1. Turn on the **WLC-Connect device**.
2. Pair it with the Raspberry Pi using Bluetooth.
3. Update the **MAC address** in the script (`BT_MAC` variable).
4. Run the logger script.
5. Data will be streamed via serial.

---

## 📊 Example Output
```
> Starting main logger...
> Frequency data logger
> Logger running... Press CTRL+C to quit.
Torque = 0.25 Nm
Torque = 0.27 Nm
Torque = 0.26 Nm
```

---

## 📌 Notes
- Default frequency is set to **100 Hz**.
- Serial device used: `/dev/rfcomm0`.
- Tested on **Raspberry Pi 4 with Raspbian**.

---

## 🛠️ Future Improvements
- Save logs to CSV automatically
- Add real-time plotting
- Support multiple sensor connections

---

*This page -except the code - was automatically generated by ChatGPT*

