import telebot
from telebot import types

import sys
import requests
from requests import RequestException, HTTPError

telegramToken = sys.argv[1]
serverHost = sys.argv[2]
serverPort = sys.argv[3]

bot = telebot.TeleBot(telegramToken)
chatState = {}
serverUrl = 'http://' + serverHost + ':' + serverPort + '/api/bets/{}'


def make_request_to_server(id='', method='GET', data={}):
    url = serverUrl.format(id)
    resp = requests.request(method, url, data=data)
    resp.raise_for_status()
    try:
        return resp.json()
    except ValueError:
        return None


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
    try:
        make_request_to_server(method="POST",
                               data={'title': chatState[chat_id]['prediction'],
                                     'confidence': chatState[chat_id]['chance']})
        text = 'Done!'
    except RequestException:
        text = 'Something went wrong.'
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


## step 3.5
def check_chance(message):
    chance_str = message.text
    is_percentage = False
    if chance_str.endswith('%'):
        chance_str = chance_str[:-1]
        is_percentage = True

    try:
        chance = float(chance_str)

        if is_percentage:
            chance /= 100

        if chance < 0 or chance > 1:
            bot.send_message(message.chat.id,
                             "Probability should be in interval from 0 to 1. Try again.")
        else:
            chatState[message.chat.id]['chance'] = chance
            predict_reminder(message)

    except ValueError:
        bot.send_message(message.chat.id, "You should type proper number. Try again.")


## step 4
def predict_reminder(message):
    chatState[message.chat.id]['state'] = 'predict_reminder'
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
    try:
        response = make_request_to_server()
        text = ''
        for element in response:
            text += '{}. {}\n'.format(element['id'], element['title'])
        print(response)
    except RequestException:
        text = "Something went wrong."
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
    chatState[message.chat.id]['prediction_id'] = message.text
    try:
        prediction = make_request_to_server(message.text)
        bot.send_message(message.chat.id,
                         "So your prediction was:\n{}".format(
                             prediction['title']))
        markup = types.ReplyKeyboardMarkup()
        markup.row('Correct', 'Incorrect')
        markup.row('Cancel')
        bot.send_message(message.chat.id, "Did you guess it right?", reply_markup=markup)
    except RequestException as e:
        if type(e) == HTTPError and e.response.status_code == 404:
            bot.send_message(message.chat.id, "There is no prediction with such number.")
            cancel(message)
        else:
            bot.send_message(message.chat.id, "Something went wrong.")


## step 3
def resolve_resolution(message):
    chatState[message.chat.id]['state'] = 'resolve_resolution'

    if message.text.lower() in ['y', 'yes', 'correct', 'right']:
        outcome = True
    elif message.text.lower() in ['n', 'no', 'incorrect']:
        outcome = False
    else:
        if message.text.lower() != 'cancel':
            bot.send_message(message.chat.id, "Cannot interpret your answer",
                             reply_markup=types.ReplyKeyboardHide())
        cancel(message)
        return

    chatState[message.chat.id]['prediction_outcome'] = outcome
    try:
        make_request_to_server(
            chatState[message.chat.id]['prediction_id'],
            method="PATCH",
            data={'outcome': outcome})
    except RequestException:
        bot.send_message(message.chat.id, "Something went wrong.",
                         reply_markup=types.ReplyKeyboardHide())
        cancel(message)
        return

    bot.send_message(message.chat.id, "Ok, we saved that. Good luck next time",
                     reply_markup=types.ReplyKeyboardHide())


####################### ALL OTHER MESSAGES #######################
state2handler = {
    'predict_start': predict_answer,
    'predict_answer': predict_chance,
    'predict_chance': check_chance,
    'check_chance': check_chance,
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
        start(message)
        print("Don't know how to handle message ")
        print(message)


print("Start polling...")
bot.polling()
