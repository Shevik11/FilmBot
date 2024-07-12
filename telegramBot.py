from typing import Final
import environ
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import pyrebase

env = environ.Env()
environ.Env.read_env()

TOKEN: Final = env("TOKEN")
BOT_USERNAME: Final = env("BOT_USERNAME")

config = {
    "apiKey": env("API_KEY"),
    "authDomain": env("AUTH_DOMAIN"),
    "databaseURL": env("DATABASE_URL"),
    "projectId": env("PROJECT_ID"),
    "storageBucket": env("STORAGE_BUCKET"),
    "messagingSenderId": env("MESSAGING_SENDER_ID"),
    "appId": env("APP_ID"),
    "measurementId": env("MEASUREMENT_ID"),
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
all_movies = db.child("movies").get()


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello, Thanks use me. ily')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    Here are the commands you can use:
    /start - Start the bot
    /help - Show this help message
    /additional - Show additional information
    /findMovieByName - Find information about a movie by its name
    """
    await update.message.reply_text(help_text)

async def additional_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'm additional_command")

async def find_movie_by_name_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Write name of movie please")



# Responses

def handle_response(text:str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey'
    if 'how are you' in processed:
        return 'I am good'
    if 'ily' in processed:
        return 'Me too'
    # if processed ==
    return 'I dont understand you'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    print('here_1')
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    print('here_2')
    movie_info = get_movie_info(text)
    print('here_4')
    print(movie_info)
    if movie_info:
        response = f"Name: {movie_info['Title']}\n"
        response += f"Year: {movie_info['Year']}\n"
        response += f"Genre: {movie_info['Genre']}\n"
        response += f"Rate: {movie_info['Rate']}"

    else:
        response: str = handle_response(text)
    print('here_3')
    print('Bot:', response)
    await update.message.reply_text(response)

def get_movie_info(movie_name):
    for movie in all_movies.each():
        if movie.val()['Title'].lower() == movie_name.lower():
            return movie.val()
    return None

# Errors


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print("Starting Bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('additional', additional_command))
    app.add_handler(CommandHandler('find_movie_by_name', find_movie_by_name_command))

    # Message
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)