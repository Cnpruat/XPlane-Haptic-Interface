# XPlane-Haptic-Interface

This repository gathers two independent projects developed during my engineering internship. Both interact with the X-Plane flight simulator:

- 🧠 A **Python program** that retrieves real-time flight data from X-Plane and triggers haptic feedback using the **bHaptics TactSuit X40**.
- ✈️ A **C++ plugin** for X-Plane that displays an interactive window with buttons to trigger failures, adjust weather, or test control surfaces.

---

## 🔧 Contents

### 1. `python_interface/`

A Python application using:

- `xplaneconnect` to communicate with X-Plane
- `pygame` and `pygame_widgets` to build a GUI
- `multiprocessing` to handle real-time data and feedback
- `bHaptics` SDK to send vibration patterns

**Features:**
- Displays real-time flight data
- Sends vibrations based on pitch, roll, altitude, or yaw rate
- Helps pilots fight spatial disorientation in simulator training

#### 📸 GUI Example

![Pitch and Roll Feedback](images/gui_pitch_roll.png)  
*Real-time data from X-Plane with attitude visualisation.*

#### 📸 Vest Feedback Zones

![VestFront Diagram](images/vestfront_diagram.png)  
![VestBack Diagram](images/vestback_diagram.png) 
*Example of vibration zones activated on the TactSuit X40.*

---

### 2. `xp_plugin/`

A native plugin for X-Plane (written in C++) using the XPLM SDK:

- Opens a custom window inside X-Plane
- Provides buttons to:
  - Reset all failures
  - Inject various weather conditions
  - Disable control surfaces (rudder, elevator, ailerons, etc.)
- Fully compatible with X-Plane 11 and 12

#### 📸 Plugin Window

![X-Plane Plugin Window](images/xp_plugin_window.png)  
*Custom window inside X-Plane with interactive controls.*

---

## 🏁 How to Run

### Python Program
1. Install requirements:
   ```bash
   pip install pygame pygame_widgets xplaneconnect
   ```
2. Connect your TactSuit and X-Plane simulator
3. Launch the GUI:
   ```bash
   python main.py
   ```

### X-Plane Plugin
1. Build the plugin using a C++ compiler with the XPLM SDK
2. Copy the compiled `.xpl` plugin into:
   ```
   X-Plane/Resources/plugins/XPlaneInterface/
   ```
3. Launch X-Plane and activate the plugin from the **Plugins** menu

---

## 📁 Folder Structure

```
XPlane-Haptic-Interface/
│
├── python_interface/     ← Python GUI + haptic integration
├── xp_plugin/            ← C++ plugin using XPLM SDK
├── images/               ← Screenshots and diagrams for README
├── .gitignore
└── README.md             ← This file
```

---

## 👨‍🔬 Author

**Pierre Bourrandy**  
Engineering student in Mechatronics – ENSIL-ENSCI  
2025 Internship Project – Australia 🇦🇺

---

## 📜 License

This project is intended for academic and personal demonstration purposes.  
For commercial or extended use, please contact the author.
