from dotenv import load_dotenv
from user import User
from datetime import datetime, timedelta
import time
import locale
import os
import telebot

load_dotenv()
token = os.getenv("TOKEN")

bot = telebot.TeleBot(token)

def log(message):
    print(message)
    log_path = "./Files/log_activities.log"
    with open(log_path, 'a') as new_file:
        new_file.write(f'{message}\n')

def set_user(username, user_id):
    global user
    user = User(username, user_id)
    log(f'NEW USER | Username: {user.get_username()}, User_Id: {user.get_id()}')

# def read(user):
#     print(user.file_path)
#     with open(user.file_path, 'r') as content:
#         return content.read()

@bot.message_handler(commands=['start', 'help', 'id', 'username', 'today', 'tomorrow', 'user']) # Accede alla funzione sottostante quando viene inviato un comando
def handle_command(message):
    if message.text == '/start':
        set_user(message.from_user.username, message.from_user.id) # crea l'utenza
        bot.send_message(message.chat.id, "Ciao!\nSono Segretob, il tuo segretario digitale.\nPer poter continuare carica il file .csv che contiene il tuo calendaro.\n\nDigita /help per saperne di più su come formattare il suo file csv.")
    elif message.text == '/help':
        bot.send_message(message.chat.id, "Ci scusiamo ma il messaggio è in sviluppo.")
    elif message.text == '/id':
        bot.send_message(message.chat.id, f"Your id is: {user.get_id()}")
    elif message.text == '/username':
        bot.send_message(message.chat.id, f"Your username is: {user.get_username()}")
    # elif message.text == '/today':
    #     locale.setlocale(locale.LC_TIME, "it_IT")
    #     date_time_str = time.strftime("%A, %B %d, %Y")
    #     bot.send_message(message.chat.id, f"Data: {date_time_str}")
    # elif message.text == '/tomorrow':
    #     locale.setlocale(locale.LC_TIME, "it_IT")
    #     date_time_str = time.strftime("%A, %B %d, %Y")
    #     bot.send_message(message.chat.id, f"Data: {date_time_str}")
    elif message.text == '/user':
        return True
    else:
        bot.send_message(message.chat.id, "Mi dispiace ma non credo di aver capito.\nDigita /start per iniziare.")

@bot.message_handler(func=lambda m: True) # Accede alla funzione sottostante per tutti i messaggi inviati
def echo_all(message):
    print(user.check())
    bot.send_message(message.chat.id, "Un saluto")

@bot.message_handler(content_types=['document']) # list relevant content types
def addfile(message):
    file_name = message.document.file_name # nome del file
    file_info = bot.get_file(message.document.file_id) # {file_id, file_unique_id, file_size, file_path}
    downloaded_file = bot.download_file(file_info.file_path) # contenuto del file
    user.file_path = f"./Files/{user.get_id()}/{file_name}"

    with open(user.file_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "File salvato correttamente!")
    log(f'NEW FILE | Username: {user.get_username()}, User_Id: {user.get_id()}')

log("BOT START RUNNING...")
bot.polling()