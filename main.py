import os
import time
import openai
import telebot
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")
api = os.getenv("API")

openai.api_key = api
bot = telebot.TeleBot(token)
context = []


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Работаем, бип')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    global context
    context.append(message.text)

    typing_message = bot.send_message(message.chat.id, 'Дай подумать')

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt='\n'.join(context),
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7
    )

    bot.edit_message_text(response.choices[0].text, chat_id=message.chat.id, message_id=typing_message.message_id)


bot.polling(none_stop=True)
