TOut pourri encore

# XPlane-Haptic-Interface

This repository gathers two independent projects developed during my engineering internship. Both interact with the X-Plane flight simulator:

- 🧠 A **Python program** that retrieves real-time flight data from X-Plane and triggers haptic feedback using the **bHaptics TactSuit X40**.
- ✈️ A **C++ plugin** for X-Plane that displays an interactive window with buttons to trigger failures, adjust weather, or test control surfaces.

---


# 🔧 Contents

## 1. `python_interface/`

A Python application using:

- `xplaneconnect` to communicate with X-Plane
- `pygame` and `pygame_widgets` to build a GUI
- `multiprocessing` to handle real-time data and feedback
- `bHaptics` SDK to send vibration patterns

**Features:**
- Displays real-time flight data
- Sends vibrations based on pitch, roll, altitude, or yaw rate
- Helps pilots fight spatial disorientation in simulator training

### 📸 GUI Example

<p align="center">
   <img src="images/GUI_py.png" alt="Python GUI" width="850"/>
</p>
*Real-time data from X-Plane with attitude visualisation.*

### 📸 Vest Feedback Zones

<p align="center">
   <img src="images/vestfront_diagram.png" alt="Vest diagram" width="400"/>
   <img src="images/vestback_diagram.png" alt="Vest diagram" width="400"/>
</p>
*bHaptics TactSuit x40 tactors index. Front on the left, back on the right*

---

## 2. `xp_plugin/`

A plugin for X-Plane (written in C++) using the XPLM SDK:

- Opens a custom window inside X-Plane
- Provides buttons to:
  - Reset all failures
  - Inject various weather conditions
  - Disable control surfaces (rudder, elevator, ailerons, etc.)

### 📸 Plugin Window
<p align="center">
   <img src="images/controlpanel_xp.png" alt="XPlane control panel" width="400"/>
</p>
*Custom window inside X-Plane with interactive controls.*

---

# 🏁 How to use

## Software
- Windows 10/11
- Python 3.13.5
- Visual studio code (recommended)
- Microsoft visual studio (recommended)
- [bHaptics player](https://www.bhaptics.com/software/player/)
- XPlane 11/12 (tested)

## Requirements

All the librairies needed are listed in [requirements.txt](/python_interface/requirements.txt).
```bash
keyboard==0.13.5
pybind11==3.0.0
pygame==2.6.1
pygame_widgets==1.2.2
setuptools==80.8.0
websocket_client==0.57.0

tactcombine==0.1
```
### Standard librairies
You can install all the standard python libraries with :

```bash
pip install keyboard==0.13.5 pybind11==3.0.0 pygame==2.6.1 pygame_widgets==1.2.2 setuptools==80.8.0 websocket_client==0.57.0
```
### Custom librairy
Since `tactcombine` is a custom library, you will need to build it manually from the `python_interface/combine/` directory using pybind11 :

```bash
pip install ./python_interface/combine
```
The library will be added to your python PATH.

(A [precompiled version of the tactcombine library](/python_interface/combine/tactcombine.cp313-win_amd64.pyd) is also included for Windows. This allows immediate use without requiring compilation.)

### Local SDK/plugin
You will also need the following dependencies :
- [XPlane connect Plugin](/python_interface/libs/xpc)
- [bHaptics python SDK](/python_interface/libs/bhaptics/)

## Python Program
1. The bHaptics player needs to be launched first
2. Connect the TactSuit and launch XPlane
3. Run the [main program](/python_interface/main.py)

   ```bash
   python main.py
   ```

## X-Plane Plugin
You can either use the [pre-compiled plugin](/Control_panel_XP/plugin_output/plugin/control_panel/) and put it into (for example) :
  ```
   C:\X-Plane 12\Resources\plugins
  ```

  Or you can edit the [source code](/Control_panel_XP/control_panel.cpp) and compile it yourself :
1. Build the plugin using a C++ compiler with the [XPlane SDK](/Control_panel_XP/SDK/)
2. Copy the compiled folder with the `.xpl` and `.pdb`files into:
   ```
   X-Plane/Resources/plugins/XPlaneInterface/
   ```
3. Launch X-Plane and activate the plugin from the





# 📁 Folder Structure

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

# 👨‍🔬 Author

**Pierre Bourrandy**
Engineering student in Mechatronics – ENSIL-ENSCI
2025 Internship Project – Australia

---

# 📜 License

This project is intended for academic and personal demonstration purposes.
For commercial or extended use, please contact the author.
