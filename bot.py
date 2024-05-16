import telebot
from typing import final
from main import load_knowledge_base, get_answer, add_to_knowledge_base

Token :final = "6792024677:AAEEHmBrkBLNJXsy7BcWgP_x3Hw5Z8AywEI"
bot = telebot.TeleBot(Token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    file_path = 'knowlage_base.json'
    data = load_knowledge_base(file_path)
    user_question = message.text
    answer = get_answer(user_question, data)
    if answer is not None:
        bot.reply_to(message, answer)
    else:
        bot.reply_to(message, "I don't know the answer to that question. Can you provide the answer?")
        bot.register_next_step_handler(message, process_answer, user_question, file_path, data)

def process_answer(message, user_question, file_path, data):
    user_answer = message.text
    add_to_knowledge_base(file_path, user_question, user_answer)
    data = load_knowledge_base(file_path)
    bot.reply_to(message, "Thank you! I've learned something new.")

print("Bot is working...")
bot.polling