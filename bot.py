"""Yangi Alifbo Bot — eski o'zbek lotin alifbosini 2026-yilgi yangi alifboga o'tkazadi."""

import logging
import os
from io import BytesIO

from dotenv import load_dotenv
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    InlineQueryHandler,
    MessageHandler,
    filters,
)

from converter import to_new, to_old

load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise SystemExit("BOT_TOKEN topilmadi. .env faylga BOT_TOKEN=... yozing.")

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger("yangialifbo")

MAX_FILE_BYTES = 5 * 1024 * 1024  # 5 MB
MODE_KEY = "mode"  # "new" (default) yoki "old"

START_TEXT = (
    "Assalomu alaykum! 👋\n\n"
    "Men eski lotin alifbosidagi matnni <b>2026-yilgi yangi alifboga</b> o‘tkazib beraman.\n\n"
    "<b>O‘zgargan harflar:</b>\n"
    "O‘ o‘ → Ö ö\n"
    "G‘ g‘ → Ğ ğ\n"
    "Sh sh → Ş ş\n"
    "Ch ch → Ç ç\n\n"
    "Menga matn yuboring yoki <code>.txt</code> fayl tashlang — javobini qaytaraman.\n\n"
    "<b>Buyruqlar:</b>\n"
    "/yangi — eski → yangi (standart)\n"
    "/eski — yangi → eski (teskari)\n"
    "/help — yordam"
)

HELP_TEXT = (
    "<b>Qanday ishlataman?</b>\n\n"
    "1. Matn yuboring — konvertatsiya qilingan matn qaytadi.\n"
    "2. <code>.txt</code> fayl yuboring — konvertatsiya qilingan fayl qaytadi (5 MB gacha).\n"
    "3. Istalgan chatda <code>@bot_nomi matn</code> deb yozing (inline rejim).\n\n"
    "<b>Yo‘nalish:</b>\n"
    "/yangi — eski alifbo → yangi alifbo\n"
    "/eski — yangi alifbo → eski alifbo\n\n"
    "<b>Eslatma:</b> o‘ va g‘ dagi apostrofning qaysi ko‘rinishi (‘ ’ ' `) ishlatilgani ahamiyatsiz — "
    "hammasini tushunaman. Tutuq belgisi (ma’no, e’lon) o‘zgarmaydi."
)


def _convert(context: ContextTypes.DEFAULT_TYPE, text: str) -> str:
    mode = context.user_data.get(MODE_KEY, "new")
    return to_old(text) if mode == "old" else to_new(text)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(START_TEXT, parse_mode=ParseMode.HTML)


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_TEXT, parse_mode=ParseMode.HTML)


async def cmd_mode_new(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data[MODE_KEY] = "new"
    await update.message.reply_text("✅ Rejim: eski alifbo → yangi alifbo (Ö Ğ Ş Ç)")


async def cmd_mode_old(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data[MODE_KEY] = "old"
    await update.message.reply_text("✅ Rejim: yangi alifbo → eski alifbo (O‘ G‘ Sh Ch)")


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    result = _convert(context, text)
    # Telegram bitta xabarda 4096 belgi qabul qiladi
    for i in range(0, len(result), 4096):
        await update.message.reply_text(result[i : i + 4096])


async def on_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    doc = update.message.document
    name = doc.file_name or "matn.txt"
    if not name.lower().endswith(".txt"):
        await update.message.reply_text("Faqat .txt fayllarni qabul qilaman.")
        return
    if doc.file_size and doc.file_size > MAX_FILE_BYTES:
        await update.message.reply_text("Fayl juda katta (maksimum 5 MB).")
        return

    tg_file = await doc.get_file()
    raw = bytes(await tg_file.download_as_bytearray())
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("cp1251", errors="replace")

    result = _convert(context, text)
    out = BytesIO(result.encode("utf-8"))
    stem = name[:-4]
    suffix = "eski" if context.user_data.get(MODE_KEY) == "old" else "yangi"
    out.name = f"{stem}_{suffix}.txt"
    await update.message.reply_document(out, caption="Tayyor ✅")


async def on_inline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = (update.inline_query.query or "").strip()
    if not query:
        return
    new = to_new(query)
    old = to_old(query)
    results = [
        InlineQueryResultArticle(
            id="new",
            title="Yangi alifbo (Ö Ğ Ş Ç)",
            description=new[:100],
            input_message_content=InputTextMessageContent(new),
        ),
        InlineQueryResultArticle(
            id="old",
            title="Eski alifbo (O‘ G‘ Sh Ch)",
            description=old[:100],
            input_message_content=InputTextMessageContent(old),
        ),
    ]
    await update.inline_query.answer(results, cache_time=0)


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.exception("Xatolik: %s", context.error)


def main() -> None:
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("yangi", cmd_mode_new))
    app.add_handler(CommandHandler("eski", cmd_mode_old))
    app.add_handler(MessageHandler(filters.Document.ALL, on_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_handler(InlineQueryHandler(on_inline))
    app.add_error_handler(on_error)
    log.info("Bot ishga tushdi")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
