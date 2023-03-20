from dotenv import load_dotenv
from user import User
import os
import telebot

load_dotenv()
token = os.getenv("TOKEN")

bot = telebot.TeleBot(token)

def read(user):
    print(user.get_file_path())
    with open(user.get_file_path(), 'r') as content:
        return content.read()

@bot.message_handler(commands=['start', 'help', 'id', 'username', 'read']) # Accede alla funzione sottostante quando viene inviato un comando
def handle_command(message):
    user = User(message.from_user.username, message.from_user.id)
    if message.text == '/start':
        bot.send_message(message.chat.id, "Ciao!\nSono Segretob, il tuo segretario digitale.\nPer poter continuare carica il file .csv che contiene il tuo calendaro.\n\nDigita /help per saperne di più su come formattare il suo file csv.")
    elif message.text == '/help':
        bot.send_message(message.chat.id, "Ci scusiamo ma il messaggio è in sviluppo.")
    elif message.text == '/id':
        bot.send_message(message.chat.id, f"Your id is: {user.get_id()}")
    elif message.text == '/username':
        bot.send_message(message.chat.id, f"Your username is: {user.get_username()}")
    elif message.text == '/read':
        bot.send_message(message.chat.id, read(user))
    else:
        bot.send_message(message.chat.id, "Mi dispiace ma non credo di aver capito.\nDigita /start per iniziare.")

@bot.message_handler(func=lambda m: True) # Accede alla funzione sottostante per tutti i messaggi inviati
def echo_all(message):
    bot.send_message(message.chat.id, "Un saluto")

@bot.message_handler(content_types=['document']) # list relevant content types
def addfile(message):
    user = User(message.from_user.username, message.from_user.id)
    file_name = message.document.file_name # nome del file
    file_info = bot.get_file(message.document.file_id) # {file_id, file_unique_id, file_size, file_path}
    downloaded_file = bot.download_file(file_info.file_path) # contenuto del file

    # print(file_name, "| FILE NAME")
    # print(file_info, "| FILE INFO")
    # print(downloaded_file, "| FILE DOWNLOADED")

    with open(f"./Files/{user.get_id()}/{file_name}", 'wb') as new_file:
        user.set_file_path(f"./Files/{user.get_id()}/{file_name}")
        new_file.write(downloaded_file)

    bot.reply_to(message, "File salvato correttamente!")

print("Bot is running...")
bot.polling()