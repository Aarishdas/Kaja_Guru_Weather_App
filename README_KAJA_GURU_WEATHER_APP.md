# Kaja Guru Weather App

Kaja Guru Weather App is a lightweight Windows weather application created by Aarish G. Das (@Aarishdas). It combines worldwide weather forecasts, personalized local AI guidance, multilingual options, themes, notifications, and privacy-focused local storage in one desktop app.

## What the app provides

- Current weather for cities around the world
- Three-day daily and hourly forecasts
- City and country autocomplete
- Temperature, feels-like temperature, humidity, wind, rain, pressure, and UV information
- Local AI guidance for rain, clothing, outdoor plans, travel, and storm awareness
- A personalized user profile and customizable AI assistant name
- Daily Windows and in-app weather notifications
- Permanent, Normal, and Temporary storage modes
- Multiple color themes and lightweight animations
- Adjustable weather-cache memory from 50 MB to 500 MB
- English, Hindi, Bengali, Spanish, French, and German options
- Protected API-key storage for the current Windows user

## Before using the app

The app requires Windows, an internet connection, and a valid WeatherAPI key. Users can create a key through the official [WeatherAPI signup page](https://www.weatherapi.com/signup.aspx).

Every user or publisher is responsible for following the conditions of their selected WeatherAPI plan. A real API key should never be posted publicly or shared inside a public GitHub repository.

## First launch

On a completely fresh installation, the app opens in this order:

1. Read and accept the weather, AI, and third-party disclaimer.
2. Choose Permanent, Normal, or Temporary storage.
3. Create a profile using a display or real name, an AI assistant name, and a home city.
4. Open Settings and enter a WeatherAPI key.
5. Search for a city to load the first forecast.

The name field is for a display or real name. It is not an email or password field.

## How to use the weather screen

Enter a city, region, postcode, or supported location in the search field. Matching cities and countries appear in the suggestion list. Select a result and press Search.

The main weather card shows the location, local date and time, temperature, condition, humidity, wind, rain, pressure, and UV level. Use the Daily Forecast tab for day-by-day information and the Hourly Forecast tab for detailed time-based predictions.

The temperature selector can switch between Celsius and Fahrenheit without restarting the app.

## Using the local AI assistant

The assistant can respond to greetings and weather-related questions. Examples include questions about rain, umbrellas, clothing, travel conditions, storms, outdoor plans, and the best time to go outside.

The AI feature is rule-based and analyzes information returned by the weather service. It is not a professional meteorologist and can provide an incorrect answer. Important decisions must always be checked with official government weather and emergency services.

## Storage modes

| Mode | What it remembers | Restart behavior |
|---|---|---|
| Permanent | Saves the profile, protected API key, settings, language, and recent weather cache. It can start with Windows. | Two English confirmations are required. Saved data remains after restart. |
| Normal | Saves information until Delete All App Data is used. It does not automatically start with Windows. | Two English confirmations are required. Saved data remains after restart. |
| Temporary | Keeps information only for the current app session. | Restart clears the session and returns to the starting disclaimer. |

The title-bar X always fully closes the application. Automatic refreshes and notifications work only while the app is running.

## Restarting the app

Restart App is available from the main weather screen and Settings. Restarting always requires two separate English confirmations to prevent accidental restarts.

Permanent and Normal modes keep their saved information. Temporary mode removes its session information and opens from the starting disclaimer again.

## Checking for updates

Open Settings, enter the public GitHub repository in `owner/repository` format, and select **Check for Updates**. The app compares its installed version with the newest published GitHub Release. If the installed version is current, it displays an up-to-date message. If a newer verified package exists, the packaged Windows app downloads it, quietly restarts, installs it, and opens the updated version.

The update system does not ask for or store a GitHub password or access token. The release repository must be public.

Each update must be published as a normal GitHub Release with a version tag newer than the version inside the app, such as `v4.4.1`. The Release must include these two assets with the exact names shown:

- `Kaja-Guru-Weather-App-Windows.zip`
- `Kaja-Guru-Weather-App-Windows.zip.sha256`

The ZIP must contain the complete Windows package, including `Kaja Guru Weather App.exe` and its required internal files. The checksum file must contain the ZIP file's 64-character SHA-256 value. An update is rejected if either asset is missing, the ZIP is unsafe, or the checksum does not match.

## Delete All App Data

Delete All App Data requires two confirmations. After confirmation, the app immediately starts removing the profile, protected API key, settings, recent locations, weather cache, language selection, and storage-mode selection.

Deletion runs in the background so the interface does not freeze. While a large cache is being removed, the app displays a progress message explaining that the starting disclaimer may take a little time to open. As soon as deletion finishes, the disclaimer opens inside the same running process. The entire application does not need to restart.

If the user tries to close the app while deletion is still running, the app asks them to wait until the starting disclaimer appears.

## Languages

The app includes options for English, Hindi, Bengali, Spanish, French, and German. The selected language changes the main onboarding, navigation, and settings text. Weather conditions are requested using WeatherAPI's supported language option.

The complete legal disclaimer remains in English so its intended wording is not changed by an automatic or informal translation.

## Themes and animations

Themes can be changed instantly without restarting. Available designs include Kaja Blue, Midnight, Aurora, Ocean, Forest, Sunset, Royal, Cherry, Cobalt, Emerald, Amber, Rose, Neon, Lavender, Matrix, and Graphite.

Animations are lightweight and can be disabled in Settings.

## Notifications

Users can enable a daily forecast notification and select the notification time. Test Notification displays an immediate test message. The app includes an animated in-app notification fallback if a native Windows notification cannot be displayed.

Windows Focus Assist, notification permissions, internet problems, or third-party service failures may prevent a notification from appearing.

## Weather-cache memory

The weather-cache limit can be set to 50, 100, 200, 300, 400, or 500 MB. This is a maximum limit, not an amount that is allocated immediately. Old weather responses are automatically removed after a short period.

The cache setting does not change the installed application size.

## Compact package design

The app is designed for a compact Windows package. It uses Python's standard library for the interface, networking, local storage, encryption, and Windows integration. Native notification support is optional and lightweight. No large AI model or offline weather dataset is included in the package.

The intended release target is below 100 MB. Final package size must be checked when the Windows release is actually built because it depends on the Python runtime, packaging-tool version, included logo, and notification components.

When the packaged release is prepared later, the application, required runtime components, and bundled Kaja Guru logo should be delivered together as one official release.

## Privacy and security

Profile information and settings stay on the Windows computer according to the selected storage mode. The API key is protected for the current Windows account using Windows Data Protection API.

City searches and weather requests are sent to WeatherAPI.com. Users should review WeatherAPI's privacy information and [service terms](https://www.weatherapi.com/terms.aspx).

## System requirements

- Windows 10 or Windows 11
- Internet access for forecasts and city search
- A valid WeatherAPI key
- Windows notifications enabled if native alerts are desired
- Enough free local space for the selected cache limit

## Troubleshooting

If weather does not load, check the internet connection, confirm that the API key is valid, and verify that the WeatherAPI plan is active. If city suggestions do not appear, type at least two characters and wait briefly for results.

If notifications do not appear, check Windows notification permissions and Focus Assist, then use Test Notification in Settings.

If the app is slow immediately after deleting a large cache, wait for the deletion progress message to finish. The starting disclaimer will open automatically.

## Important disclaimer

Weather forecasts and local AI suggestions may be delayed, incomplete, unavailable, or incorrect. Never use this application as the only source for emergency planning, aviation, maritime work, medical decisions, dangerous travel, property protection, agriculture, or other safety-critical decisions.

Always verify important information with official government weather departments, emergency services, and qualified professionals.

## Copyright and third-party services

Copyright (c) 2026 Aarish G. Das (@Aarishdas). All rights reserved.

This application source code is not offered under an open-source license. Permission is not granted to copy, modify, distribute, sublicense, or sell the source without written authorization from the copyright owner.

Python, Tkinter, optional notification components, and WeatherAPI remain subject to their own licenses or service terms. Those third-party rights are not replaced by this application's copyright notice.
