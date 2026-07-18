# Kaja Guru Weather App
# Copyright (c) 2026 Aarish G. Das
# GitHub: @Aarishdas
# All rights reserved.
#
# Concept, product design, selection, testing and modifications:
# Aarish G. Das
#
# Developed with AI assistance.
# No permission is granted to copy, modify, distribute or sell this
# source code without written permission from the copyright owner.
import base64
import ctypes
import hashlib
import json
import math
import os
import queue
import random
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import tkinter as tk
import webbrowser
import winreg
import zipfile

from ctypes import wintypes
from datetime import datetime
from tkinter import messagebox, simpledialog, ttk
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

try:
    from winotify import Notification, audio
except ImportError:
    Notification = None
    audio = None


APP_NAME = "Kaja Guru Weather App"
APP_VERSION = "4.4.0"

# Your original, self-made logo shown inside the app.
ORIGINAL_LOGO_PATH = (
    r"C:\Users\Aarish G. Das\Desktop\Kohinoor_OS\weather_app_icon.png"
)

API_BASE_URL = "https://api.weatherapi.com/v1"
API_SIGNUP_URL = "https://www.weatherapi.com/signup.aspx"
API_TERMS_URL = "https://www.weatherapi.com/terms.aspx"

# Set this to your public GitHub repository before distributing the app,
# for example: "your-github-name/your-repository-name".
DEFAULT_GITHUB_REPOSITORY = "Aarishdas/Kaja_Guru_Weather_App"
UPDATE_PACKAGE_NAME = "Kaja_Guru_Weather_App.zip"
UPDATE_CHECKSUM_NAME = UPDATE_PACKAGE_NAME + ".sha256"
MAX_UPDATE_DOWNLOAD_BYTES = 150 * 1024 * 1024
MAX_UPDATE_EXTRACTED_BYTES = 300 * 1024 * 1024

MIN_CACHE_MB = 50
DEFAULT_CACHE_MB = 100
MAX_CACHE_MB = 500
CACHE_LIFETIME = 55 * 60

LANGUAGE_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
}

TEXTS = {
    "English": {
        "language": "Language",
        "choose_storage": "Choose how this app should remember information on this computer.",
        "permanent": "Permanent",
        "normal": "Normal",
        "temporary": "Temporary",
        "permanent_desc": "Saves profile, protected API key, settings and cache. The app starts automatically with Windows.",
        "normal_desc": "Saves information until you manually use Delete All App Data in Settings.",
        "temporary_desc": "Keeps data only while the app is running. Closing or restarting removes session data.",
        "close_note": "The title-bar X fully closes the app. Restart keeps Permanent/Normal data, but Temporary restarts from the beginning.",
        "exit": "Exit",
        "disclaimer": "Disclaimer",
        "accept_disclaimer": "I have read and accept this disclaimer.",
        "accept_continue": "Accept and Continue",
        "accept_warning": "Please accept the disclaimer to continue.",
        "create_profile": "Create Your Profile",
        "profile_note": "This is your display profile. Do not enter a password.",
        "your_name": "Your display or real name",
        "name_hint": "Example: Aarish. Enter a name, not an email address.",
        "assistant_name": "Your AI assistant's name",
        "assistant_hint": "Default: Aira, pronounced EYE-rah.",
        "home_city": "Home city",
        "city_hint": "Example: Kolkata, Delhi, London or New York.",
        "create_button": "Create Profile",
        "hello": "Hello, {name}",
        "ready": "{app} - {assistant} is ready",
        "restart": "Restart App",
        "themes": "Themes",
        "settings": "Settings",
        "search": "Search",
        "daily": "Daily Forecast",
        "hourly": "Hourly Forecast",
        "ask": "Ask {assistant}",
        "cache_limit": "Weather cache memory limit (MB)",
        "refresh": "Refresh interval",
        "ai_mode": "Local AI prediction mode",
        "notify_time": "Daily notification time (24-hour HH:MM)",
        "enable_notify": "Enable daily weather notifications",
        "enable_animations": "Enable animations",
        "save": "Save",
        "test_notification": "Test Notification",
        "remove_key": "Remove API Key",
        "view_disclaimer": "View Disclaimer",
        "clear_cache": "Clear Weather Cache",
        "delete_all": "Delete All App Data",
        "exit_app": "Exit Application",
    },
    "Hindi": {
        "language": "भाषा",
        "choose_storage": "चुनें कि यह ऐप इस कंप्यूटर पर आपकी जानकारी कैसे याद रखे।",
        "permanent": "स्थायी",
        "normal": "सामान्य",
        "temporary": "अस्थायी",
        "permanent_desc": "प्रोफ़ाइल, सुरक्षित API कुंजी, सेटिंग और कैश सहेजता है। ऐप Windows के साथ शुरू होगा।",
        "normal_desc": "जानकारी तब तक सहेजी जाएगी जब तक आप Settings से Delete All App Data नहीं चुनते।",
        "temporary_desc": "डेटा केवल इस सत्र में रहता है। बंद या रीस्टार्ट करने पर सत्र डेटा मिट जाएगा।",
        "close_note": "X ऐप को पूरी तरह बंद करता है। स्थायी/सामान्य डेटा रीस्टार्ट पर रहेगा, अस्थायी मोड शुरुआत से खुलेगा।",
        "exit": "बाहर निकलें",
        "disclaimer": "अस्वीकरण",
        "accept_disclaimer": "मैंने अस्वीकरण पढ़ लिया है और स्वीकार करता/करती हूँ।",
        "accept_continue": "स्वीकार करें और आगे बढ़ें",
        "accept_warning": "आगे बढ़ने के लिए अस्वीकरण स्वीकार करें।",
        "create_profile": "अपनी प्रोफ़ाइल बनाएँ",
        "profile_note": "यह आपकी डिस्प्ले प्रोफ़ाइल है। पासवर्ड दर्ज न करें।",
        "your_name": "आपका नाम",
        "assistant_name": "आपके AI सहायक का नाम",
        "home_city": "गृह शहर",
        "create_button": "प्रोफ़ाइल बनाएँ",
        "hello": "नमस्ते, {name}",
        "ready": "{app} - {assistant} तैयार है",
        "restart": "ऐप रीस्टार्ट करें",
        "themes": "थीम",
        "settings": "सेटिंग्स",
        "search": "खोजें",
        "daily": "दैनिक पूर्वानुमान",
        "hourly": "प्रति घंटा पूर्वानुमान",
        "ask": "{assistant} से पूछें",
        "cache_limit": "मौसम कैश मेमोरी सीमा (MB)",
        "refresh": "रिफ्रेश अंतराल",
        "ai_mode": "स्थानीय AI पूर्वानुमान मोड",
        "notify_time": "दैनिक सूचना समय (HH:MM)",
        "enable_notify": "दैनिक मौसम सूचनाएँ चालू करें",
        "enable_animations": "एनिमेशन चालू करें",
        "save": "सहेजें",
        "test_notification": "सूचना जाँचें",
        "remove_key": "API कुंजी हटाएँ",
        "view_disclaimer": "अस्वीकरण देखें",
        "clear_cache": "मौसम कैश साफ़ करें",
        "delete_all": "सभी ऐप डेटा हटाएँ",
        "exit_app": "ऐप बंद करें",
    },
    "Bengali": {
        "language": "ভাষা",
        "choose_storage": "এই কম্পিউটারে অ্যাপটি কীভাবে তথ্য মনে রাখবে তা বেছে নিন।",
        "permanent": "স্থায়ী",
        "normal": "সাধারণ",
        "temporary": "অস্থায়ী",
        "permanent_desc": "প্রোফাইল, সুরক্ষিত API কী, সেটিংস ও ক্যাশ সংরক্ষণ করে এবং Windows-এর সঙ্গে চালু হয়।",
        "normal_desc": "Settings থেকে Delete All App Data না করা পর্যন্ত তথ্য সংরক্ষিত থাকবে।",
        "temporary_desc": "তথ্য শুধু এই সেশনে থাকবে। বন্ধ বা রিস্টার্ট করলে সেশন মুছে যাবে।",
        "close_note": "X অ্যাপ পুরোপুরি বন্ধ করে। স্থায়ী/সাধারণ ডেটা থাকবে, অস্থায়ী মোড শুরু থেকে খুলবে।",
        "exit": "প্রস্থান",
        "disclaimer": "দায়-অস্বীকার",
        "accept_disclaimer": "আমি দায়-অস্বীকারটি পড়েছি এবং গ্রহণ করছি।",
        "accept_continue": "গ্রহণ করে এগিয়ে যান",
        "create_profile": "প্রোফাইল তৈরি করুন",
        "your_name": "আপনার নাম",
        "assistant_name": "আপনার AI সহকারীর নাম",
        "home_city": "নিজের শহর",
        "create_button": "প্রোফাইল তৈরি করুন",
        "hello": "নমস্কার, {name}",
        "ready": "{app} - {assistant} প্রস্তুত",
        "restart": "অ্যাপ রিস্টার্ট",
        "themes": "থিম",
        "settings": "সেটিংস",
        "search": "খুঁজুন",
        "daily": "দৈনিক পূর্বাভাস",
        "hourly": "ঘণ্টাভিত্তিক পূর্বাভাস",
        "ask": "{assistant}-কে জিজ্ঞাসা করুন",
        "cache_limit": "আবহাওয়া ক্যাশ মেমরি সীমা (MB)",
        "save": "সংরক্ষণ",
        "test_notification": "নোটিফিকেশন পরীক্ষা",
        "clear_cache": "ক্যাশ পরিষ্কার করুন",
        "delete_all": "সব অ্যাপ ডেটা মুছুন",
        "exit_app": "অ্যাপ বন্ধ করুন",
    },
    "Spanish": {
        "language": "Idioma",
        "choose_storage": "Elige cómo debe recordar la información esta aplicación.",
        "permanent": "Permanente",
        "normal": "Normal",
        "temporary": "Temporal",
        "permanent_desc": "Guarda el perfil, la clave API protegida, los ajustes y la caché; se inicia con Windows.",
        "normal_desc": "Guarda la información hasta que selecciones Eliminar todos los datos.",
        "temporary_desc": "Conserva los datos solo durante la sesión. Cerrar o reiniciar elimina la sesión.",
        "close_note": "X cierra completamente la aplicación. El modo temporal vuelve al inicio al reiniciar.",
        "exit": "Salir",
        "disclaimer": "Aviso legal",
        "accept_disclaimer": "He leído y acepto este aviso legal.",
        "accept_continue": "Aceptar y continuar",
        "create_profile": "Crear perfil",
        "your_name": "Tu nombre",
        "assistant_name": "Nombre de tu asistente de IA",
        "home_city": "Ciudad de origen",
        "create_button": "Crear perfil",
        "hello": "Hola, {name}",
        "ready": "{app} - {assistant} está listo",
        "restart": "Reiniciar aplicación",
        "themes": "Temas",
        "settings": "Ajustes",
        "search": "Buscar",
        "daily": "Pronóstico diario",
        "hourly": "Pronóstico por hora",
        "ask": "Preguntar a {assistant}",
        "cache_limit": "Límite de memoria de caché (MB)",
        "save": "Guardar",
        "test_notification": "Probar notificación",
        "clear_cache": "Borrar caché",
        "delete_all": "Eliminar todos los datos",
        "exit_app": "Cerrar aplicación",
    },
    "French": {
        "language": "Langue",
        "choose_storage": "Choisissez comment l'application mémorise les informations.",
        "permanent": "Permanent",
        "normal": "Normal",
        "temporary": "Temporaire",
        "permanent_desc": "Enregistre le profil, la clé API protégée, les réglages et le cache; démarre avec Windows.",
        "normal_desc": "Enregistre les informations jusqu'à la suppression manuelle des données.",
        "temporary_desc": "Conserve les données uniquement pendant la session. Fermer ou redémarrer efface la session.",
        "close_note": "X ferme complètement l'application. Le mode temporaire revient au début après redémarrage.",
        "exit": "Quitter",
        "disclaimer": "Avertissement",
        "accept_disclaimer": "J'ai lu et j'accepte cet avertissement.",
        "accept_continue": "Accepter et continuer",
        "create_profile": "Créer votre profil",
        "your_name": "Votre nom",
        "assistant_name": "Nom de votre assistant IA",
        "home_city": "Ville de résidence",
        "create_button": "Créer le profil",
        "hello": "Bonjour, {name}",
        "ready": "{app} - {assistant} est prêt",
        "restart": "Redémarrer l'application",
        "themes": "Thèmes",
        "settings": "Paramètres",
        "search": "Rechercher",
        "daily": "Prévisions quotidiennes",
        "hourly": "Prévisions horaires",
        "ask": "Demander à {assistant}",
        "cache_limit": "Limite mémoire du cache météo (MB)",
        "save": "Enregistrer",
        "test_notification": "Tester la notification",
        "clear_cache": "Vider le cache",
        "delete_all": "Supprimer toutes les données",
        "exit_app": "Quitter l'application",
    },
    "German": {
        "language": "Sprache",
        "choose_storage": "Wählen Sie, wie die App Informationen auf diesem Computer speichert.",
        "permanent": "Dauerhaft",
        "normal": "Normal",
        "temporary": "Temporär",
        "permanent_desc": "Speichert Profil, geschützten API-Schlüssel, Einstellungen und Cache; startet mit Windows.",
        "normal_desc": "Speichert Informationen, bis alle App-Daten manuell gelöscht werden.",
        "temporary_desc": "Behält Daten nur während der Sitzung. Schließen oder Neustart löscht die Sitzung.",
        "close_note": "X schließt die App vollständig. Der temporäre Modus beginnt nach dem Neustart von vorn.",
        "exit": "Beenden",
        "disclaimer": "Haftungsausschluss",
        "accept_disclaimer": "Ich habe den Haftungsausschluss gelesen und akzeptiere ihn.",
        "accept_continue": "Akzeptieren und fortfahren",
        "create_profile": "Profil erstellen",
        "your_name": "Ihr Name",
        "assistant_name": "Name Ihres KI-Assistenten",
        "home_city": "Heimatstadt",
        "create_button": "Profil erstellen",
        "hello": "Hallo, {name}",
        "ready": "{app} - {assistant} ist bereit",
        "restart": "App neu starten",
        "themes": "Designs",
        "settings": "Einstellungen",
        "search": "Suchen",
        "daily": "Tagesvorhersage",
        "hourly": "Stündliche Vorhersage",
        "ask": "{assistant} fragen",
        "cache_limit": "Wetter-Cache-Speicherlimit (MB)",
        "save": "Speichern",
        "test_notification": "Benachrichtigung testen",
        "clear_cache": "Cache leeren",
        "delete_all": "Alle App-Daten löschen",
        "exit_app": "App beenden",
    },
}

