import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler,filters, Dispatcher
import os
import openai

# Set up the Telegram bot
bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN"))

# Create a dispatcher for the bot
dispatcher = Dispatcher(bot, None)


# Define a function to handle the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Howdy, ChattyPilot here. Anything I can help you with?")


# Define a function to handle user messages and send them to ChatGPT API
def chat(update, context):
    # Get user input from message
    user_input = update.message.text

    # Use OpenAI's GPT-3 to generate a response to user input
    response = openai.Completion.create(
        engine="davinci", prompt=f"User: {user_input}\nBot:", max_tokens=150
    )

    # Extract the response text from OpenAI's API response
    response_text = response.choices[0].text.strip()

    # Send the response back to the user via Telegram bot
    context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)


# Set up command handler for /start command
start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

# Set up message handler for user messages
chat_handler = MessageHandler(filters.text & ~filters.command, chat)
dispatcher.add_handler(chat_handler)

# Start the Telegram bot
updater = Updater(token=os.getenv("TELEGRAM_TOKEN"), use_context=True, dispatcher=dispatcher)
updater.start_polling()
updater.idle()
