"""Barcha botlarga nom, tavsif, buyruqlar va profil rasmini o'rnatadi.

Ishlatish:  BOT_TOKENS=tok1,tok2 python setup_bots.py
(yoki .env faylga BOT_TOKENS=... yozing)
"""
import json
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()
TOKENS = [t.strip() for t in os.environ.get("BOT_TOKENS", "").split(",") if t.strip()]
if not TOKENS:
    sys.exit("BOT_TOKENS bo'sh. .env ga BOT_TOKENS=tok1,tok2,... yozing.")

NAME = "Yangi Alifbo · Ö Ğ Ş Ç"
SHORT = "Eski lotin ⇄ 2026-yilgi yangi o‘zbek alifbosi. Matn yoki .txt yuboring."
DESCRIPTION = (
    "Eski o‘zbek lotin alifbosidagi matnni 2026-yilgi yangi alifboga o‘tkazib beraman "
    "(va aksincha).\n\n"
    "O‘ o‘ → Ö ö\n"
    "G‘ g‘ → Ğ ğ\n"
    "Sh sh → Ş ş\n"
    "Ch ch → Ç ç\n\n"
    "Matn yoki .txt fayl yuboring — alifboni o‘zim aniqlab, qarama-qarshi tomonga o‘giraman. "
    "Inline rejim: istalgan chatda @bot_nomi matn."
)
COMMANDS = [
    {"command": "start", "description": "Botni ishga tushirish"},
    {"command": "avto", "description": "Alifboni avtomatik aniqlash (standart)"},
    {"command": "yangi", "description": "Har doim eski → yangi alifbo"},
    {"command": "eski", "description": "Har doim yangi → eski alifbo"},
    {"command": "help", "description": "Yordam"},
]


def call(token, method, **kwargs):
    r = requests.post(f"https://api.telegram.org/bot{token}/{method}", timeout=30, **kwargs)
    data = r.json()
    if not data.get("ok"):
        print(f"   ✗ {method}: {data.get('description')}")
    return data.get("ok", False)


for token in TOKENS:
    me = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=30).json()
    if not me.get("ok"):
        print(f"✗ token noto'g'ri: {token[:10]}...")
        continue
    print(f"@{me['result']['username']}")
    ok = all([
        call(token, "setMyName", json={"name": NAME}),
        call(token, "setMyShortDescription", json={"short_description": SHORT}),
        call(token, "setMyDescription", json={"description": DESCRIPTION}),
        call(token, "setMyCommands", json={"commands": COMMANDS}),
    ])
    with open("logo.png", "rb") as f:
        ok &= call(
            token,
            "setMyProfilePhoto",
            data={"photo": json.dumps({"type": "static", "photo": "attach://logo"})},
            files={"logo": ("logo.png", f, "image/png")},
        )
    print("   ✓ hammasi o'rnatildi" if ok else "   ! ba'zi sozlamalar o'rnatilmadi")