APP_DATA = os.path.join(
    os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
    "KajaGuruWeatherApp",
)

SETTINGS_FILE = os.path.join(APP_DATA, "settings.json")
CACHE_DIRECTORY = os.path.join(APP_DATA, "weather_cache")


def bundled_resource(filename):
    base = getattr(
        sys,
        "_MEIPASS",
        os.path.dirname(os.path.abspath(__file__)),
    )
    return os.path.join(base, filename)


# The rounded transparent logo is bundled with the packaged application.
BUNDLED_LOGO_PATH = bundled_resource("weather_app_icon_rounded.png")

LOGO_PATH = (
    BUNDLED_LOGO_PATH
    if os.path.isfile(BUNDLED_LOGO_PATH)
    else ORIGINAL_LOGO_PATH
)


def normalize_github_repository(value):
    repository = str(value or "").strip()
    repository = re.sub(
        r"^https?://(?:www\.)?github\.com/",
        "",
        repository,
        flags=re.IGNORECASE,
    )
    repository = repository.strip().strip("/")

    if repository.lower().endswith(".git"):
        repository = repository[:-4]

    if not re.fullmatch(
        r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+",
        repository,
    ):
        raise ValueError(
            "Enter a public GitHub repository as owner/repository."
        )

    return repository


def version_key(value):
    numbers = [
        int(number)
        for number in re.findall(r"\d+", str(value or ""))[:4]
    ]
    numbers.extend([0] * (4 - len(numbers)))
    return tuple(numbers)


def read_github_latest_release(repository):
    url = (
        "https://api.github.com/repos/"
        f"{repository}/releases/latest"
    )
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": f"Kaja-Guru-Weather-App/{APP_VERSION}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )

    with urlopen(request, timeout=25) as response:
        payload = response.read(2 * 1024 * 1024 + 1)

    if len(payload) > 2 * 1024 * 1024:
        raise WeatherError("The GitHub release response was too large.")

    release = json.loads(payload.decode("utf-8"))
    if not isinstance(release, dict):
        raise WeatherError("GitHub returned an invalid release response.")

    return release


def download_update_file(url, destination):
    temporary = destination + ".part"
    os.makedirs(os.path.dirname(destination), exist_ok=True)

    try:
        request = Request(
            url,
            headers={
                "Accept": "application/octet-stream",
                "User-Agent": f"Kaja-Guru-Weather-App/{APP_VERSION}",
            },
        )

        with urlopen(request, timeout=30) as response:
            declared_size = response.headers.get("Content-Length")
            if (
                declared_size
                and int(declared_size) > MAX_UPDATE_DOWNLOAD_BYTES
            ):
                raise WeatherError(
                    "The update package is larger than the allowed limit."
                )

            total = 0
            with open(temporary, "wb") as output:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break

                    total += len(chunk)
                    if total > MAX_UPDATE_DOWNLOAD_BYTES:
                        raise WeatherError(
                            "The update package is larger than the "
                            "allowed limit."
                        )

                    output.write(chunk)

        os.replace(temporary, destination)
    finally:
        if os.path.isfile(temporary):
            try:
                os.remove(temporary)
            except OSError:
                pass


