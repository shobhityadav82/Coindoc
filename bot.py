import logging
import os

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    BotCommand,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)


# ============================================================
# CONFIGURATION
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

BOT_NAME = "Coindocbot"

VIDEO_BOT_USERNAME = "VidoMate82bot"

WEB_CODE_GITHUB = "https://github.com/shobhityadav82/webcode.git"

# Telegram link for the video downloader bot
VIDEO_BOT_URL = f"https://t.me/{VIDEO_BOT_USERNAME}"


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ============================================================
# KEYBOARD
# ============================================================

def main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "🎬 Video Downloader Bot",
                url=VIDEO_BOT_URL
            )
        ],
        [
            InlineKeyboardButton(
                "💻 Web Code GitHub",
                url=WEB_CODE_GITHUB
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ️ About",
                callback_data="about"
            ),
            InlineKeyboardButton(
                "❓ Help",
                callback_data="help"
            ),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# ============================================================
# START MESSAGE
# ============================================================

START_MESSAGE = """
Hey there! 👋

My name is Coindocbot.

I'm a simple Telegram bot created to provide quick access
to useful projects and tools.

🎬 Video Downloader
Use my video downloader bot:
@VidoMate82bot

💻 Web Code
You can find the Web Code project on GitHub:
https://github.com/shobhityadav82/webcode.git

Choose an option below 👇
"""


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    if not update.message:
        return

    user = update.effective_user

    logger.info(
        "User started bot: %s (%s)",
        user.full_name if user else "Unknown",
        user.id if user else "Unknown",
    )

    await update.message.reply_text(
        START_MESSAGE,
        reply_markup=main_keyboard(),
        disable_web_page_preview=True,
    )


# ============================================================
# HELP
# ============================================================

HELP_MESSAGE = """
❓ Help

Available commands:

/start - Start the bot
/help - Show help
/about - About this bot

You can also use the buttons below to open
the available projects.
"""


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    if not update.message:
        return

    await update.message.reply_text(
        HELP_MESSAGE,
        reply_markup=main_keyboard(),
    )


# ============================================================
# ABOUT
# ============================================================

ABOUT_MESSAGE = """
ℹ️ About Coindocbot

Coindocbot is a Telegram utility bot created by
Shobhit Yadav.

Projects:

🎬 Video Downloader
@VidoMate82bot

💻 Web Code
A browser-based HTML, CSS and JavaScript coding project.

GitHub:
https://github.com/shobhityadav82/webcode.git

━━━━━━━━━━━━━━━━━━
Shobhit Web
Learn • Explore • Grow
"""


async def about_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    if not update.message:
        return

    await update.message.reply_text(
        ABOUT_MESSAGE,
        reply_markup=main_keyboard(),
        disable_web_page_preview=True,
    )


# ============================================================
# BUTTON CALLBACKS
# ============================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    query = update.callback_query

    if not query:
        return

    await query.answer()

    if query.data == "about":

        await query.edit_message_text(
            ABOUT_MESSAGE,
            reply_markup=main_keyboard(),
            disable_web_page_preview=True,
        )

    elif query.data == "help":

        await query.edit_message_text(
            HELP_MESSAGE,
            reply_markup=main_keyboard(),
        )


# ============================================================
# UNKNOWN COMMAND
# ============================================================

async def unknown_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    if not update.message:
        return

    await update.message.reply_text(
        "Sorry, I don't recognize that command.\n\n"
        "Use /start to open the main menu.",
        reply_markup=main_keyboard(),
    )


# ============================================================
# ERROR HANDLER
# ============================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    logger.error(
        "Exception while handling an update:",
        exc_info=context.error,
    )


# ============================================================
# BOT INFORMATION
# ============================================================

async def setup_bot(application: Application) -> None:
    """
    Configure bot description and command menu.
    """

    await application.bot.set_my_short_description(
        "Coindocbot — useful projects and tools."
    )

    await application.bot.set_my_description(
        "Coindocbot provides quick access to useful projects "
        "and tools, including the video downloader bot "
        "@VidoMate82bot and the Web Code project."
    )

    await application.bot.set_my_commands(
        [
            BotCommand("start", "Start the bot"),
            BotCommand("help", "Show help"),
            BotCommand("about", "About Coindocbot"),
        ]
    )

    logger.info("Bot information configured successfully.")


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable is missing. "
            "Please set your Telegram bot token."
        )

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(setup_bot)
        .build()
    )

    # Commands
    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        CommandHandler("about", about_command)
    )

    # Inline button callbacks
    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    # Unknown commands
    application.add_handler(
        CommandHandler(None, unknown_command)
    )

    # Error handling
    application.add_error_handler(error_handler)

    logger.info("Coindocbot is starting...")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
