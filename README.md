# MINSS Android Engine — V5.1 Debug

A Windows launcher/bridge for an Android Emulator installation. MINSS helps locate the Android Emulator and ADB tools, list configured Android Virtual Devices (AVDs), launch a selected AVD with a lightweight test configuration, inspect connected ADB devices, and install APK files.

> **Important:** MINSS is not a standalone Android operating system or emulator. It does not bundle the Android SDK, emulator system images, Google Play Store, or BUSSID. Those are provided by the Android SDK/emulator installation and the configured virtual device. Performance depends on the host PC and selected Android image.

## Features

- Dark interface with neon-green MINSS branding
- Automatic and manual selection of `emulator.exe` and `adb.exe`
- List configured Android Virtual Devices
- Launch a selected virtual device using a lightweight test configuration
- Check ADB-connected devices
- Install an APK to a running, connected Android device
- Save selected tool paths in `minss_config.json`
- Write diagnostics to `minss_debug.log`

## Requirements

- Windows
- Python 3
- Android SDK Emulator and a configured Android Virtual Device
- Android SDK Platform-Tools (ADB)
- Enough RAM, storage, and CPU capability for the chosen Android system image

The launcher itself is lightweight, but the Android Emulator can be demanding. PCs with 4 GB RAM and a hard-disk drive may struggle with modern Android images. A 768 MB guest-memory setting is only a test configuration and is not a guarantee that Android will boot or run smoothly.

## Run from source

1. Extract this project to a writable folder.
2. Install Python 3 if it is not already installed.
3. Double-click `run_minss.bat`.
4. If the tools are not detected automatically, use **Browse for emulator.exe** and select it from the Android SDK's `emulator` folder.
5. Use **Browse for adb.exe** to select `platform-tools\adb.exe`.
6. Click **List virtual devices**, select a device, then click **Boot selected (Lite)**.
7. Once Android is running, use **Refresh ADB devices** and **Install APK** as needed.
8. If something fails, use **Open debug log** and review `minss_debug.log`.

## Troubleshooting

- **No virtual devices listed:** Create an Android Virtual Device in the Android SDK first.
- **Emulator not found:** Browse to the actual `emulator.exe` file in your SDK installation.
- **ADB does not show a device:** Start the virtual device and then refresh ADB devices.
- **Android hangs at the boot logo:** Check the debug log and emulator output. Do not use **Wipe Data** unless you accept losing data stored in that virtual device.
- **APK installation fails:** Confirm the device is fully booted and that the APK is compatible with its Android version and CPU architecture.

Install APK files only from sources you trust.

## Project status

This is a **V5.1 Debug release candidate**, not a claim of a standalone emulator. Before tagging a stable release, test the packaged project on a clean Windows account or a second PC and record the Windows version, Python version, Android Emulator version, AVD/system-image details, and the result of installing and launching a test APK and BUSSID.

## License

See `LICENSE.txt`.