def file_sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as file:
        while True:
            chunk = file.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def safely_extract_update(zip_path, destination):
    destination = os.path.abspath(destination)
    os.makedirs(destination, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as archive:
        extracted_size = sum(
            max(0, member.file_size)
            for member in archive.infolist()
        )
        if extracted_size > MAX_UPDATE_EXTRACTED_BYTES:
            raise WeatherError(
                "The extracted update is larger than the allowed limit."
            )

        for member in archive.infolist():
            member_path = os.path.abspath(
                os.path.join(destination, member.filename)
            )

            try:
                inside_destination = (
                    os.path.commonpath([destination, member_path])
                    == destination
                )
            except ValueError:
                inside_destination = False

            unix_file_type = (member.external_attr >> 16) & 0o170000
            if not inside_destination or unix_file_type == 0o120000:
                raise WeatherError(
                    "The update ZIP contains an unsafe file path."
                )

        archive.extractall(destination)


def find_update_package_root(destination):
    executable_name = f"{APP_NAME}.exe"
    for root_directory, _, filenames in os.walk(destination):
        if executable_name in filenames:
            return root_directory

    raise WeatherError(
        f"The update ZIP does not contain {executable_name}."
    )


DISCLAIMER = """
IMPORTANT WEATHER, AI AND THIRD-PARTY DISCLAIMER

Kaja Guru Weather App provides weather information and locally generated AI
suggestions for general information only.

Weather forecasts are probabilistic. They may be inaccurate, delayed,
incomplete or unavailable. The local AI uses rules to analyze API weather
data. It may misunderstand questions or provide an incorrect answer.

Do not use this app as your only source for emergency planning, aviation,
maritime activity, medical decisions, agriculture, property protection,
dangerous travel or any safety-critical decision.

Always verify important information using an official government weather
department, emergency service or qualified professional.

WeatherAPI.com, internet connections and Windows notifications are independent
third-party services. They may change, fail, suspend access or stop operating.
The developer cannot guarantee their availability, accuracy or notification
delivery.

To the fullest extent allowed by applicable law, the developer is not
responsible for losses caused by reliance on inaccurate weather information,
an AI response, a missed notification or an unavailable third-party service.

Your selected storage mode controls local data:

• Permanent: saves your profile, settings, protected API key and cache, and
  starts the app with Windows.

• Normal: saves information until you manually delete it.

• Temporary: keeps information only for the current session and removes it
  when the app closes normally.

Location searches and weather requests are sent to WeatherAPI.com. Weather
data is provided under WeatherAPI.com's separate terms. Each publisher or user
must use an authorized API key and follow the applicable plan requirements.

Nothing in this disclaimer removes legal rights or liabilities that cannot
lawfully be excluded.
""".strip()


THEMES = {
    "Kaja Blue": (
        "#041A2F", "#0A3152", "#10476F",
        "#38BDF8", "#F8FAFC", "#A5D8F3",
    ),
    "Midnight": (
        "#050B18", "#0E1B2E", "#152945",
        "#38BDF8", "#F8FAFC", "#94A3B8",
    ),
    "Aurora": (
        "#031713", "#0B2924", "#123E36",
        "#5EEAD4", "#F0FDFA", "#99F6E4",
    ),
    "Ocean": (
        "#031525", "#082F49", "#0C4A6E",
        "#22D3EE", "#ECFEFF", "#A5F3FC",
    ),
    "Forest": (
        "#07180D", "#12351C", "#1B4D29",
        "#4ADE80", "#F0FDF4", "#BBF7D0",
    ),
    "Sunset": (
        "#1B0B18", "#341529", "#4A1E35",
        "#FB923C", "#FFF7ED", "#FED7AA",
    ),
    "Royal": (
        "#120A26", "#241346", "#382064",
        "#C084FC", "#FAF5FF", "#E9D5FF",
    ),
    "Cherry": (
        "#210811", "#3D1020", "#5A1830",
        "#FB7185", "#FFF1F2", "#FECDD3",
    ),
    "Cobalt": (
        "#07152E", "#102A56", "#173D78",
        "#60A5FA", "#EFF6FF", "#BFDBFE",
    ),
    "Emerald": (
        "#031C18", "#083B32", "#0E5749",
        "#34D399", "#ECFDF5", "#A7F3D0",
    ),
    "Amber": (
        "#211306", "#3F270A", "#5D3A0E",
        "#FBBF24", "#FFFBEB", "#FDE68A",
    ),
    "Rose": (
        "#210B1B", "#40162F", "#5E2045",
        "#F472B6", "#FDF2F8", "#FBCFE8",
    ),
    "Neon": (
        "#05050A", "#111124", "#1B1B35",
        "#22D3EE", "#F5F3FF", "#C4B5FD",
    ),
    "Lavender": (
        "#171126", "#2B2042", "#40305E",
        "#D8B4FE", "#FAF5FF", "#E9D5FF",
    ),
    "Matrix": (
        "#020A04", "#071A0C", "#0D2A14",
        "#4ADE80", "#F0FDF4", "#86EFAC",
    ),
    "Graphite": (
        "#090A0C", "#17191D", "#25282E",
        "#E5E7EB", "#FFFFFF", "#C7CBD1",
    ),
}


def get_theme(name):
    values = THEMES.get(name, THEMES["Kaja Blue"])
    return {
        "background": values[0],
        "panel": values[1],
        "card": values[2],
        "primary": values[3],
        "text": values[4],
        "muted": values[5],
        "input": values[2],
        "button_text": values[0],
    }


class DataBlob(ctypes.Structure):
    _fields_ = [
        ("cbData", wintypes.DWORD),
        ("pbData", ctypes.POINTER(ctypes.c_char)),
    ]


def protect_secret(secret):
    secret = str(secret or "").strip()

    if not secret:
        return ""

    try:
        raw = secret.encode("utf-8")
        source_buffer = ctypes.create_string_buffer(raw)

        source = DataBlob(
            len(raw),
            ctypes.cast(
                source_buffer,
                ctypes.POINTER(ctypes.c_char),
            ),
        )

        destination = DataBlob()

        success = ctypes.windll.crypt32.CryptProtectData(
            ctypes.byref(source),
            None,
            None,
            None,
            None,
            0,
            ctypes.byref(destination),
        )

        if not success:
            return ""

        try:
            encrypted = ctypes.string_at(
                destination.pbData,
                destination.cbData,
            )
            return base64.b64encode(encrypted).decode("ascii")
        finally:
            ctypes.windll.kernel32.LocalFree(
                destination.pbData
            )

    except Exception:
        return ""


def unprotect_secret(value):
    if not value:
        return ""

    try:
        encrypted = base64.b64decode(value)
        source_buffer = ctypes.create_string_buffer(encrypted)

        source = DataBlob(
            len(encrypted),
            ctypes.cast(
                source_buffer,
                ctypes.POINTER(ctypes.c_char),
            ),
        )

        destination = DataBlob()

        success = ctypes.windll.crypt32.CryptUnprotectData(
            ctypes.byref(source),
            None,
            None,
            None,
            None,
            0,
            ctypes.byref(destination),
        )

        if not success:
            return ""

        try:
            decrypted = ctypes.string_at(
                destination.pbData,
                destination.cbData,
            )
            return decrypted.decode("utf-8")
        finally:
            ctypes.windll.kernel32.LocalFree(
                destination.pbData
            )

    except Exception:
        return ""


class AppMemory:
    def __init__(self):
        self.lock = threading.RLock()
        self.data = self.defaults()
        self.session_cache = {}
        self.load()
        self.prune_cache()

    @staticmethod
    def defaults():
        return {
            "storage_mode": "",
            "disclaimer_accepted": False,
            "profile_name": "",
            "assistant_name": "Aira",
            "home_city": "",
            "protected_api_key": "",
            "last_query": "",
            "last_location": "",
            "theme": "Kaja Blue",
            "language": "English",
            "unit": "Celsius",
            "animations": True,
            "daily_notifications": True,
            "notification_time": "08:00",
            "refresh_minutes": 15,
            "cache_limit_mb": DEFAULT_CACHE_MB,
            "last_notification_date": "",
            "ai_mode": "Balanced",
            "github_repository": DEFAULT_GITHUB_REPOSITORY,
        }

    def is_temporary(self):
        return self.data.get("storage_mode") == "Temporary"

    def load(self):
        try:
            if os.path.isfile(SETTINGS_FILE):
                with open(
                    SETTINGS_FILE,
                    "r",
                    encoding="utf-8",
                ) as file:
                    saved = json.load(file)

                if isinstance(saved, dict):
                    self.data.update(saved)
        except Exception:
            self.data = self.defaults()

    def save(self):
        if self.is_temporary():
            return

        with self.lock:
            os.makedirs(APP_DATA, exist_ok=True)
            temporary = SETTINGS_FILE + ".tmp"

            with open(
                temporary,
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    self.data,
                    file,
                    indent=2,
                    ensure_ascii=False,
                )

            os.replace(temporary, SETTINGS_FILE)

    def update(self, **values):
        with self.lock:
            self.data.update(values)
            self.save()

    def get_api_key(self):
        return unprotect_secret(
            self.data.get("protected_api_key", "")
        )

    def set_api_key(self, key):
        protected = protect_secret(key)

        if not protected:
            raise ValueError(
                "The API key could not be protected."
            )

        self.update(protected_api_key=protected)

    def remove_api_key(self):
        self.update(protected_api_key="")

    @staticmethod
    def cache_path(query):
        filename = hashlib.sha256(
            query.strip().lower().encode("utf-8")
        ).hexdigest() + ".json"

        return os.path.join(CACHE_DIRECTORY, filename)

    def save_weather(self, query, weather):
        payload = {
            "saved_at": time.time(),
            "weather": weather,
        }

        if self.is_temporary():
            self.session_cache[
                query.strip().lower()
            ] = payload
            self.prune_cache()
            return

        os.makedirs(CACHE_DIRECTORY, exist_ok=True)
        target = self.cache_path(query)
        temporary = target + ".tmp"

        with open(
            temporary,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                payload,
                file,
                separators=(",", ":"),
            )

        os.replace(temporary, target)
        self.prune_cache()

    def load_weather(self, query):
        if self.is_temporary():
            payload = self.session_cache.get(
                query.strip().lower()
            )

            if not payload:
                return None

            if (
                time.time() - payload.get("saved_at", 0)
                > CACHE_LIFETIME
            ):
                return None

            return payload.get("weather")

        target = self.cache_path(query)

        try:
            with open(
                target,
                "r",
                encoding="utf-8",
            ) as file:
                payload = json.load(file)

            if (
                time.time() - payload.get("saved_at", 0)
                > CACHE_LIFETIME
            ):
                os.remove(target)
                return None

            os.utime(target, None)
            return payload.get("weather")

        except Exception:
            return None

    def prune_cache(self):
        try:
            configured_limit = int(
                self.data.get(
                    "cache_limit_mb",
                    DEFAULT_CACHE_MB,
                )
            )
        except (TypeError, ValueError):
            configured_limit = DEFAULT_CACHE_MB

        cache_limit_mb = max(
            MIN_CACHE_MB,
            min(
                MAX_CACHE_MB,
                configured_limit,
            ),
        )
        cache_limit_bytes = cache_limit_mb * 1024 * 1024

        if self.is_temporary():
            cutoff = time.time() - CACHE_LIFETIME
            self.session_cache = {
                key: value
                for key, value in self.session_cache.items()
                if value.get("saved_at", 0) >= cutoff
            }

            cached_items = []
            total_size = 0

            for key, value in self.session_cache.items():
                try:
                    size = len(
                        json.dumps(
                            value,
                            separators=(",", ":"),
                        ).encode("utf-8")
                    )
                except (TypeError, ValueError):
                    size = 0

                cached_items.append(
                    (value.get("saved_at", 0), size, key)
                )
                total_size += size

            cached_items.sort(key=lambda item: item[0])

            for _, size, key in cached_items:
                if total_size <= cache_limit_bytes:
                    break
                self.session_cache.pop(key, None)
                total_size -= size

            return

        if not os.path.isdir(CACHE_DIRECTORY):
            return

        files = []
        total_size = 0
        now = time.time()

        for filename in os.listdir(CACHE_DIRECTORY):
            path = os.path.join(CACHE_DIRECTORY, filename)

            try:
                modified = os.path.getmtime(path)
                size = os.path.getsize(path)

                if now - modified > CACHE_LIFETIME:
                    os.remove(path)
                    continue

                files.append((modified, size, path))
                total_size += size
            except OSError:
                pass

        files.sort(key=lambda item: item[0])

        for _, size, path in files:
            if total_size <= cache_limit_bytes:
                break

            try:
                os.remove(path)
                total_size -= size
            except OSError:
                pass

    def clear_cache(self):
        self.session_cache.clear()

        if os.path.isdir(CACHE_DIRECTORY):
            shutil.rmtree(
                CACHE_DIRECTORY,
                ignore_errors=True,
            )

        self.update(
            last_query="",
            last_location="",
        )

    def delete_all(self):
        with self.lock:
            self.session_cache.clear()

            if os.path.isdir(APP_DATA):
                shutil.rmtree(
                    APP_DATA,
                    ignore_errors=True,
                )

            self.data = self.defaults()

    def end_temporary_session(self):
        if not self.is_temporary():
            return

        self.session_cache.clear()
        self.data = self.defaults()

        if os.path.isdir(APP_DATA):
            shutil.rmtree(
                APP_DATA,
                ignore_errors=True,
            )


class WeatherError(Exception):
    pass


class KajaGuruWeatherApp:
    def __init__(self, root):
        self.root = root
        self.memory = AppMemory()

        self.root.title(
            f"{APP_NAME} {APP_VERSION}"
        )
        self.root.geometry("1120x760")
        self.root.minsize(940, 650)
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_app,
        )

        self.colors = get_theme(
            self.memory.data.get(
                "theme",
                "Kaja Blue",
            )
        )

        self.logo_images = []
        self.weather = None
        self.ai_result = None
        self.loading = False
        self.deleting_data = False
        self.update_in_progress = False
        self.last_fetch_time = 0

        self.city_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.unit_var = tk.StringVar(
            value=self.memory.data.get(
                "unit",
                "Celsius",
            )
        )

        self.suggestion_job = None
        self.suggestion_token = 0
        self.city_suggestions = []

        self.background_canvas = None
        self.particles = []

        self.app_icon = self.load_logo(256)
        if self.app_icon is not None:
            try:
                self.root.iconphoto(True, self.app_icon)
            except tk.TclError:
                pass

        if not self.memory.data.get("disclaimer_accepted"):
            self.show_disclaimer()
        elif not self.memory.data.get("storage_mode"):
            self.show_storage_screen()
        elif not self.memory.data.get("profile_name"):
            self.show_profile()
        else:
            self.show_dashboard()

        self.animate_background()
        self.background_tasks()

    def clear_root(self):
        for widget in self.root.winfo_children():
            if not isinstance(widget, tk.Toplevel):
                widget.destroy()

        self.logo_images.clear()
        self.background_canvas = None
        self.particles = []

    def tr(self, key, **values):
        language = self.memory.data.get(
            "language",
            "English",
        )
        language_texts = TEXTS.get(
            language,
            TEXTS["English"],
        )
        text = language_texts.get(
            key,
            TEXTS["English"].get(key, key),
        )

        try:
            return text.format(**values)
        except (KeyError, ValueError):
            return text

    def select_onboarding_language(self, language):
        if language not in LANGUAGE_CODES:
            language = "English"

        # Do not create a settings file before the user chooses a
        # Permanent, Normal or Temporary storage mode.
        self.memory.data["language"] = language
        self.show_storage_screen()

    def weather_language_code(self):
        return LANGUAGE_CODES.get(
            self.memory.data.get("language", "English"),
            "en",
        )

    def weather_cache_key(self, query):
        return (
            f"{query.strip()}::lang="
            f"{self.weather_language_code()}"
        )

    def load_logo(self, target_size):
        if not os.path.isfile(LOGO_PATH):
            return None

        try:
            image = tk.PhotoImage(file=LOGO_PATH)
            largest = max(image.width(), image.height())
            factor = max(
                1,
                math.ceil(largest / target_size),
            )

            if factor > 1:
                image = image.subsample(
                    factor,
                    factor,
                )

            self.logo_images.append(image)
            return image
        except tk.TclError:
            return None

    def add_logo(self, parent, size, **pack_options):
        image = self.load_logo(size)

        if image is None:
            return

        tk.Label(
            parent,
            image=image,
            bg=parent.cget("bg"),
            borderwidth=0,
        ).pack(**pack_options)

    def button(
        self,
        parent,
        text,
        command,
        secondary=False,
    ):
        normal_color = (
            self.colors["card"]
            if secondary
            else self.colors["primary"]
        )

        foreground = (
            self.colors["text"]
            if secondary
            else self.colors["button_text"]
        )

        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=normal_color,
            fg=foreground,
            activebackground=self.colors["input"],
            activeforeground=self.colors["text"],
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8,
        )

        button.bind(
            "<Enter>",
            lambda event: button.configure(
                bg=self.colors["input"]
            ),
        )

        button.bind(
            "<Leave>",
            lambda event: button.configure(
                bg=normal_color
            ),
        )

        return button

    def fade_in(self):
        if not self.memory.data.get("animations", True):
            return

        try:
            self.root.attributes("-alpha", 0.82)
        except tk.TclError:
            return

        def step(value=0.82):
            value = min(1.0, value + 0.03)

            try:
                self.root.attributes("-alpha", value)
            except tk.TclError:
                return

            if value < 1.0:
                self.root.after(
                    18,
                    lambda: step(value),
                )

        step()

    def show_storage_screen(self):
        self.clear_root()
        self.root.configure(
            bg=self.colors["background"]
        )

        panel = tk.Frame(
            self.root,
            bg=self.colors["panel"],
            padx=35,
            pady=25,
        )
        panel.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=720,
            height=700,
        )

        self.add_logo(
            panel,
            115,
            anchor="center",
            pady=(0, 8),
        )

        tk.Label(
            panel,
            text=APP_NAME,
            font=("Segoe UI", 25, "bold"),
            bg=self.colors["panel"],
            fg=self.colors["text"],
        ).pack()

        language_row = tk.Frame(
            panel,
            bg=self.colors["panel"],
        )
        language_row.pack(pady=(8, 5))

        tk.Label(
            language_row,
            text=self.tr("language") + ":",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors["panel"],
            fg=self.colors["text"],
        ).pack(side="left", padx=(0, 8))

        language_var = tk.StringVar(
            value=self.memory.data.get(
                "language",
                "English",
            )
        )
        language_box = ttk.Combobox(
            language_row,
            textvariable=language_var,
            values=tuple(LANGUAGE_CODES),
            state="readonly",
            width=14,
        )
        language_box.pack(side="left")
        language_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.select_onboarding_language(
                language_var.get()
            ),
        )

        tk.Label(
            panel,
            text=self.tr("choose_storage"),
            font=("Segoe UI", 10),
            bg=self.colors["panel"],
            fg=self.colors["muted"],
        ).pack(pady=(4, 16))

        choices = (
            (
                "Permanent",
                self.tr("permanent_desc"),
            ),
            (
                "Normal",
                self.tr("normal_desc"),
            ),
            (
                "Temporary",
                self.tr("temporary_desc"),
            ),
        )

        def select_mode(mode):
            permanent = mode == "Permanent"

            self.memory.update(
                storage_mode=mode,
                start_with_windows=permanent,
            )

            self.configure_windows_startup(permanent)

            if self.memory.data.get("profile_name"):
                self.show_dashboard()
            else:
                self.show_profile()

        for mode, description in choices:
            card = tk.Frame(
                panel,
                bg=self.colors["card"],
                padx=15,
                pady=14,
            )
            card.pack(fill="x", pady=7)

            self.button(
                card,
                self.tr(mode.lower()),
                lambda selected=mode: select_mode(selected),
            ).pack(side="left", padx=(0, 15))

            tk.Label(
                card,
                text=description,
                bg=self.colors["card"],
                fg=self.colors["muted"],
                font=("Segoe UI", 9),
                wraplength=470,
                justify="left",
            ).pack(side="left", fill="x", expand=True)

        tk.Label(
            panel,
            text=self.tr("close_note"),
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=("Segoe UI", 8),
            wraplength=620,
            justify="center",
        ).pack(pady=(15, 7))

        self.button(
            panel,
            self.tr("exit"),
            self.close_app,
            secondary=True,
        ).pack()

        self.fade_in()

    def show_disclaimer(self):
        self.clear_root()
        self.root.configure(
            bg=self.colors["background"]
        )

        panel = tk.Frame(
            self.root,
            bg=self.colors["panel"],
            padx=28,
            pady=22,
        )
        panel.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            relwidth=0.82,
            relheight=0.9,
        )

        title_row = tk.Frame(
            panel,
            bg=self.colors["panel"],
        )
        title_row.pack(fill="x")

        self.add_logo(
            title_row,
            65,
            side="left",
            padx=(0, 14),
        )

        tk.Label(
            title_row,
            text=self.tr("disclaimer"),
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["panel"],
            fg=self.colors["text"],
        ).pack(side="left")

        text = tk.Text(
            panel,
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=("Segoe UI", 10),
            wrap="word",
            relief="flat",
            padx=15,
            pady=15,
        )
        text.pack(
            fill="both",
            expand=True,
            pady=(12, 8),
        )
        text.insert("1.0", DISCLAIMER)
        text.configure(state="disabled")

        accepted = tk.BooleanVar(value=False)

        tk.Checkbutton(
            panel,
            text=self.tr("accept_disclaimer"),
            variable=accepted,
            bg=self.colors["panel"],
            fg=self.colors["text"],
            selectcolor=self.colors["input"],
            activebackground=self.colors["panel"],
            activeforeground=self.colors["text"],
        ).pack(anchor="w", pady=7)

        def continue_app():
            if not accepted.get():
                messagebox.showwarning(
                    APP_NAME,
                    self.tr("accept_warning"),
                )
                return

            if self.memory.data.get("storage_mode"):
                self.memory.update(
                    disclaimer_accepted=True
                )
                self.show_profile()
            else:
                # The disclaimer must be first on a completely fresh
                # installation. Storage is selected on the next screen,
                # so no settings file is created before that choice.
                self.memory.data[
                    "disclaimer_accepted"
                ] = True
                self.show_storage_screen()

        row = tk.Frame(
            panel,
            bg=self.colors["panel"],
        )
        row.pack(fill="x")

        self.button(
            row,
            self.tr("accept_continue"),
            continue_app,
        ).pack(side="left")

        self.button(
            row,
            self.tr("exit"),
            self.close_app,
            secondary=True,
        ).pack(side="left", padx=8)

        self.fade_in()

    def profile_field(
        self,
        parent,
        title,
        variable,
        hint,
    ):
        tk.Label(
            parent,
            text=title,
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", pady=(10, 4))

        tk.Entry(
            parent,
            textvariable=variable,
            bg=self.colors["input"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            font=("Segoe UI", 11),
            relief="flat",
        ).pack(fill="x", ipady=8)

        tk.Label(
            parent,
            text=hint,
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=("Segoe UI", 8),
        ).pack(anchor="w", pady=(3, 0))

    def show_profile(self):
        self.clear_root()
        self.root.configure(
            bg=self.colors["background"]
        )

        panel = tk.Frame(
            self.root,
            bg=self.colors["panel"],
            padx=38,
            pady=28,
        )
        panel.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=610,
            height=650,
        )

        self.add_logo(
            panel,
            90,
            anchor="center",
            pady=(0, 8),
        )

        tk.Label(
            panel,
            text=self.tr("create_profile"),
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["panel"],
            fg=self.colors["text"],
        ).pack(anchor="w")

        tk.Label(
            panel,
            text=self.tr("profile_note"),
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(3, 10))

        name_var = tk.StringVar()
        assistant_var = tk.StringVar(value="Aira")
        city_var = tk.StringVar()

        self.profile_field(
            panel,
            self.tr("your_name"),
            name_var,
            self.tr("name_hint"),
        )

        self.profile_field(
            panel,
            self.tr("assistant_name"),
            assistant_var,
            self.tr("assistant_hint"),
        )

        self.profile_field(
            panel,
            self.tr("home_city"),
            city_var,
            self.tr("city_hint"),
        )

        tk.Label(
            panel,
            text=(
                "The assistant uses your name in weather briefings "
                "and Windows notifications."
            ),
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=("Segoe UI", 9),
            wraplength=500,
            justify="left",
        ).pack(anchor="w", pady=(15, 18))

        def create_profile():
            name = name_var.get().strip()
            assistant = assistant_var.get().strip()
            city = city_var.get().strip()

            if len(name) < 2 or "@" in name:
                messagebox.showwarning(
                    APP_NAME,
                    "Enter your name, not an email address.",
                )
                return

            if len(city) < 2:
                messagebox.showwarning(
                    APP_NAME,
                    "Please enter your home city.",
                )
                return

            if len(assistant) < 2:
                assistant = "Aira"

            self.memory.update(
                profile_name=name[:40],
                assistant_name=assistant[:40],
                home_city=city[:80],
                last_query=city[:80],
                last_location=city[:80],
            )

            self.city_var.set(city)
            self.show_dashboard()

            if not self.memory.get_api_key():
                self.root.after(
                    300,
                    self.open_settings,
                )
            else:
                self.root.after(
                    400,
                    self.search_weather,
                )

        self.button(
            panel,
            self.tr("create_button"),
            create_profile,
        ).pack(anchor="w")

        self.fade_in()

    def show_dashboard(self):
        self.clear_root()

        self.colors = get_theme(
            self.memory.data.get(
                "theme",
                "Kaja Blue",
            )
        )

        self.root.configure(
            bg=self.colors["background"]
        )

        # This Canvas is created first, so every later widget stays above it.
        # Do not call canvas.lower() without a tag; that causes the TclError.
        self.background_canvas = tk.Canvas(
            self.root,
            bg=self.colors["background"],
            highlightthickness=0,
        )
        self.background_canvas.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1,
        )

        self.create_particles()
        self.configure_styles()

        header = tk.Frame(
            self.root,
            bg=self.colors["background"],
        )
        header.pack(
            fill="x",
            padx=35,
            pady=(16, 8),
        )

        self.add_logo(
            header,
            58,
            side="left",
            padx=(0, 12),
        )

        name = self.memory.data.get(
            "profile_name",
            "User",
        )
        assistant = self.memory.data.get(
            "assistant_name",
            "Aira",
        )

        title_area = tk.Frame(
            header,
            bg=self.colors["background"],
        )
        title_area.pack(side="left")

        tk.Label(
            title_area,
            text=self.tr("hello", name=name),
            bg=self.colors["background"],
            fg=self.colors["text"],
            font=("Segoe UI", 22, "bold"),
        ).pack(anchor="w")

        tk.Label(
            title_area,
            text=self.tr(
                "ready",
                app=APP_NAME,
                assistant=assistant,
            ),
            bg=self.colors["background"],
            fg=self.colors["muted"],
            font=("Segoe UI", 9),
        ).pack(anchor="w")

        self.button(
            header,
            self.tr("themes"),
            self.open_theme_palette,
            secondary=True,
        ).pack(side="right", padx=(8, 0))

        self.button(
            header,
            self.tr("settings"),
            self.open_settings,
            secondary=True,
        ).pack(side="right")

        self.button(
            header,
            self.tr("restart"),
            self.restart_application,
            secondary=True,
        ).pack(side="right", padx=(0, 8))

        search_panel = tk.Frame(
            self.root,
            bg=self.colors["panel"],
            padx=14,
            pady=12,
        )
        search_panel.pack(
            fill="x",
            padx=35,
        )

        search_row = tk.Frame(
            search_panel,
            bg=self.colors["panel"],
        )
        search_row.pack(fill="x")

        if not self.city_var.get():
            self.city_var.set(
                self.memory.data.get("last_location")
                or self.memory.data.get("home_city", "")
            )

        self.city_entry = tk.Entry(
            search_row,
            textvariable=self.city_var,
            bg=self.colors["input"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            font=("Segoe UI", 12),
            relief="flat",
        )
        self.city_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=9,
            padx=(0, 10),
        )

        self.city_entry.bind(
            "<Return>",
            lambda event: self.search_weather(),
        )
        self.city_entry.bind(
            "<KeyRelease>",
            self.city_key_released,
        )

        unit_box = ttk.Combobox(
            search_row,
            textvariable=self.unit_var,
            values=("Celsius", "Fahrenheit"),
            state="readonly",
            width=12,
        )
        unit_box.pack(
            side="left",
            padx=(0, 10),
        )
        unit_box.bind(
            "<<ComboboxSelected>>",
            self.change_unit,
        )

        self.search_button = self.button(
            search_row,
            self.tr("search"),
            self.search_weather,
        )
        self.search_button.pack(side="left")

        self.suggestion_list = tk.Listbox(
            search_panel,
            height=5,
            bg=self.colors["input"],
            fg=self.colors["text"],
            selectbackground=self.colors["primary"],
            selectforeground=self.colors["button_text"],
            font=("Segoe UI", 10),
            relief="flat",
        )
        self.suggestion_list.bind(
            "<Double-Button-1>",
            self.choose_suggestion,
        )
        self.suggestion_list.bind(
            "<Return>",
            self.choose_suggestion,
        )

        status_row = tk.Frame(
            self.root,
            bg=self.colors["background"],
        )
        status_row.pack(
            fill="x",
            padx=37,
            pady=(6, 5),
        )

        tk.Label(
            status_row,
            textvariable=self.status_var,
            bg=self.colors["background"],
            fg=self.colors["muted"],
            font=("Segoe UI", 9),
        ).pack(side="left")

        self.clock_label = tk.Label(
            status_row,
            text=datetime.now().strftime(
                "%A, %d %B %Y • %H:%M:%S"
            ),
            bg=self.colors["background"],
            fg=self.colors["muted"],
            font=("Segoe UI", 9),
        )
        self.clock_label.pack(side="right")

        current_panel = tk.Frame(
            self.root,
            bg=self.colors["panel"],
            padx=20,
            pady=14,
        )
        current_panel.pack(
            fill="x",
            padx=35,
            pady=(0, 8),
        )

        self.weather_icon_label = tk.Label(
            current_panel,
            text="🌍",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI Emoji", 42),
        )
        self.weather_icon_label.pack(
            side="left",
            padx=(0, 14),
        )

        current_text = tk.Frame(
            current_panel,
            bg=self.colors["panel"],
        )
        current_text.pack(side="left")

        self.location_label = tk.Label(
            current_text,
            text="Search for a city",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 15, "bold"),
        )
        self.location_label.pack(anchor="w")

        self.temperature_label = tk.Label(
            current_text,
            text="--°",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 34, "bold"),
        )
        self.temperature_label.pack(anchor="w")

        self.condition_label = tk.Label(
            current_text,
            text="Current conditions",
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=("Segoe UI", 10),
        )
        self.condition_label.pack(anchor="w")

        self.details_label = tk.Label(
            current_panel,
            text=(
                "Feels: --   Humidity: --   Wind: --\n"
                "Rain: --   Pressure: --   UV: --"
            ),
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=("Segoe UI", 10),
            justify="left",
            padx=18,
            pady=12,
        )
        self.details_label.pack(
            side="right",
            padx=(20, 0),
        )

        notebook = ttk.Notebook(self.root)
        notebook.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 5),
        )

        daily_tab = tk.Frame(
            notebook,
            bg=self.colors["background"],
        )
        hourly_tab = tk.Frame(
            notebook,
            bg=self.colors["background"],
        )
        ai_tab = tk.Frame(
            notebook,
            bg=self.colors["background"],
        )

        notebook.add(
            daily_tab,
            text=self.tr("daily"),
        )
        notebook.add(
            hourly_tab,
            text=self.tr("hourly"),
        )
        notebook.add(
            ai_tab,
            text=self.tr("ask", assistant=assistant),
        )

        self.daily_text = tk.Text(
            daily_tab,
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 11),
            wrap="word",
            relief="flat",
            padx=18,
            pady=15,
        )
        self.daily_text.pack(
            fill="both",
            expand=True,
            pady=8,
        )
        self.daily_text.insert(
            "1.0",
            "Search for a city to see predictions."
        )
        self.daily_text.configure(state="disabled")

        columns = (
            "time",
            "temperature",
            "condition",
            "rain",
            "wind",
        )

        self.hourly_tree = ttk.Treeview(
            hourly_tab,
            columns=columns,
            show="headings",
        )

        headings = (
            "Date and Time",
            "Temperature",
            "Condition",
            "Rain",
            "Wind",
        )

        for column, title in zip(columns, headings):
            self.hourly_tree.heading(
                column,
                text=title,
            )
            self.hourly_tree.column(
                column,
                anchor="center",
                width=180,
            )

        scrollbar = ttk.Scrollbar(
            hourly_tab,
            command=self.hourly_tree.yview,
        )
        self.hourly_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.hourly_tree.pack(
            side="left",
            fill="both",
            expand=True,
        )
        scrollbar.pack(
            side="right",
            fill="y",
        )

        self.ai_summary_label = tk.Label(
            ai_tab,
            text=(
                f"{assistant} will analyze the forecast here. "
                "AI answers may be incorrect."
            ),
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 11),
            wraplength=900,
            justify="left",
            padx=18,
            pady=14,
        )
        self.ai_summary_label.pack(
            fill="x",
            pady=(10, 8),
        )

        question_row = tk.Frame(
            ai_tab,
            bg=self.colors["background"],
        )
        question_row.pack(fill="x")

        self.ai_question_var = tk.StringVar()

        ai_entry = tk.Entry(
            question_row,
            textvariable=self.ai_question_var,
            bg=self.colors["input"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            font=("Segoe UI", 11),
            relief="flat",
        )
        ai_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=8,
            padx=(0, 8),
        )
        ai_entry.bind(
            "<Return>",
            lambda event: self.ask_ai(),
        )

        self.button(
            question_row,
            self.tr("ask", assistant=assistant),
            self.ask_ai,
        ).pack(side="left")

        self.ai_answer_label = tk.Label(
            ai_tab,
            text=(
                "Try: Hello, will it rain, what should I wear, "
                "is it safe to travel, or what is the best outdoor time?"
            ),
            bg=self.colors["background"],
            fg=self.colors["muted"],
            font=("Segoe UI", 10),
            wraplength=900,
            justify="left",
        )
        self.ai_answer_label.pack(
            fill="x",
            anchor="w",
            pady=12,
        )

        tk.Label(
            self.root,
            text=(
                "Weather data provided by WeatherAPI.com • "
                "General information only"
            ),
            bg=self.colors["background"],
            fg=self.colors["muted"],
            font=("Segoe UI", 8),
        ).pack(pady=(0, 6))

        self.restore_weather()
        self.fade_in()

    def configure_styles(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TNotebook",
            background=self.colors["background"],
            borderwidth=0,
        )
        style.configure(
            "TNotebook.Tab",
            background=self.colors["panel"],
            foreground=self.colors["muted"],
            padding=(18, 8),
        )
        style.map(
            "TNotebook.Tab",
            background=[
                ("selected", self.colors["primary"])
            ],
            foreground=[
                ("selected", self.colors["button_text"])
            ],
        )
        style.configure(
            "Treeview",
            background=self.colors["panel"],
            fieldbackground=self.colors["panel"],
            foreground=self.colors["text"],
            rowheight=28,
        )
        style.configure(
            "Treeview.Heading",
            background=self.colors["card"],
            foreground=self.colors["text"],
        )

    def create_particles(self):
        if self.background_canvas is None:
            return

        width = max(1120, self.root.winfo_width())
        height = max(760, self.root.winfo_height())

        for index in range(14):
            radius = random.randint(22, 60)
            x = random.randint(0, width)
            y = random.randint(0, height)

            item = self.background_canvas.create_oval(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill=(
                    self.colors["primary"]
                    if index % 2 == 0
                    else self.colors["card"]
                ),
                outline="",
                stipple="gray50",
            )

            self.particles.append({
                "item": item,
                "x": x,
                "y": y,
                "radius": radius,
                "dx": random.uniform(-0.3, 0.3),
                "dy": random.uniform(-0.22, 0.22),
            })

    def animate_background(self):
        canvas = self.background_canvas

        if (
            canvas is not None
            and canvas.winfo_exists()
            and self.memory.data.get("animations", True)
        ):
            width = max(1, self.root.winfo_width())
            height = max(1, self.root.winfo_height())

            for particle in self.particles:
                particle["x"] += particle["dx"]
                particle["y"] += particle["dy"]

                radius = particle["radius"]

                if particle["x"] < -radius:
                    particle["x"] = width + radius
                elif particle["x"] > width + radius:
                    particle["x"] = -radius

                if particle["y"] < -radius:
                    particle["y"] = height + radius
                elif particle["y"] > height + radius:
                    particle["y"] = -radius

                try:
                    canvas.coords(
                        particle["item"],
                        particle["x"] - radius,
                        particle["y"] - radius,
                        particle["x"] + radius,
                        particle["y"] + radius,
                    )
                except tk.TclError:
                    break

        try:
            self.root.after(
                40,
                self.animate_background,
            )
        except tk.TclError:
            pass

    def city_key_released(self, event=None):
        if event and event.keysym in (
            "Up",
            "Down",
            "Return",
            "Escape",
        ):
            return

        if self.suggestion_job:
            self.root.after_cancel(
                self.suggestion_job
            )

        query = self.city_var.get().strip()

        if len(query) < 2:
            self.hide_suggestions()
            return

        self.suggestion_job = self.root.after(
            350,
            lambda: self.fetch_city_suggestions(query),
        )

    def fetch_city_suggestions(self, query):
        if not self.memory.get_api_key():
            return

        self.suggestion_token += 1
        token = self.suggestion_token

        def worker():
            try:
                results = self.api_request(
                    "search.json",
                    {"q": query},
                )

                self.root.after(
                    0,
                    lambda: self.show_suggestions(
                        results,
                        token,
                    ),
                )
            except Exception:
                pass

        threading.Thread(
            target=worker,
            daemon=True,
        ).start()

    def show_suggestions(self, results, token):
        if token != self.suggestion_token:
            return

        self.city_suggestions = results[:8]
        self.suggestion_list.delete(0, tk.END)

        for location in self.city_suggestions:
            text = ", ".join(
                part
                for part in (
                    location.get("name"),
                    location.get("region"),
                    location.get("country"),
                )
                if part
            )
            self.suggestion_list.insert(tk.END, text)

        if self.city_suggestions:
            if not self.suggestion_list.winfo_ismapped():
                self.suggestion_list.pack(
                    fill="x",
                    pady=(7, 0),
                )
        else:
            self.hide_suggestions()

    def choose_suggestion(self, event=None):
        selection = self.suggestion_list.curselection()

        if not selection:
            return

        index = selection[0]
        location = self.city_suggestions[index]
        display_name = self.suggestion_list.get(index)

        self.city_var.set(display_name)
        self.hide_suggestions()

        query = (
            f"{location.get('lat')},"
            f"{location.get('lon')}"
        )
        self.search_weather(query=query)

    def hide_suggestions(self):
        if (
            hasattr(self, "suggestion_list")
            and self.suggestion_list.winfo_ismapped()
        ):
            self.suggestion_list.pack_forget()

    def api_request(
        self,
        endpoint,
        parameters,
    ):
        api_key = self.memory.get_api_key()

        if not api_key:
            raise WeatherError(
                "No WeatherAPI key is configured."
            )

        parameters = dict(parameters)
        parameters["key"] = api_key

        request = Request(
            (
                f"{API_BASE_URL}/{endpoint}?"
                f"{urlencode(parameters)}"
            ),
            headers={
                "User-Agent": (
                    f"{APP_NAME}/{APP_VERSION}"
                ),
                "Accept": "application/json",
            },
        )

        try:
            with urlopen(
                request,
                timeout=15,
            ) as response:
                return json.loads(
                    response.read().decode("utf-8")
                )

        except HTTPError as error:
            try:
                payload = json.loads(
                    error.read().decode("utf-8")
                )
                reason = payload["error"]["message"]
            except Exception:
                reason = (
                    f"Weather service error {error.code}."
                )

            raise WeatherError(reason) from None

        except URLError:
            raise WeatherError(
                "Unable to connect to WeatherAPI."
            ) from None

    def search_weather(
        self,
        query=None,
        silent=False,
    ):
        if self.loading or self.deleting_data:
            return

        query = (
            query
            or self.city_var.get().strip()
        )

        if not query:
            return

        if not self.memory.get_api_key():
            if not silent:
                self.open_settings()
            return

        self.loading = True
        self.last_fetch_time = time.time()
        self.status_var.set("Loading weather...")

        if hasattr(self, "search_button"):
            self.search_button.configure(
                state="disabled",
                text="Loading...",
            )

        def worker():
            try:
                weather = self.api_request(
                    "forecast.json",
                    {
                        "q": query,
                        "days": 3,
                        "aqi": "yes",
                        "alerts": "yes",
                        "lang": self.weather_language_code(),
                    },
                )

                if self.deleting_data:
                    return

                self.memory.save_weather(
                    self.weather_cache_key(query),
                    weather,
                )

                location = weather.get(
                    "location",
                    {},
                )

                display_name = ", ".join(
                    part
                    for part in (
                        location.get("name"),
                        location.get("region"),
                        location.get("country"),
                    )
                    if part
                )

                self.memory.update(
                    last_query=query,
                    last_location=display_name,
                )

                self.root.after(
                    0,
                    lambda: self.weather_loaded(
                        weather,
                        display_name,
                    ),
                )

            except Exception as error:
                cached = self.memory.load_weather(
                    self.weather_cache_key(query)
                )
                error_message = str(error)

                self.root.after(
                    0,
                    lambda: self.weather_failed(
                        cached,
                        error_message,
                        silent,
                    ),
                )

        threading.Thread(
            target=worker,
            daemon=True,
        ).start()

    def weather_loaded(
        self,
        weather,
        display_name,
    ):
        self.loading = False
        self.weather = weather
        self.city_var.set(display_name)
        self.status_var.set(
            "Weather updated successfully."
        )

        if hasattr(self, "search_button"):
            self.search_button.configure(
                state="normal",
                text=self.tr("search"),
            )

        self.display_weather(weather)

    def weather_failed(
        self,
        cached,
        error_message,
        silent,
    ):
        self.loading = False

        if hasattr(self, "search_button"):
            self.search_button.configure(
                state="normal",
                text=self.tr("search"),
            )

        if cached:
            self.weather = cached
            self.status_var.set(
                "Showing recent cached weather."
            )
            self.display_weather(cached)
            return

        self.status_var.set("Weather request failed.")

        if not silent:
            messagebox.showerror(
                APP_NAME,
                error_message,
            )

    def restore_weather(self):
        query = self.memory.data.get(
            "last_query",
            "",
        )

        if query:
            cached = self.memory.load_weather(
                self.weather_cache_key(query)
            )

            if cached:
                self.weather = cached
                self.display_weather(cached)
                self.status_var.set(
                    "Showing recent cached weather."
                )
                return

        if (
            self.memory.get_api_key()
            and self.memory.data.get("home_city")
        ):
            self.root.after(
                500,
                lambda: self.search_weather(
                    self.memory.data.get("home_city"),
                    silent=True,
                ),
            )

    def display_weather(self, weather):
        location = weather.get("location", {})
        current = weather.get("current", {})
        forecast_days = weather.get(
            "forecast",
            {},
        ).get("forecastday", [])

        fahrenheit = (
            self.unit_var.get() == "Fahrenheit"
        )

        if fahrenheit:
            temperature = current.get("temp_f")
            feels = current.get("feelslike_f")
            wind = current.get("wind_mph")
            temperature_unit = "°F"
            wind_unit = "mph"
        else:
            temperature = current.get("temp_c")
            feels = current.get("feelslike_c")
            wind = current.get("wind_kph")
            temperature_unit = "°C"
            wind_unit = "km/h"

        condition = current.get(
            "condition",
            {},
        ).get("text", "Unknown")

        display_location = ", ".join(
            part
            for part in (
                location.get("name"),
                location.get("region"),
                location.get("country"),
            )
            if part
        )

        local_time = location.get(
            "localtime",
            "Unknown time",
        )

        self.location_label.configure(
            text=f"{display_location} • {local_time}"
        )
        self.temperature_label.configure(
            text=f"{self.number(temperature)}{temperature_unit}"
        )
        self.condition_label.configure(
            text=condition
        )
        self.weather_icon_label.configure(
            text=self.condition_icon(condition)
        )

        precipitation = current.get(
            "precip_mm",
            0,
        )

        self.details_label.configure(
            text=(
                f"Feels: {self.number(feels)}{temperature_unit}   "
                f"Humidity: {current.get('humidity', '--')}%   "
                f"Wind: {self.number(wind)} {wind_unit}\n"
                f"Rain: {self.number(precipitation)} mm   "
                f"Pressure: {self.number(current.get('pressure_mb'))} mb   "
                f"UV: {self.number(current.get('uv'))}"
            )
        )

        self.daily_text.configure(state="normal")
        self.daily_text.delete("1.0", tk.END)

        for forecast in forecast_days:
            date_text = forecast.get("date", "")

            try:
                date_text = datetime.strptime(
                    date_text,
                    "%Y-%m-%d",
                ).strftime(
                    "%A, %d %B %Y"
                )
            except ValueError:
                pass

            day = forecast.get("day", {})
            day_condition = day.get(
                "condition",
                {},
            ).get("text", "Unknown")

            if fahrenheit:
                high = day.get("maxtemp_f")
                low = day.get("mintemp_f")
            else:
                high = day.get("maxtemp_c")
                low = day.get("mintemp_c")

            self.daily_text.insert(
                tk.END,
                (
                    f"{self.condition_icon(day_condition)}  "
                    f"{date_text}\n"
                    f"Condition: {day_condition}\n"
                    f"High: {self.number(high)}{temperature_unit}   "
                    f"Low: {self.number(low)}{temperature_unit}   "
                    f"Rain chance: "
                    f"{day.get('daily_chance_of_rain', 0)}%   "
                    f"Maximum wind: "
                    f"{self.number(day.get('maxwind_kph'))} km/h\n\n"
                ),
            )

        self.daily_text.configure(state="disabled")

        for item in self.hourly_tree.get_children():
            self.hourly_tree.delete(item)

        for forecast in forecast_days:
            for hour in forecast.get("hour", []):
                if fahrenheit:
                    hour_temperature = hour.get("temp_f")
                    hour_wind = hour.get("wind_mph")
                    hour_wind_unit = "mph"
                else:
                    hour_temperature = hour.get("temp_c")
                    hour_wind = hour.get("wind_kph")
                    hour_wind_unit = "km/h"

                self.hourly_tree.insert(
                    "",
                    tk.END,
                    values=(
                        hour.get("time", ""),
                        (
                            f"{self.number(hour_temperature)}"
                            f"{temperature_unit}"
                        ),
                        hour.get(
                            "condition",
                            {},
                        ).get("text", "Unknown"),
                        (
                            f"{hour.get('chance_of_rain', 0)}%"
                        ),
                        (
                            f"{self.number(hour_wind)} "
                            f"{hour_wind_unit}"
                        ),
                    ),
                )

        self.ai_result = self.analyze_weather(weather)

        self.ai_summary_label.configure(
            text=self.ai_result["summary"]
        )

    def analyze_weather(self, weather):
        current = weather.get("current", {})
        forecast_days = weather.get(
            "forecast",
            {},
        ).get("forecastday", [])

        day = (
            forecast_days[0].get("day", {})
            if forecast_days
            else {}
        )

        condition = current.get(
            "condition",
            {},
        ).get("text", "Unknown")

        temperature = current.get("temp_c", 0)
        wind = current.get("wind_kph", 0)
        rain_chance = day.get(
            "daily_chance_of_rain",
            0,
        )
        uv = current.get("uv", 0)

        mode = self.memory.data.get(
            "ai_mode",
            "Balanced",
        )

        rain_limit = 25 if mode == "Cautious" else 45
        wind_limit = 30 if mode == "Cautious" else 45

        if rain_chance >= rain_limit:
            rain = (
                f"Rain chance is {rain_chance}%. "
                "Carrying an umbrella is recommended."
            )
        else:
            rain = (
                f"Rain chance is {rain_chance}%. "
                "Rain risk currently appears lower."
            )

        if temperature <= 12:
            clothing = (
                "Wear warm layers and consider a jacket."
            )
        elif temperature >= 32:
            clothing = (
                "Wear light clothing, drink water and avoid "
                "long exposure to strong heat."
            )
        else:
            clothing = (
                "Comfortable everyday clothing should be suitable."
            )

        if wind >= wind_limit:
            travel = (
                f"Wind is around {self.number(wind)} km/h. "
                "Use additional caution while travelling."
            )
        elif rain_chance >= 60:
            travel = (
                "Heavy rain may affect visibility and road conditions."
            )
        else:
            travel = (
                "No major travel warning is visible in the current "
                "local forecast, but verify road conditions."
            )

        if uv >= 6:
            outdoor = (
                "UV is high. Use shade, sunscreen and protective clothing."
            )
        elif rain_chance >= 60:
            outdoor = (
                "Outdoor plans may be interrupted by rain."
            )
        else:
            outdoor = (
                "Outdoor conditions appear reasonable based on "
                "the available forecast."
            )

        summary = (
            f"Local AI summary: {condition}, "
            f"{self.number(temperature)}°C, "
            f"rain chance {rain_chance}% and wind "
            f"{self.number(wind)} km/h. {outdoor} "
            "AI predictions can be wrong, so verify important information."
        )

        return {
            "summary": summary,
            "rain": rain,
            "clothing": clothing,
            "travel": travel,
            "outdoor": outdoor,
            "storm": (
                "Check the Alerts section from the official weather "
                "provider and your government weather service before "
                "making safety decisions."
            ),
            "best_time": (
                "Choose an hour in the Hourly Forecast with lower rain, "
                "lower wind and a comfortable temperature."
            ),
        }

    def ask_ai(self):
        question = self.ai_question_var.get().strip().lower()

        name = self.memory.data.get(
            "profile_name",
            "User",
        )
        assistant = self.memory.data.get(
            "assistant_name",
            "Aira",
        )

        if not question:
            answer = "Type a question or say hello."

        elif any(
            greeting in question.split()
            for greeting in (
                "hello",
                "hi",
                "hey",
                "namaste",
                "नमस्ते",
            )
        ):
            answer = (
                f"Hello, {name}! I am {assistant}. "
                "Ask me about rain, clothing, travel, storms "
                "or outdoor conditions."
            )

        elif "your name" in question or "who are you" in question:
            answer = (
                f"My name is {assistant}, {name}."
            )

        elif "how are you" in question:
            answer = (
                f"I am ready and working, {name}."
            )

        elif "thank" in question:
            answer = f"You are welcome, {name}!"

        elif not self.ai_result:
            answer = (
                "Please search for a city's weather first."
            )

        elif "rain" in question or "umbrella" in question:
            answer = self.ai_result["rain"]

        elif "wear" in question or "cloth" in question:
            answer = self.ai_result["clothing"]

        elif "travel" in question or "drive" in question:
            answer = self.ai_result["travel"]

        elif "outside" in question or "outdoor" in question:
            answer = self.ai_result["outdoor"]

        elif "storm" in question or "danger" in question:
            answer = self.ai_result["storm"]

        elif "best" in question or "time" in question:
            answer = self.ai_result["best_time"]

        elif "help" in question:
            answer = (
                "Ask about rain, clothing, travel, storms, "
                "outdoor plans or the best time."
            )

        else:
            answer = self.ai_result["summary"]

        self.ai_answer_label.configure(
            text=f"{assistant}: {answer}"
        )

    def change_unit(self, event=None):
        self.memory.update(
            unit=self.unit_var.get()
        )

        if self.weather:
            self.display_weather(self.weather)

    def open_theme_palette(self):
        window = tk.Toplevel(self.root)
        window.title(f"{APP_NAME} Themes")
        window.geometry("780x610")
        window.resizable(False, False)
        window.configure(
            bg=self.colors["background"]
        )
        window.transient(self.root)

        tk.Label(
            window,
            text="Choose a Theme",
            bg=self.colors["background"],
            fg=self.colors["text"],
            font=("Segoe UI", 20, "bold"),
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 12),
        )

        grid = tk.Frame(
            window,
            bg=self.colors["background"],
        )
        grid.pack(
            fill="both",
            expand=True,
            padx=22,
        )

        for index, name in enumerate(THEMES):
            preview = get_theme(name)

            def select_theme(selected=name):
                window.destroy()
                self.memory.update(theme=selected)
                self.colors = get_theme(selected)
                self.show_dashboard()

            button = tk.Button(
                grid,
                text=name,
                command=select_theme,
                bg=preview["card"],
                fg=preview["text"],
                activebackground=preview["primary"],
                activeforeground=preview["button_text"],
                font=("Segoe UI", 10, "bold"),
                relief="flat",
                cursor="hand2",
                width=16,
                height=3,
            )
            button.grid(
                row=index // 4,
                column=index % 4,
                padx=7,
                pady=7,
                sticky="nsew",
            )

        for column in range(4):
            grid.grid_columnconfigure(
                column,
                weight=1,
            )

    def open_settings(self):
        window = tk.Toplevel(self.root)
        window.title(f"{APP_NAME} - {self.tr('settings')}")
        window.geometry("650x730")
        window.resizable(False, False)
        window.configure(
            bg=self.colors["background"]
        )
        window.transient(self.root)
        window.grab_set()

        outer = tk.Frame(
            window,
            bg=self.colors["background"],
        )
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            outer,
            bg=self.colors["background"],
            highlightthickness=0,
        )
        scrollbar = ttk.Scrollbar(
            outer,
            orient="vertical",
            command=canvas.yview,
        )
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        panel = tk.Frame(
            canvas,
            bg=self.colors["panel"],
            padx=25,
            pady=20,
        )
        panel_window = canvas.create_window(
            (20, 20),
            window=panel,
            anchor="nw",
        )

        panel.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            ),
        )
        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(
                panel_window,
                width=max(300, event.width - 45),
            ),
        )
        window.bind(
            "<MouseWheel>",
            lambda event: canvas.yview_scroll(
                int(-event.delta / 120),
                "units",
            ),
        )

        storage_mode = self.memory.data.get(
            "storage_mode",
            "Normal",
        )

        tk.Label(
            panel,
            text=(
                f"{self.tr('settings')} - "
                f"{storage_mode} storage"
            ),
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w")

        key_var = tk.StringVar()
        refresh_var = tk.StringVar(
            value=str(
                self.memory.data.get(
                    "refresh_minutes",
                    15,
                )
            )
        )
        notification_var = tk.BooleanVar(
            value=self.memory.data.get(
                "daily_notifications",
                True,
            )
        )
        notification_time_var = tk.StringVar(
            value=self.memory.data.get(
                "notification_time",
                "08:00",
            )
        )
        animation_var = tk.BooleanVar(
            value=self.memory.data.get(
                "animations",
                True,
            )
        )
        ai_mode_var = tk.StringVar(
            value=self.memory.data.get(
                "ai_mode",
                "Balanced",
            )
        )
        language_var = tk.StringVar(
            value=self.memory.data.get(
                "language",
                "English",
            )
        )
        cache_limit_var = tk.StringVar(
            value=str(
                self.memory.data.get(
                    "cache_limit_mb",
                    DEFAULT_CACHE_MB,
                )
            )
        )
        github_repository_var = tk.StringVar(
            value=self.memory.data.get(
                "github_repository",
                DEFAULT_GITHUB_REPOSITORY,
            )
        )
        update_status_var = tk.StringVar(value="")

        def check_updates_now():
            try:
                repository = normalize_github_repository(
                    github_repository_var.get()
                )
            except ValueError as error:
                messagebox.showerror(
                    "GitHub Updates",
                    str(error),
                    parent=window,
                )
                return

            github_repository_var.set(repository)
            self.check_for_updates(
                parent=window,
                repository=repository,
                status_variable=update_status_var,
            )

        tk.Label(
            panel,
            text="WeatherAPI key",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(14, 4))

        tk.Label(
            panel,
            text=(
                "A protected API key is saved."
                if self.memory.get_api_key()
                else "No API key is saved."
            ),
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=("Segoe UI", 8),
        ).pack(anchor="w")

        tk.Entry(
            panel,
            textvariable=key_var,
            show="●",
            bg=self.colors["input"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="flat",
        ).pack(
            fill="x",
            ipady=7,
            pady=(4, 5),
        )

        tk.Label(
            panel,
            text=(
                "Enter your own key. Never place a real API key "
                "directly inside published source code or an EXE."
            ),
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=("Segoe UI", 8),
            wraplength=520,
            justify="left",
        ).pack(anchor="w")

        self.button(
            panel,
            "Get a WeatherAPI Key",
            lambda: webbrowser.open(API_SIGNUP_URL),
            secondary=True,
        ).pack(anchor="w", pady=(6, 8))

        tk.Label(
            panel,
            text="GitHub update repository",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(8, 4))

        tk.Entry(
            panel,
            textvariable=github_repository_var,
            bg=self.colors["input"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="flat",
        ).pack(fill="x", ipady=7)

        tk.Label(
            panel,
            text=(
                "Public owner/repository only. The app downloads the release "
                "ZIP and verifies its SHA-256 checksum."
            ),
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=("Segoe UI", 8),
            wraplength=520,
            justify="left",
        ).pack(anchor="w", pady=(3, 4))

        self.button(
            panel,
            "Check for Updates",
            check_updates_now,
            secondary=True,
        ).pack(anchor="w", pady=(2, 3))

        tk.Label(
            panel,
            textvariable=update_status_var,
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=("Segoe UI", 8),
            wraplength=520,
            justify="left",
        ).pack(anchor="w", pady=(0, 6))

        tk.Label(
            panel,
            text=self.tr("language"),
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(5, 4))

        ttk.Combobox(
            panel,
            textvariable=language_var,
            values=tuple(LANGUAGE_CODES),
            state="readonly",
        ).pack(fill="x")

        tk.Label(
            panel,
            text=self.tr("refresh"),
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(5, 4))

        ttk.Combobox(
            panel,
            textvariable=refresh_var,
            values=("5", "10", "15", "30", "60"),
            state="readonly",
        ).pack(fill="x")

        tk.Label(
            panel,
            text=self.tr("cache_limit"),
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(10, 4))

        ttk.Combobox(
            panel,
            textvariable=cache_limit_var,
            values=("50", "100", "200", "300", "400", "500"),
            state="readonly",
        ).pack(fill="x")

        tk.Label(
            panel,
            text=self.tr("ai_mode"),
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(10, 4))

        ttk.Combobox(
            panel,
            textvariable=ai_mode_var,
            values=("Balanced", "Cautious"),
            state="readonly",
        ).pack(fill="x")

        tk.Label(
            panel,
            text=self.tr("notify_time"),
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(10, 4))

        tk.Entry(
            panel,
            textvariable=notification_time_var,
            bg=self.colors["input"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="flat",
        ).pack(fill="x", ipady=7)

        tk.Checkbutton(
            panel,
            text=self.tr("enable_notify"),
            variable=notification_var,
            bg=self.colors["panel"],
            fg=self.colors["text"],
            selectcolor=self.colors["input"],
            activebackground=self.colors["panel"],
            activeforeground=self.colors["text"],
        ).pack(anchor="w", pady=(10, 3))

        tk.Checkbutton(
            panel,
            text=self.tr("enable_animations"),
            variable=animation_var,
            bg=self.colors["panel"],
            fg=self.colors["text"],
            selectcolor=self.colors["input"],
            activebackground=self.colors["panel"],
            activeforeground=self.colors["text"],
        ).pack(anchor="w", pady=3)

        def save_settings():
            repository_text = github_repository_var.get().strip()
            if repository_text:
                try:
                    repository_text = normalize_github_repository(
                        repository_text
                    )
                except ValueError as error:
                    messagebox.showerror(
                        "GitHub Updates",
                        str(error),
                        parent=window,
                    )
                    return

            try:
                datetime.strptime(
                    notification_time_var.get().strip(),
                    "%H:%M",
                )
            except ValueError:
                messagebox.showerror(
                    APP_NAME,
                    "Notification time must use HH:MM format.",
                    parent=window,
                )
                return

            if key_var.get().strip():
                try:
                    self.memory.set_api_key(
                        key_var.get().strip()
                    )
                except ValueError as error:
                    messagebox.showerror(
                        APP_NAME,
                        str(error),
                        parent=window,
                    )
                    return

            self.memory.update(
                refresh_minutes=int(refresh_var.get()),
                ai_mode=ai_mode_var.get(),
                language=language_var.get(),
                cache_limit_mb=int(cache_limit_var.get()),
                daily_notifications=notification_var.get(),
                notification_time=(
                    notification_time_var.get().strip()
                ),
                animations=animation_var.get(),
                github_repository=repository_text,
            )
            self.memory.prune_cache()

            window.destroy()
            self.show_dashboard()

            if self.memory.get_api_key():
                self.root.after(
                    250,
                    lambda: self.search_weather(silent=True),
                )

        row = tk.Frame(
            panel,
            bg=self.colors["panel"],
        )
        row.pack(fill="x", pady=(12, 5))

        self.button(
            row,
            self.tr("save"),
            save_settings,
        ).pack(side="left")

        self.button(
            row,
            self.tr("test_notification"),
            lambda: self.send_notification(
                f"{APP_NAME} test",
                (
                    f"Hello "
                    f"{self.memory.data.get('profile_name', 'User')}. "
                    "The test notification is working."
                ),
                show_in_app=True,
            ),
            secondary=True,
        ).pack(side="left", padx=7)

        def remove_api_key():
            if messagebox.askyesno(
                APP_NAME,
                "Remove the protected API key?",
                parent=window,
            ):
                self.memory.remove_api_key()

        self.button(
            panel,
            self.tr("remove_key"),
            remove_api_key,
            secondary=True,
        ).pack(anchor="w", pady=3)

        self.button(
            panel,
            self.tr("view_disclaimer"),
            lambda: messagebox.showinfo(
                "Disclaimer",
                DISCLAIMER,
                parent=window,
            ),
            secondary=True,
        ).pack(anchor="w", pady=3)

        def clear_weather_cache():
            if messagebox.askyesno(
                APP_NAME,
                "Clear the weather cache and recent location history?",
                parent=window,
            ):
                self.memory.clear_cache()

        self.button(
            panel,
            self.tr("clear_cache"),
            clear_weather_cache,
            secondary=True,
        ).pack(anchor="w", pady=3)

        self.button(
            panel,
            self.tr("delete_all"),
            lambda: self.delete_all_data(window),
            secondary=True,
        ).pack(anchor="w", pady=3)

        self.button(
            panel,
            self.tr("restart"),
            lambda: self.restart_application(window),
            secondary=True,
        ).pack(anchor="w", pady=3)

        self.button(
            panel,
            self.tr("exit_app"),
            self.close_app,
            secondary=True,
        ).pack(anchor="w", pady=3)

    def restart_application(self, parent=None):
        first = messagebox.askyesno(
            "Restart Application - First Confirmation",
            (
                "Are you sure you want to restart "
                f"{APP_NAME}?"
            ),
            parent=parent or self.root,
        )

        if not first:
            return

        second = messagebox.askyesno(
            "Restart Application - Final Confirmation",
            (
                "This is the second confirmation. "
                "Do you really want to restart the application now?"
            ),
            parent=parent or self.root,
        )

        if not second:
            return

        if self.memory.is_temporary():
            try:
                self.configure_windows_startup(False)
            finally:
                # Temporary restart intentionally returns to the first
                # storage/disclaimer/profile experience.
                self.memory.end_temporary_session()
        else:
            # Permanent and Normal modes retain their saved state.
            self.memory.save()

        try:
            if parent and parent.winfo_exists():
                parent.grab_release()
                parent.destroy()
        except tk.TclError:
            pass

        try:
            self.root.withdraw()
            self.root.update_idletasks()

            if getattr(sys, "frozen", False):
                os.execl(
                    sys.executable,
                    sys.executable,
                )
            else:
                os.execl(
                    sys.executable,
                    sys.executable,
                    os.path.abspath(__file__),
                )
        except OSError as error:
            self.root.deiconify()
            messagebox.showerror(
                APP_NAME,
                f"The application could not restart:\n{error}",
            )

    def show_data_deletion_overlay(self):
        overlay = tk.Toplevel(self.root)
        overlay.title("Deleting App Data")
        overlay.geometry("520x220")
        overlay.resizable(False, False)
        overlay.transient(self.root)
        overlay.attributes("-topmost", True)
        overlay.configure(bg=self.colors["panel"])
        overlay.protocol("WM_DELETE_WINDOW", lambda: None)

        overlay.update_idletasks()
        x = max(
            0,
            self.root.winfo_rootx()
            + (self.root.winfo_width() - 520) // 2,
        )
        y = max(
            0,
            self.root.winfo_rooty()
            + (self.root.winfo_height() - 220) // 2,
        )
        overlay.geometry(f"520x220+{x}+{y}")

        tk.Label(
            overlay,
            text="Deleting data immediately...",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 17, "bold"),
        ).pack(pady=(35, 8))

        tk.Label(
            overlay,
            text=(
                "Please wait. The starting disclaimer might take a "
                "little time to open when a large weather cache is removed."
            ),
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=("Segoe UI", 10),
            wraplength=440,
            justify="center",
        ).pack(padx=25)

        progress = ttk.Progressbar(
            overlay,
            mode="indeterminate",
            length=420,
        )
        progress.pack(pady=(20, 10))
        progress.start(10)
        overlay.grab_set()
        self.root.update_idletasks()
        return overlay, progress

    def delete_all_data(self, settings_window):
        first = messagebox.askyesno(
            "First Confirmation",
            (
                "Delete your profile, protected API key, "
                "settings, history and weather cache?"
            ),
            parent=settings_window,
        )

        if not first:
            return

        second = simpledialog.askstring(
            "Second Confirmation",
            "Type DELETE to permanently remove all app data.",
            parent=settings_window,
        )

        if second != "DELETE":
            messagebox.showinfo(
                APP_NAME,
                "Deletion cancelled.",
                parent=settings_window,
            )
            return

        self.deleting_data = True
        self.loading = False

        try:
            settings_window.grab_release()
        except tk.TclError:
            pass
        settings_window.destroy()

        overlay, progress = self.show_data_deletion_overlay()
        started_at = time.monotonic()
        result_queue = queue.Queue(maxsize=1)

        def deletion_finished(error_message=""):
            progress.stop()

            try:
                overlay.grab_release()
                overlay.destroy()
            except tk.TclError:
                pass

            self.deleting_data = False
            self.configure_windows_startup(False)

            self.weather = None
            self.ai_result = None
            self.city_var.set("")
            self.city_suggestions = []
            self.colors = get_theme("Kaja Blue")

            if error_message:
                messagebox.showwarning(
                    APP_NAME,
                    (
                        "Some data could not be removed completely:\n"
                        f"{error_message}"
                    ),
                    parent=self.root,
                )

            # Opening the disclaimer in the existing process is faster
            # than closing and relaunching the whole application.
            self.show_disclaimer()

        def delete_worker():
            error_message = ""

            try:
                self.memory.delete_all()
            except Exception as error:
                error_message = str(error)

            result_queue.put(error_message)

        def poll_delete_worker():
            try:
                error_message = result_queue.get_nowait()
            except queue.Empty:
                if self.deleting_data:
                    self.root.after(40, poll_delete_worker)
                return

            elapsed_ms = int(
                (time.monotonic() - started_at) * 1000
            )
            remaining_ms = max(0, 300 - elapsed_ms)

            self.root.after(
                remaining_ms,
                lambda message=error_message: deletion_finished(
                    message
                ),
            )

        threading.Thread(
            target=delete_worker,
            daemon=True,
        ).start()
        self.root.after(40, poll_delete_worker)

    def configure_windows_startup(self, enabled):
        registry_path = (
            r"Software\Microsoft\Windows"
            r"\CurrentVersion\Run"
        )

        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                registry_path,
                0,
                winreg.KEY_SET_VALUE,
            ) as key:
                if enabled:
                    if getattr(sys, "frozen", False):
                        command = f'"{sys.executable}"'
                    else:
                        python_executable = sys.executable

                        if python_executable.lower().endswith(
                            "python.exe"
                        ):
                            pythonw = (
                                python_executable[:-10]
                                + "pythonw.exe"
                            )

                            if os.path.isfile(pythonw):
                                python_executable = pythonw

                        command = (
                            f'"{python_executable}" '
                            f'"{os.path.abspath(__file__)}"'
                        )

                    winreg.SetValueEx(
                        key,
                        "KajaGuruWeatherApp",
                        0,
                        winreg.REG_SZ,
                        command,
                    )
                else:
                    try:
                        winreg.DeleteValue(
                            key,
                            "KajaGuruWeatherApp",
                        )
                    except FileNotFoundError:
                        pass

        except OSError:
            if enabled:
                messagebox.showwarning(
                    APP_NAME,
                    "Windows startup could not be enabled.",
                )

    def send_notification(
        self,
        title,
        message,
        show_in_app=False,
    ):
        if show_in_app:
            self.show_in_app_notification(
                title,
                message,
            )

        def worker():
            try:
                if Notification is None:
                    raise RuntimeError(
                        "winotify is not installed"
                    )

                notification = Notification(
                    app_id=APP_NAME,
                    title=str(title),
                    msg=str(message),
                    icon=(
                        os.path.abspath(LOGO_PATH)
                        if os.path.isfile(LOGO_PATH)
                        else ""
                    ),
                )

                if audio is not None:
                    notification.set_audio(
                        audio.Default,
                        loop=False,
                    )

                notification.show()

            except Exception:
                if not show_in_app:
                    try:
                        self.root.after(
                            0,
                            lambda: self.show_in_app_notification(
                                title,
                                message,
                            ),
                        )
                    except tk.TclError:
                        pass

        threading.Thread(
            target=worker,
            daemon=True,
        ).start()

    def show_in_app_notification(
        self,
        title,
        message,
    ):
        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)
        popup.configure(
            bg=self.colors["panel"]
        )

        width = 390
        height = 140
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()

        target_x = screen_width - width - 24
        y = screen_height - height - 65

        popup.geometry(
            f"{width}x{height}+{screen_width}+{y}"
        )

        tk.Button(
            popup,
            text="×",
            command=popup.destroy,
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            activebackground=self.colors["card"],
            activeforeground=self.colors["text"],
            relief="flat",
            cursor="hand2",
        ).place(
            relx=1.0,
            x=-8,
            y=7,
            anchor="ne",
        )

        tk.Label(
            popup,
            text=title,
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 11, "bold"),
        ).pack(
            anchor="w",
            padx=16,
            pady=(15, 3),
        )

        tk.Label(
            popup,
            text=message,
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=("Segoe UI", 9),
            wraplength=350,
            justify="left",
        ).pack(
            anchor="w",
            padx=16,
        )

        if self.memory.data.get("animations", True):
            distance = screen_width - target_x

            for step in range(1, 13):
                x = round(
                    screen_width
                    - distance * (step / 12)
                )

                popup.after(
                    step * 18,
                    lambda value=x: popup.geometry(
                        f"{width}x{height}+{value}+{y}"
                    ),
                )
        else:
            popup.geometry(
                f"{width}x{height}+{target_x}+{y}"
            )

        popup.after(
            7000,
            popup.destroy,
        )

    def check_daily_notification(self):
        if not self.memory.data.get(
            "daily_notifications",
            True,
        ):
            return

        if not self.weather:
            return

        now = datetime.now()
        today = now.date().isoformat()

        if (
            self.memory.data.get(
                "last_notification_date"
            )
            == today
        ):
            return

        notification_time = self.memory.data.get(
            "notification_time",
            "08:00",
        )

        if now.strftime("%H:%M") < notification_time:
            return

        location = self.weather.get(
            "location",
            {},
        )
        current = self.weather.get(
            "current",
            {},
        )

        forecast_days = self.weather.get(
            "forecast",
            {},
        ).get("forecastday", [])

        if not forecast_days:
            return

        day = forecast_days[0].get("day", {})

        user_name = self.memory.data.get(
            "profile_name",
            "User",
        )
        assistant_name = self.memory.data.get(
            "assistant_name",
            "Aira",
        )

        title = (
            f"{assistant_name}'s Daily Forecast"
        )

        message = (
            f"Good morning {user_name}. "
            f"{location.get('name', 'Your city')}: "
            f"{current.get('condition', {}).get('text', 'Weather')}, "
            f"{self.number(current.get('temp_c'))}°C now. "
            f"High {self.number(day.get('maxtemp_c'))}°C, "
            f"low {self.number(day.get('mintemp_c'))}°C, "
            f"rain chance "
            f"{day.get('daily_chance_of_rain', 0)}%."
        )

        self.send_notification(
            title,
            message,
            show_in_app=True,
        )

        self.memory.update(
            last_notification_date=today
        )

    def check_for_updates(
        self,
        parent=None,
        repository=None,
        status_variable=None,
    ):
        if self.update_in_progress:
            return

        try:
            repository = normalize_github_repository(
                repository
                or self.memory.data.get("github_repository", "")
            )
        except ValueError as error:
            messagebox.showinfo(
                "GitHub Updates",
                (
                    f"{error}\n\n"
                    "The repository must be public. No GitHub token is "
                    "stored by this app."
                ),
                parent=parent or self.root,
            )
            return

        self.memory.update(github_repository=repository)
        self.update_in_progress = True

        if status_variable is not None:
            status_variable.set("Checking GitHub for a newer release...")

        result_queue = queue.Queue(maxsize=1)

        def update_worker():
            work_directory = ""
            pending_directory = ""

            try:
                release = read_github_latest_release(repository)
                release_tag = str(release.get("tag_name", "")).strip()

                if not release_tag:
                    raise WeatherError(
                        "The latest GitHub release has no version tag."
                    )

                if version_key(release_tag) <= version_key(APP_VERSION):
                    result_queue.put(
                        {
                            "result": "up_to_date",
                            "tag": release_tag,
                        }
                    )
                    return

                if not getattr(sys, "frozen", False):
                    result_queue.put(
                        {
                            "result": "source_update",
                            "tag": release_tag,
                        }
                    )
                    return

                assets = {
                    str(asset.get("name", "")): asset
                    for asset in release.get("assets", [])
                    if isinstance(asset, dict)
                }
                package_asset = assets.get(UPDATE_PACKAGE_NAME)
                checksum_asset = assets.get(UPDATE_CHECKSUM_NAME)

                if not package_asset or not checksum_asset:
                    raise WeatherError(
                        "The release must contain both "
                        f"{UPDATE_PACKAGE_NAME} and "
                        f"{UPDATE_CHECKSUM_NAME}."
                    )

                package_url = package_asset.get("browser_download_url")
                checksum_url = checksum_asset.get("browser_download_url")
                if not package_url or not checksum_url:
                    raise WeatherError(
                        "GitHub did not provide valid release download URLs."
                    )

                work_directory = tempfile.mkdtemp(
                    prefix="KajaGuruWeatherUpdate_"
                )
                package_path = os.path.join(
                    work_directory,
                    UPDATE_PACKAGE_NAME,
                )
                checksum_path = os.path.join(
                    work_directory,
                    UPDATE_CHECKSUM_NAME,
                )

                download_update_file(package_url, package_path)
                download_update_file(checksum_url, checksum_path)

                with open(
                    checksum_path,
                    "r",
                    encoding="utf-8",
                    errors="replace",
                ) as checksum_file:
                    checksum_text = checksum_file.read(4096)

                checksum_match = re.search(
                    r"\b([A-Fa-f0-9]{64})\b",
                    checksum_text,
                )
                if not checksum_match:
                    raise WeatherError(
                        "The release checksum file is invalid."
                    )

                expected_checksum = checksum_match.group(1).lower()
                if file_sha256(package_path) != expected_checksum:
                    raise WeatherError(
                        "The downloaded update failed SHA-256 verification."
                    )

                extraction_directory = os.path.join(
                    work_directory,
                    "extracted",
                )
                safely_extract_update(
                    package_path,
                    extraction_directory,
                )
                package_root = find_update_package_root(
                    extraction_directory
                )

                current_directory = os.path.dirname(sys.executable)
                pending_directory = current_directory + ".update-new"
                if os.path.isdir(pending_directory):
                    shutil.rmtree(pending_directory)

                shutil.copytree(package_root, pending_directory)

                result_queue.put(
                    {
                        "result": "ready",
                        "tag": release_tag,
                        "pending_directory": pending_directory,
                    }
                )

            except HTTPError as error:
                if os.path.isdir(pending_directory):
                    shutil.rmtree(pending_directory, ignore_errors=True)

                if error.code == 404:
                    message = (
                        "No public GitHub Release was found for this "
                        "repository."
                    )
                elif error.code == 403:
                    message = (
                        "GitHub temporarily refused the update check. "
                        "Please try again later."
                    )
                else:
                    message = f"GitHub returned HTTP error {error.code}."

                result_queue.put({"result": "error", "message": message})

            except (URLError, OSError, TypeError, ValueError,
                    json.JSONDecodeError,
                    zipfile.BadZipFile, WeatherError) as error:
                if os.path.isdir(pending_directory):
                    shutil.rmtree(pending_directory, ignore_errors=True)
                result_queue.put(
                    {
                        "result": "error",
                        "message": str(error),
                    }
                )

            finally:
                if work_directory:
                    shutil.rmtree(work_directory, ignore_errors=True)

        def valid_parent():
            try:
                if parent is not None and parent.winfo_exists():
                    return parent
            except tk.TclError:
                pass
            return self.root

        def poll_update_result():
            try:
                result = result_queue.get_nowait()
            except queue.Empty:
                try:
                    self.root.after(100, poll_update_result)
                except tk.TclError:
                    pass
                return

            outcome = result.get("result")
            if outcome == "ready":
                if status_variable is not None:
                    status_variable.set(
                        "Verified update downloaded. Restarting quietly..."
                    )
                try:
                    self.install_verified_update(
                        result["pending_directory"],
                        result.get("tag", ""),
                    )
                except OSError as error:
                    self.update_in_progress = False
                    shutil.rmtree(
                        result.get("pending_directory", ""),
                        ignore_errors=True,
                    )
                    messagebox.showerror(
                        "GitHub Updates",
                        f"The update could not be installed:\n{error}",
                        parent=valid_parent(),
                    )
                return

            self.update_in_progress = False

            if outcome == "up_to_date":
                text = f"You already have the latest version ({APP_VERSION})."
                if status_variable is not None:
                    status_variable.set(text)
                messagebox.showinfo(
                    "GitHub Updates",
                    text,
                    parent=valid_parent(),
                )
            elif outcome == "source_update":
                text = (
                    f"Version {result.get('tag')} is available. Automatic "
                    "installation works in the packaged Windows app."
                )
                if status_variable is not None:
                    status_variable.set(text)
                messagebox.showinfo(
                    "GitHub Updates",
                    text,
                    parent=valid_parent(),
                )
            else:
                text = result.get("message") or "The update check failed."
                if status_variable is not None:
                    status_variable.set(text)
                messagebox.showerror(
                    "GitHub Updates",
                    text,
                    parent=valid_parent(),
                )

        threading.Thread(
            target=update_worker,
            daemon=True,
        ).start()
        self.root.after(100, poll_update_result)

    def install_verified_update(self, pending_directory, release_tag):
        target_directory = os.path.dirname(sys.executable)
        backup_directory = target_directory + ".update-backup"
        executable_path = os.path.join(
            target_directory,
            f"{APP_NAME}.exe",
        )
        log_path = os.path.join(
            tempfile.gettempdir(),
            "KajaGuruWeatherApp-update.log",
        )
        script_path = os.path.join(
            tempfile.gettempdir(),
            f"KajaGuruWeatherApp-update-{os.getpid()}.ps1",
        )

        def powershell_literal(value):
            return "'" + str(value).replace("'", "''") + "'"

        script = f"""
$ErrorActionPreference = 'Stop'
$target = {powershell_literal(target_directory)}
$pending = {powershell_literal(pending_directory)}
$backup = {powershell_literal(backup_directory)}
$executable = {powershell_literal(executable_path)}
$log = {powershell_literal(log_path)}
$processId = {os.getpid()}

try {{
    $deadline = (Get-Date).AddSeconds(90)
    while (Get-Process -Id $processId -ErrorAction SilentlyContinue) {{
        if ((Get-Date) -ge $deadline) {{
            throw 'The running app did not close in time.'
        }}
        Start-Sleep -Milliseconds 200
    }}

    if (Test-Path -LiteralPath $backup) {{
        Remove-Item -LiteralPath $backup -Recurse -Force
    }}
    if (-not (Test-Path -LiteralPath $pending)) {{
        throw 'The verified update folder is missing.'
    }}

    Move-Item -LiteralPath $target -Destination $backup
    try {{
        Move-Item -LiteralPath $pending -Destination $target
    }} catch {{
        Move-Item -LiteralPath $backup -Destination $target
        throw
    }}

    Start-Process -FilePath $executable
    Start-Sleep -Seconds 2
    if (Test-Path -LiteralPath $backup) {{
        Remove-Item -LiteralPath $backup -Recurse -Force
    }}
    if (Test-Path -LiteralPath $log) {{
        Remove-Item -LiteralPath $log -Force
    }}
}} catch {{
    $message = $_.Exception.Message
    try {{
        if ((-not (Test-Path -LiteralPath $target)) -and
            (Test-Path -LiteralPath $backup)) {{
            Move-Item -LiteralPath $backup -Destination $target
        }}
        if (Test-Path -LiteralPath $executable) {{
            Start-Process -FilePath $executable
        }}
    }} catch {{}}
    Set-Content -LiteralPath $log -Value $message -Encoding UTF8
}}

Start-Sleep -Seconds 1
Remove-Item -LiteralPath $PSCommandPath -Force -ErrorAction SilentlyContinue
"""

        with open(script_path, "w", encoding="utf-8") as script_file:
            script_file.write(script)

        creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        subprocess.Popen(
            [
                "powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-ExecutionPolicy",
                "Bypass",
                "-WindowStyle",
                "Hidden",
                "-File",
                script_path,
            ],
            close_fds=True,
            creationflags=creation_flags,
            cwd=tempfile.gettempdir(),
        )

        self.root.withdraw()
        self.root.after(250, self.root.destroy)

    def background_tasks(self):
        try:
            if hasattr(self, "clock_label"):
                self.clock_label.configure(
                    text=datetime.now().strftime(
                        "%A, %d %B %Y • %H:%M:%S"
                    )
                )

            self.memory.prune_cache()
            self.check_daily_notification()

            refresh_seconds = (
                int(
                    self.memory.data.get(
                        "refresh_minutes",
                        15,
                    )
                )
                * 60
            )

            dashboard_exists = (
                hasattr(self, "search_button")
                and self.search_button.winfo_exists()
            )

            if (
                dashboard_exists
                and not self.loading
                and not self.deleting_data
                and self.memory.get_api_key()
                and time.time() - self.last_fetch_time
                >= refresh_seconds
            ):
                query = (
                    self.memory.data.get("last_query")
                    or self.memory.data.get(
                        "home_city",
                        "",
                    )
                )

                if query:
                    self.search_weather(
                        query=query,
                        silent=True,
                    )

            self.root.after(
                30_000,
                self.background_tasks,
            )

        except tk.TclError:
            pass

    def close_app(self):
        if self.deleting_data:
            messagebox.showwarning(
                APP_NAME,
                (
                    "Data deletion is still running. The starting disclaimer "
                    "might take a little time to open. Please wait."
                ),
                parent=self.root,
            )
            return

        try:
            if self.memory.is_temporary():
                try:
                    self.configure_windows_startup(False)
                finally:
                    self.memory.end_temporary_session()
        finally:
            try:
                self.root.quit()
            except tk.TclError:
                pass

            try:
                self.root.destroy()
            except tk.TclError:
                pass

    @staticmethod
    def condition_icon(condition):
        text = str(condition).lower()

        if "thunder" in text:
            return "⛈️"
        if "snow" in text or "sleet" in text:
            return "❄️"
        if "rain" in text or "drizzle" in text:
            return "🌧️"
        if "fog" in text or "mist" in text:
            return "🌫️"
        if "overcast" in text:
            return "☁️"
        if "cloud" in text:
            return "⛅"
        if "sunny" in text or "clear" in text:
            return "☀️"

        return "🌡️"

    @staticmethod
    def number(value):
        if value is None:
            return "--"

        try:
            value = float(value)

            if value.is_integer():
                return str(int(value))

            return f"{value:.1f}"

        except (TypeError, ValueError):
            return str(value)


def main():
    if os.name != "nt":
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            APP_NAME,
            "Kaja Guru Weather App supports Windows only.",
        )
        root.destroy()
        return

    root = tk.Tk()
    KajaGuruWeatherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
