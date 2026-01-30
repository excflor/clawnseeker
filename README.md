# 🦅 ClawnSeeker

**ClawnSeeker** is a high-performance, low-level hardware emulation dashboard built for Windows. It utilizes a dedicated driver-level interaction layer to simulate human-like HID (Human Interface Device) inputs with micro-precision.



## ✨ Key Features
* **Driver-Level Emulation:** Uses the `interception` framework for OS-level stealth.
* **Visual Analysis Zone:** Capture and monitor specific screen regions in real-time.
* **Dual-Action Logic:** Support for primary loops and secondary "Cheer" sequences.
* **Profile Management:** Save and hot-swap configurations for different environments.
* **Modern Dashboard UI:** A high-end, side-by-side Dark Mode interface.

## 🚀 Getting Started

### Prerequisites
1.  **Python 3.11+** (Tested on 3.13)
2.  **Interception Driver:** You must have the Interception driver installed on your Windows system for the HID emulation to function.
3.  **Administrator Rights:** The application must be run as Administrator to interact with the driver.

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/YourUsername/ClawnSeeker.git](https://github.com/YourUsername/ClawnSeeker.git)
   cd ClawnSeeker
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the application:
   ```bash
   python src/main.py

## 🛠️ Build Instructions (Standalone EXE)
To compile the project into a stealthy, single-file executable, run the provided build script in your terminal:
    ```batch
    build.bat
The resulting .exe will be located in the dist/ folder with the custom icon embedded. The build process utilizes Nuitka for advanced anti-tamper benefits and increased execution speed.

## 📂 Project Structure

## 🛡️ Stealth & Security
ClawnSeeker is designed with a "Security-First" mindset:

Humanized Delays: Implements Gaussian-style randomization for input intervals.

Non-Invasive Vision: Uses Desktop Duplication API for screen capture, avoiding game hooks.

Driver HID: Inputs are indistinguishable from physical hardware at the OS level.

## ⚖️ Disclaimer
This software is provided for educational and research purposes only. The authors are not responsible for any misuse, account bans, or violations of third-party Terms of Service. Use at your own risk.