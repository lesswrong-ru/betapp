import telebot
import sys
from telebot import types


telegramToken = sys.argv[1]
bot = telebot.TeleBot(telegramToken)
chatState = {}

def log_message(message):
    print message

####################### START #######################
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Good morning friend! What to predict something?")
    send_welcome(message)
    chatState[message.chat.id] = ''
    #todo add authentification

####################### HELP #######################
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "You can do several things. Type: \n"
                          "/predict - to predict something\n"
                          "/list - to list your predictions \n"
                          "/resolve - to resolve one of them\n"
                          "/cancel - cancel current operation\n"
                          "Good luck!")


####################### cancel #######################
@bot.message_handler(commands=['cancel'])
def cancel(message):
    chatState[message.chat.id] = ''
    bot.send_message(message.chat.id, "Canceled", reply_markup=types.ReplyKeyboardHide())
    send_welcome(message)


####################### PREDICT #######################
## step 1
@bot.message_handler(commands=['predict'])
def predict_start(message):
    chatState[message.chat.id] = { 'state' : 'predict_start'}
    bot.send_message(message.chat.id, "Type something you want to predict")

## step 2
def predict_answer(message):
    chatState[message.chat.id]['state'] = 'predict_answer'
    chatState[message.chat.id]['question'] = message
    markup = types.ReplyKeyboardMarkup()
    markup.row('YES', 'NO',)
    bot.send_message(message.chat.id, "What is your answer? Choose one of the options or type in your answer ", reply_markup=markup)

## step 3
def predict_chance(message):
    chatState[message.chat.id]['state'] = 'predict_chance'
    chatState[message.chat.id]['answer'] = message
    markup = types.ReplyKeyboardMarkup()
    markup.row('50%', '60%', '70%')
    markup.row('80%', '90%', '99%')
    bot.send_message(message.chat.id, "How sure you about it? Choose one of the options or type in your number", reply_markup=markup)

## step 4
def predict_reminder(message):
    chatState[message.chat.id]['state'] = 'predict_reminder'
    chatState[message.chat.id]['chance'] = message
    markup = types.ReplyKeyboardMarkup()
    markup.row('1 Hour', '6 Hours', '12 Hours')
    markup.row('1 Day', '1 Week', '1 Month')
    markup.row('No reminder')
    markup.one_time_keyboard = True
    bot.send_message(message.chat.id, "Do you want me to remind you about it? You can type in date if you want", reply_markup=markup)


## step 5
def predict_done(message):
    chatState[message.chat.id] = {}
    bot.send_message(message.chat.id, "Done!", reply_markup=types.ReplyKeyboardHide())

# all other messages
state2handler = {
    'predict_start' : predict_answer,
    'predict_answer': predict_chance,
    'predict_chance': predict_reminder,
    'predict_reminder': predict_done,
}

@bot.message_handler(func=lambda message: True)
def unrecognized(message):
    chat_id = message.chat.id
    # if chatState[chat_id] and chatState[chat_id]['state'] and state2handler[chatState[chat_id]['state']]:
    if chat_id in chatState and 'state' in chatState[chat_id] and chatState[chat_id]['state'] in state2handler:
        state2handler[chatState[chat_id]['state']](message)
    else:
        print "Don't know how to handle message "
        print message



print "Start polling..."
bot.polling()

