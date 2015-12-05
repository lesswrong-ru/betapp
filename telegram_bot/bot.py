import telebot
from telebot import types

import sys
import requests

telegramToken = sys.argv[1]
serverHost = sys.argv[2]
serverPort = sys.argv[3]

bot = telebot.TeleBot(telegramToken)
chatState = {}
serverUrl = 'http://' + serverHost + ':' + serverPort + '/api/bets/{}'


def make_request_to_server(id='', method='GET', data={}):
    url = serverUrl.format(id)
    resp = requests.request(method, url, data=data)
    return {'code': resp.status_code, 'data': resp.json()}


####################### START #######################
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Good morning friend! What to predict something?")
    send_help(message)
    chatState[message.chat.id] = ''
    # todo add authentification


####################### HELP #######################
@bot.message_handler(commands=['help'])
def send_help(message):
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
    send_help(message)


def save_prediction(message):
    chat_id = message.chat.id
    response = make_request_to_server(method="POST",
                                      data={'title': chatState[chat_id]['prediction'],
                                            'confidence': chatState[chat_id]['chance']})
    if response['code'] == 201:
        text = 'Done!'
    else:
        text = 'Fail!'
    bot.send_message(chat_id, text, reply_markup=types.ReplyKeyboardHide())
    chatState[message.chat.id] = {}


####################### PREDICT #######################
## step 1
@bot.message_handler(commands=['predict'])
def predict_start(message):
    chatState[message.chat.id] = {'state': 'predict_start'}
    bot.send_message(message.chat.id, "Type something you want to predict")


## step 2
def predict_answer(message):
    chatState[message.chat.id]['state'] = 'predict_answer'
    chatState[message.chat.id]['prediction'] = message.text
    markup = types.ReplyKeyboardMarkup()
    markup.row('YES', 'NO', )
    bot.send_message(message.chat.id, "What is your answer? Choose one of the options or type in your answer ",
                     reply_markup=markup)


## step 3
def predict_chance(message):
    chatState[message.chat.id]['state'] = 'predict_chance'
    chatState[message.chat.id]['answer'] = message.text
    markup = types.ReplyKeyboardMarkup()
    markup.row('50%', '60%', '70%')
    markup.row('80%', '90%', '99%')
    bot.send_message(message.chat.id, "How sure you about it? Choose one of the options or type in your number",
                     reply_markup=markup)


## step 4
def predict_reminder(message):
    chatState[message.chat.id]['state'] = 'predict_reminder'
    chatState[message.chat.id]['chance'] = message.text[:-1]
    markup = types.ReplyKeyboardMarkup()
    markup.row('1 Hour', '6 Hours', '12 Hours')
    markup.row('1 Day', '1 Week', '1 Month')
    markup.row('No reminder')
    markup.one_time_keyboard = True
    bot.send_message(message.chat.id, "Do you want me to remind you about it? You can type in date if you want",
                     reply_markup=markup)


####################### LIST #######################
@bot.message_handler(commands=['list'])
def prediction_list(message):
    response = make_request_to_server()
    print(response)
    text = ''
    for element in response['data']:
        text += '{}. {}\n'.format(element['id'], element['title'])

    bot.send_message(message.chat.id, text)


####################### RESOLVE #######################
@bot.message_handler(commands=['resolve'])
## step 1
def resolve_start(message):
    chatState[message.chat.id] = {'state': 'resolve_start'}
    bot.send_message(message.chat.id, "Which prediction do you want to resolve? Type in the number:")
    prediction_list(message)


## step 2
def resolve_choose(message):
    chatState[message.chat.id]['state'] = 'resolve_choose'
    chatState[message.chat.id]['prediction_id'] = message
    prediction = make_request_to_server(message.text)
    bot.send_message(message.chat.id,
                     "So your prediction was:\n{}".format(
                         prediction['data']['title']))
    markup = types.ReplyKeyboardMarkup()
    markup.row('Correct', 'Incorrect')
    markup.row('Cancel')
    bot.send_message(message.chat.id, "Did you guess it right?", reply_markup=markup)


## step 3
def resolve_resolution(message):
    chatState[message.chat.id]['state'] = 'resolve_resolution'
    if message.text == 'Cancel':
        cancel(message)
    else:
        chatState[message.chat.id]['prediction_outcome'] = message
        bot.send_message(message.chat.id, "Ok, we saved that. Good luck next time",
                         reply_markup=types.ReplyKeyboardHide())
        # todo: save it on the server


####################### ALL OTHER MESSAGES #######################
state2handler = {
    'predict_start': predict_answer,
    'predict_answer': predict_chance,
    'predict_chance': predict_reminder,
    'predict_reminder': save_prediction,
    'resolve_start': resolve_choose,
    'resolve_choose': resolve_resolution,
}


@bot.message_handler(func=lambda message: True)
def unrecognized(message):
    chat_id = message.chat.id
    if chat_id in chatState and 'state' in chatState[chat_id] and chatState[chat_id]['state'] in state2handler:
        state2handler[chatState[chat_id]['state']](message)
    else:
        print("Don't know how to handle message ")
        print(message)


print("Start polling...")
bot.polling()
