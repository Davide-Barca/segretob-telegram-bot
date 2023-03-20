import telebot

bot = telebot.TeleBot("6203959531:AAGbh0EqkLfHN7ZKl54cuxGB6sY8GtBO8bQ")


@bot.message_handler(commands=['start'])
def handle_command(message):
    print(message.text.lower())
    if message.text == '/start':
        bot.send_message(message.chat.id, message.text.lower())
    else:
        bot.send_message(message.chat.id, "Parla potebbile uaju")

print("Bot is running...")
bot.polling()