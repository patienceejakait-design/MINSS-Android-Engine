MINSS ANDROID ENGINE V5.1 DEBUG
===============================
This is a diagnostic launcher/bridge. It is NOT a complete Android runtime and does not include the Android SDK.

WHAT'S NEW
- Browse manually to emulator.exe and adb.exe if MINSS cannot find them.
- Saves selected paths in minss_config.json.
- Logs output and errors to minss_debug.log.
- More visible startup checks and boot exit codes.
- Uses a 768 MB guest RAM test setting; this may or may not boot and is not a guaranteed fix.

START
1. Extract the ZIP to a normal writable folder.
2. Double-click run_minss.bat.
3. Click Browse for emulator.exe and select the emulator.exe inside your Android SDK's emulator folder if auto-detection fails.
4. Click Browse for adb.exe and select platform-tools\adb.exe if auto-detection fails.
5. Click List virtual devices, select a device, then Boot selected (Lite).
6. If it fails, click Open debug log and share the log contents/screenshot.

IMPORTANT
- Do not run multiple emulator instances at once.
- 4 GB total RAM and an HDD may be insufficient for modern Android images. A lower guest RAM setting does not guarantee Android will boot.
- If Android hangs at Google logo, the emulator console/log output is needed to identify the cause. Do not use Wipe Data unless you accept losing data in that virtual device.
- Only install APKs from trusted sources.
