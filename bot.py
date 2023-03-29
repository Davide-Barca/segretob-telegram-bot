from dotenv import load_dotenv
from user import User
from datetime import datetime, timedelta
from dateutil.parser import parse
import time
import locale
import os
import io
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

def is_date(string, fuzzy=False):
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

@bot.message_handler(commands=['start', 'help', 'id', 'today', 'tomorrow', 'ondev']) # Accede alla funzione sottostante quando viene inviato un comando
def handle_command(message):
    if message.text == '/start':
        set_user(message.from_user.username, message.from_user.id) # crea l'utenza
        log(f'Message | Username: {user.get_username()}, User_Id: {user.get_id()}, Text: {str(message.text)}')
        bot.send_message(message.chat.id, "Ciao!\nSono Segretob, il tuo segretario digitale.\nAl momento è possibile confrontare un solo calendario gestito da remoto, ma sto lavorando per fare in modo che al più presto potrai gestire il calendario che preferisci.\n\nDigita:\n\n/today per il programma di oggi\n/tomorrow per il programma di domani.\n<b>dd-mm-yyyy</b> per il programma del giorno che vuoi.", parse_mode='HTML')

    elif message.text == '/help':
        log(f'Message | Username: {user.get_username()}, User_Id: {user.get_id()}, Text: {str(message.text)}')
        bot.send_message(message.chat.id, text="Questi sono i comandi a cui posso rispondere:\n\n/start - avvia il bot\n/help - lista dei comandi\n/id - il tuo id\n/today - programma di oggi\n/tomorrow - programma di domani\n<b>dd-mm-yyyy</b> - programma data a scelta", parse_mode= 'HTML')

    elif message.text == '/id':
        log(f'Message | Username: {user.get_username()}, User_Id: {user.get_id()}, Text: {str(message.text)}')
        bot.send_message(message.chat.id, f"Your id is: {user.get_id()}")
    
    elif message.text == '/ondev':
        log(f'Message | Username: {user.get_username()}, User_Id: {user.get_id()}, Text: {str(message.text)}')
        bot.send_message(message.chat.id, "Funzioni in fase di sviluppo:\n\n1 ~ Implementazione notifica giornaliera\n2 ~ Gestione di un calendario personalizzato\n3 ~ Possibilità di inserire la data in qualsiasi formato", parse_mode='HTML')

    elif message.text == '/today':
        log(f'Message | Username: {user.get_username()}, User_Id: {user.get_id()}, Text: {str(message.text)}')
        locale.setlocale(locale.LC_TIME, "it_IT")
        date_time_str = time.strftime("%A, %B %d, %Y")
        # bot.send_message(message.chat.id, f"Data: {date_time_str}")

        with open("./Files/calendar.csv", 'r') as new_file:
            list = new_file.read()
        new_list = []
        for item in str(list).split("\n"):
            new_list.append(item.split(";"))

        for el in new_list:
            if(date_time_str in el[0]):
                response = f"In Data: {date_time_str} è previsto:\nMateria: {el[6]} \n Docente: {el[7]} \n Orario: dalle {el[2]} alle {el[3]} \n Aula {el[1]}"
                bot.send_message(message.chat.id, response)

    elif message.text == '/tomorrow':
        log(f'Message | Username: {user.get_username()}, User_Id: {user.get_id()}, Text: {str(message.text)}')
        locale.setlocale(locale.LC_TIME, "it_IT")
        now = datetime.now() + timedelta(1)
        date_time_str = now.strftime("%A, %B %d, %Y")
        # bot.send_message(message.chat.id, f"Data: {date_time_str}")

        with open("./Files/calendar.csv", 'r') as new_file:
            list = new_file.read()
        new_list = []
        for item in list.split("\n"):
            new_list.append(item.split(";"))

        for el in new_list:
            if(date_time_str in el[0]):
                response = f"In Data: {date_time_str} è previsto:\nMateria: {el[6]} \n Docente: {el[7]} \n Orario: dalle {el[2]} alle {el[3]} \n Aula {el[1]}"
                bot.send_message(message.chat.id, response)
    else:
        log(f'Message | Username: {user.get_username()}, User_Id: {user.get_id()}, Text: {str(message.text)}')
        bot.send_message(message.chat.id, "Mi dispiace ma non credo di aver capito.\nDigita /start per iniziare.")

@bot.message_handler(func=lambda m: True) # Accede alla funzione sottostante per tutti i messaggi inviati
def echo_all(message):
    log(f'Message | Username: {user.get_username()}, User_Id: {user.get_id()}, Text: {str(message.text)}')
    if(len(message.text) < 5):
        bot.send_message(message.chat.id, "Qualcosa è andato storto, riprova!")
    else:
        if(is_date(str(message.text))):
            if(message.text[2] == "-" and message.text[5] == "-"):
                split = message.text.split("-")
            elif(message.text[2] == "/" and message.text[5] == "/"):
                split = message.text.split("/")
            else:
                bot.send_message(message.chat.id, "Qualcosa è andato storto, riprova a scrivere la data separata dal carattere - o /")
                return False
                

            day = int(split[0])
            month = int(split[1])
            year = int(split[2])


            locale.setlocale(locale.LC_TIME, "it_IT@euro")
            now = datetime(year, month, day)
            date_time_str = now.strftime("%A, %B %d, %Y")

            with open("./Files/calendar.csv", 'r') as new_file:
                list = new_file.read()
            new_list = []
            for item in list.split("\n"):
                new_list.append(item.split(";"))
                    
            for el in new_list:
                if(date_time_str in el[0]):
                    response = f"In Data: {date_time_str} è previsto:\nMateria: {el[6]} \n Docente: {el[7]} \n Orario: dalle {el[2]} alle {el[3]} \n Aula {el[1]}"
                    bot.send_message(message.chat.id, response)
                return True
        bot.send_message(message.chat.id, "Data non trovata")
    #bot.send_message(message.chat.id, "Credo di non aver capito...\nAl momento accetto come testo solo date con questo formato <b>dd-mm-yyyy</b>", parse_mode='HTML')
    # bot.send_message(message.chat.id, "Mi dispiace ma in questo momento sono in grado di rispondere solo ai comandi /help.")

@bot.message_handler(content_types=['document']) # list relevant content types
def addfile(message):
    file_name = message.document.file_name # nome del file
    if(file_name[len(file_name)-4:len(file_name)] == ".csv"):
        file_info = bot.get_file(message.document.file_id) # {file_id, file_unique_id, file_size, file_path}
        downloaded_file = bot.download_file(file_info.file_path) # contenuto del file
        user.file_path = f"./Files/{user.get_id()}/{file_name}"

        with open(user.file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "File salvato correttamente!\n\n<i>Questa funzione non è ancora attiva!</i>", parse_mode="HTML")
        log(f'NEW FILE | Username: {user.get_username()}, User_Id: {user.get_id()}')
    else:
        bot.reply_to(message, "ATTENZIONE! Il file deve essere in formato .csv!\n\n<i>Facciamo notare che questa funzione non è ancora attiva!</i>", parse_mode="HTML")

log("BOT START RUNNING...")
bot.polling()
