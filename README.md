# Yangi Alifbo Bot

Eski o‘zbek lotin alifbosidagi matnni 2026-yilgi yangi lotin alifbosiga o‘tkazuvchi Telegram bot.

| Eski | Yangi |
|------|-------|
| O‘ o‘ | Ö ö |
| G‘ g‘ | Ğ ğ |
| Sh sh | Ş ş |
| Ch ch | Ç ç |

## Imkoniyatlar

- Matn yuborsangiz — konvertatsiya qilingan matn qaytadi
- `.txt` fayl yuborsangiz — konvertatsiya qilingan fayl qaytadi
- Guruhda: botni qo‘shib, xabarga reply qilib `/avto` (yoki `/yangi`, `/eski`) yozing
- Inline rejim: istalgan chatda `@bot_nomi matn` (BotFather’da `/setinline` orqali yoqiladi)
- Alifbo avtomatik aniqlanadi: eski matn → yangi, yangi matn → eski (`/avto`, standart)
- `/yangi` — har doim eski → yangi, `/eski` — har doim yangi → eski

## Ishga tushirish

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # BOT_TOKEN ni yozing
python bot.py
```

## Testlar

```bash
pytest
```

## Heroku’ga deploy qilish

```bash
heroku login
heroku create yangi-alifbo-bot          # nom bo‘sh bo‘lsa boshqasini tanlang
heroku config:set BOT_TOKEN=<token>
git push heroku debug:main              # yoki main:main
heroku ps:scale worker=1
heroku logs --tail
```

Beshta app bor, hammasi bir xil kod:

| App | Remote | Bot |
|-----|--------|-----|
| yangi-alifbo-bot | heroku | @yangialibfo_bot |
| yangi-alifbe-bot | heroku-2 | @yangi_alifbe_bot |
| yangi-alibfo-bot | heroku-3 | @yangi_alibfo_bot |
| yangi-alifbu-bot | heroku-4 | @yangi_alifbu_bot |
| yangi-alifba-bot | heroku-5 | @yangi_alifba_bot |

Hammasiga push qilish: `for r in heroku heroku-2 heroku-3 heroku-4 heroku-5; do git push $r main; done`

Bot `worker` dyno sifatida polling rejimida ishlaydi (`Procfile`). Token faqat `heroku config` orqali beriladi, repoda saqlanmaydi.

## Bot profili (nom, tavsif, buyruqlar, rasm)

```bash
python make_logo.py      # logo.png yaratadi
python setup_bots.py     # .env dagi BOT_TOKENS=tok1,tok2,... ro‘yxatidagi barcha botlarga qo‘llaydi
```
