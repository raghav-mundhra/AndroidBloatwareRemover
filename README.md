# AndroidBloatwareRemover

This application can be used to disable unwanted bloatwares which comes pre-installed with the OEMs and cannot be uninstalled directly from the device. This application do not require any root access.

## Pre-requisites:
1. A PC with Python 3.x installed on it.
2. Developer options should be enabled on mobile phone.
3. USB Debugging in Developer options should be enabled.

## Steps to use this application:
1. Connect your device to your PC with a USB cable (Make sure USB Debugging is enabled).
2. Execute the "main.py" file. A Popup will open.
3. Select your device id from the dropdown list and click "Select"
![Screenshot1](https://raw.githubusercontent.com/raghav-mundhra/AndroidBloatwareRemover/main/images/1.png)

4. The application will fetch all the apps installed on you mobile phone along with their package names and display them in a list.
5. Select the package (app) which you want to uninstall and click "Uninstall" button.
![Screenshot1](https://raw.githubusercontent.com/raghav-mundhra/AndroidBloatwareRemover/main/images/2.png)
6. Follow the onscreen instructions afterwards. The selected app will be uninstalled in few seconds.

## How to enable Developer options and USB Debugging:
1. Open "Settings" in your device.
2. Go to system settings/advance settings (this setting vary with different manufacturers).
3. Open device info and tap "Build number" 5-7 times. This will enable developer options.
4. Open "Developer Options".
5. Enable "USB Debugging".

**Note** : *This application do not deletes the bloatware/app from the ROM completely. It only removes it for the active user. The app data will still be in the ROM but it won't be able to execute and you cannot access it. All the functionalities and processes of that app will be removed. The device will "think" as if the app is uninstalled. This won't void your warranty and you will still be able to receive OTA updates from your device manufacturer. A pre-installed bloatware can be uninstalled completely with root privileges  only.*
