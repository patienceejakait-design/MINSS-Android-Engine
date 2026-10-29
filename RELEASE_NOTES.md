# MINSS Android Engine V5.1 Debug — Release Candidate

## Included
- Windows launcher/bridge source (`minss.py`)
- Windows startup script (`run_minss.bat`)
- Project documentation and license

## Capabilities
- Detect or manually select Android Emulator and ADB executables
- List configured virtual devices
- Launch a selected virtual device with a lightweight test configuration
- View ADB devices and install APKs
- Save selected tool paths and write a diagnostic log

## Known limitations
- Android SDK, emulator binaries, system images, Google Play components, and game APKs are not included.
- Boot success and performance depend on the host computer, SDK configuration, Android image, and virtualization setup.
- The lightweight memory setting is experimental and is not a guaranteed compatibility fix.

## Before calling this a stable release
- Test on a clean Windows setup.
- Confirm all third-party component licenses and distribution requirements.
- Include screenshots from the actual working build.
- Keep debug logs free of personal paths or other private information before sharing them.
