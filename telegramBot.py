from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
import random
from database_connected import (
    BOT_USERNAME,
    TOKEN,
)

from functions import (
    get_movie_info_by_name,
    get_movie_info_by_rate,
    get_movie_info_by_year,
    get_movie_info_by_genre
)

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("That's Bot to find some film")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    Here are the commands you can use:
    /start - Start the bot
    /help - Show this help message
    /additional - Show additional information
    /findMovieByName - Find information about a movie by its name
    """
    await update.message.reply_text(help_text)


async def find_movie_by_name_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Write name of movie please")

async def find_movie_by_rate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Write min and max rate of random movie (like 7 - 10)")

async def find_movie_by_year_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Write year you want random film (2014-2018)")

async def find_movie_by_genre_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Write genre(-s) of random movie()")

# Responses


def handle_response(text: str) -> str:
    processed: str = text.lower()

    if "hello" in processed:
        return "Hey"
    if "how are you" in processed:
        return "I am good"
    if "ily" in processed:
        return "Me too"
    if "pashol nafig" in processed:
        return "sama poshla"
    if "syka" in processed:
        return "shut up"
    # if processed ==
    return "I dont understand you"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return

    movie_info_by_rate = get_movie_info_by_rate(text)
    movie_info_by_name = get_movie_info_by_name(text)
    movie_info_by_year = get_movie_info_by_year(text)
    movie_info_by_genre = get_movie_info_by_genre(text)

    response = ""
    if isinstance(movie_info_by_name, list) and movie_info_by_name:
        for movie in movie_info_by_name:
            response += f"Name: {movie['Title']}\n"
            response += f"Year: {movie['Year']}\n"
            response += f"Genre: {movie['Genre']}\n"
            response += f"Rate: {movie['Rate']}\n\n"
        await update.message.reply_text(response)

    elif '-' in text and movie_info_by_rate:
        response += f"Name: {movie_info_by_rate['Title']}\n"
        response += f"Year: {movie_info_by_rate['Year']}\n"
        response += f"Genre: {movie_info_by_rate['Genre']}\n"
        response += f"Rate: {movie_info_by_rate['Rate']}\n\n"
        await update.message.reply_text(response)

    elif movie_info_by_year:
        response += f"Name: {movie_info_by_year['Title']}\n"
        response += f"Year: {movie_info_by_year['Year']}\n"
        response += f"Genre: {movie_info_by_year['Genre']}\n"
        response += f"Rate: {movie_info_by_year['Rate']}\n\n"
        await update.message.reply_text(response)

    elif movie_info_by_genre:
        response += f"Name: {movie_info_by_genre['Title']}\n"
        response += f"Year: {movie_info_by_genre['Year']}\n"
        response += f"Genre: {movie_info_by_genre['Genre']}\n"
        response += f"Rate: {movie_info_by_genre['Rate']}\n\n"
        await update.message.reply_text(response)

    else:
        response: str = handle_response(text)
        await update.message.reply_text(response)



# Errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    print("Starting Bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("findMovieByName", find_movie_by_name_command))
    app.add_handler(CommandHandler("find_movie_by_rate", find_movie_by_rate_command))
    app.add_handler(CommandHandler("find_movie_by_year", find_movie_by_year_command))
    app.add_handler(CommandHandler("find_movie_by_genre", find_movie_by_genre_command))

    # Message
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=3)
