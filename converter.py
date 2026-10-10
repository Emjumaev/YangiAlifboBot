"""
Eski (1995) o'zbek lotin alifbosidan 2026-yilgi yangi lotin alifbosiga o'tkazish.

O'zgarishlar:
    O‘ o‘  ->  Ö ö
    G‘ g‘  ->  Ğ ğ
    Sh sh  ->  Ş ş
    Ch ch  ->  Ç ç

Qolgan harflar (ng, ya, yo, yu, ye, ts, tutuq belgisi ʼ) o'zgarmaydi.
"""

import re

# Foydalanuvchilar o‘/g‘ ni turlicha teradi: ‘ ’ ' ` ʻ ʼ ´ ʹ
_APOS = "‘’'`ʻʼ´ʹ"

# o‘ / g‘  (apostrof variantlaridan qat'i nazar)
_RE_O = re.compile(rf"([Oo])[{_APOS}]")
_RE_G = re.compile(rf"([Gg])[{_APOS}]")

# Eski imloda s va h alohida talaffuz qilinishini ko'rsatish uchun
# "s'h" yoziladi (Is'hoq, as'hob). Yangi alifboda ş alohida harf
# bo'lgani uchun ajratuvchi belgi kerak emas: s'h -> sh.
_RE_S_H = re.compile(rf"([Ss])[{_APOS}]([Hh])")

_SEP = "\ue000"  # vaqtinchalik ajratuvchi (Private Use Area)

# sh / ch digraflari
_RE_SH = re.compile(r"[Ss][Hh]")
_RE_CH = re.compile(r"[Cc][Hh]")


def _digraph(first_upper_char: str, lower: str, upper: str):
    """Bosh harf katta bo'lsa katta harf, aks holda kichik harf qaytaradi."""
    def repl(m: re.Match) -> str:
        return upper if m.group(0)[0].isupper() else lower
    return repl


def to_new(text: str) -> str:
    """Eski lotin -> yangi lotin."""
    if not text:
        return text
    text = _RE_O.sub(lambda m: "Ö" if m.group(1) == "O" else "ö", text)
    text = _RE_G.sub(lambda m: "Ğ" if m.group(1) == "G" else "ğ", text)
    # s'h -> s + h; digraf almashinuvidan himoya qilish uchun vaqtincha belgi qo'yamiz
    text = _RE_S_H.sub(lambda m: m.group(1) + _SEP + m.group(2), text)
    text = _RE_SH.sub(_digraph("S", "ş", "Ş"), text)
    text = _RE_CH.sub(_digraph("C", "ç", "Ç"), text)
    return text.replace(_SEP, "")


_NEW_TO_OLD = {
    "Ö": "O‘", "ö": "o‘",
    "Ğ": "G‘", "ğ": "g‘",
    "Ş": "Sh", "ş": "sh",
    "Ç": "Ch", "ç": "ch",
}
_RE_NEW = re.compile("[ÖöĞğŞşÇç]")


def to_old(text: str) -> str:
    """Yangi lotin -> eski lotin (teskari yo'nalish)."""
    if not text:
        return text

    def repl(m: re.Match) -> str:
        ch = m.group(0)
        out = _NEW_TO_OLD[ch]
        # Butunlay katta harfli so'zlarda (ŞAHAR -> SHAHAR) ikkinchi harf ham katta
        if ch in "ŞÇ":
            start, end = m.start(), m.end()
            nxt = text[end:end + 1]
            prv = text[start - 1:start] if start > 0 else ""
            if (nxt and nxt.isupper()) or (prv and prv.isupper()):
                out = out.upper()
        return out

    # s + h ketma-ketligi (Ishoq) eski imloda s'h deb ajratiladi —
    # buni ş -> sh almashinuvidan OLDIN qilamiz
    text = re.sub(r"([Ss])([Hh])", r"\1ʼ\2", text)
    return _RE_NEW.sub(repl, text)


# --- Avtomatik aniqlash -----------------------------------------------------

_RE_OLD_MARKERS = re.compile(rf"[OoGg][{_APOS}]|[Ss][Hh]|[Cc][Hh]")
_RE_NEW_MARKERS = re.compile("[ÖöĞğŞşÇç]")


def detect(text: str) -> str:
    """Matn qaysi alifboda ekanini taxmin qiladi: "new" yoki "old".

    Yangi harflar (Ö Ğ Ş Ç) eski belgilardan (o‘ g‘ sh ch) ko'p bo'lsa — "new".
    Hech qanday belgi bo'lmasa (masalan "salom") — "old" (standart: yangiga o'giriladi).
    """
    new_count = len(_RE_NEW_MARKERS.findall(text or ""))
    old_count = len(_RE_OLD_MARKERS.findall(text or ""))
    return "new" if new_count > old_count else "old"


def convert_auto(text: str):
    """Alifboni aniqlab qarama-qarshi tomonga o'giradi.

    Qaytaradi: (natija, yo'nalish) — yo'nalish "to_new" yoki "to_old".
    """
    if detect(text) == "new":
        return to_old(text), "to_old"
    return to_new(text), "to_new"
